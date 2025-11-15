#!/usr/bin/env python3
"""
Portfolio Performance Auditor
Comprehensive performance analysis tool for developer portfolios
"""

import json
import os
import sys
import argparse
import subprocess
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import dataclasses

@dataclasses.dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    lighthouse_score: float
    fcp: float  # First Contentful Paint
    lcp: float  # Largest Contentful Paint
    tti: float  # Time to Interactive
    cls: float  # Cumulative Layout Shift
    fid: float  # First Input Delay
    bundle_size: int
    total_requests: int
    total_size: int
    performance_grade: str

@dataclasses.dataclass
class AuditResult:
    """Audit result structure"""
    url: str
    timestamp: datetime
    metrics: PerformanceMetrics
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    budget_compliance: Dict[str, bool]
    portfolio_specific_issues: List[str]

class PortfolioPerformanceAuditor:
    """Main auditor class for portfolio performance analysis"""

    def __init__(self, portfolio_path: str, output_dir: str = "./reports"):
        self.portfolio_path = Path(portfolio_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Performance budget thresholds
        self.budget = {
            'lighthouse_score': 95,
            'fcp': 1000,  # 1.0s
            'lcp': 2500,  # 2.5s
            'fid': 100,   # 100ms
            'cls': 0.1,
            'bundle_size': 250 * 1024,  # 250KB
            'total_requests': 50,
            'total_size': 1024 * 1024  # 1MB
        }

    def run_lighthouse_audit(self, url: str) -> Dict[str, Any]:
        """Run Lighthouse audit and return results"""
        try:
            # Check if lighthouse is installed
            subprocess.run(['lighthouse', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Lighthouse not found. Installing...")
            subprocess.run(['npm', 'install', '-g', 'lighthouse'], check=True)

        print(f"🔍 Running Lighthouse audit for {url}")

        # Run Lighthouse audit
        cmd = [
            'lighthouse', url,
            '--output=json',
            '--output-path=/tmp/lighthouse_report.json',
            '--chrome-flags="--headless"',
            '--quiet'
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)

            with open('/tmp/lighthouse_report.json', 'r') as f:
                return json.load(f)

        except subprocess.CalledProcessError as e:
            print(f"❌ Lighthouse audit failed: {e}")
            return {}

    def analyze_bundle_size(self) -> Dict[str, Any]:
        """Analyze bundle size and composition"""
        print("📦 Analyzing bundle size...")

        # Check for Next.js build output
        next_build_dir = self.portfolio_path / '.next'
        bundle_analysis = {
            'total_size': 0,
            'chunks': [],
            'large_assets': [],
            'unused_exports': []
        }

        if next_build_dir.exists():
            for chunk_file in next_build_dir.rglob('*.js'):
                size = chunk_file.stat().st_size
                bundle_analysis['total_size'] += size
                bundle_analysis['chunks'].append({
                    'name': chunk_file.name,
                    'size': size,
                    'path': str(chunk_file.relative_to(self.portfolio_path))
                })

                if size > 100 * 1024:  # 100KB threshold
                    bundle_analysis['large_assets'].append(str(chunk_file))

        return bundle_analysis

    def analyze_images(self) -> Dict[str, Any]:
        """Analyze image optimization opportunities"""
        print("🖼️ Analyzing images...")

        image_analysis = {
            'total_images': 0,
            'unoptimized_formats': [],
            'oversized_images': [],
            'missing_alt_text': [],
            'loading_strategies': {}
        }

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}

        for img_file in self.portfolio_path.rglob('*'):
            if img_file.suffix.lower() in image_extensions:
                size = img_file.stat().st_size
                image_analysis['total_images'] += 1

                # Check for unoptimized formats
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    image_analysis['unoptimized_formats'].append(str(img_file))

                # Check for oversized images
                if size > 500 * 1024:  # 500KB threshold
                    image_analysis['oversized_images'].append({
                        'path': str(img_file),
                        'size': size
                    })

        return image_analysis

    def analyze_code_patterns(self) -> Dict[str, Any]:
        """Analyze code for performance anti-patterns"""
        print("🔍 Analyzing code patterns...")

        code_analysis = {
            'bundle_imports': [],
            'react_patterns': {
                'missing_keys': [],
                'unnecessary_renders': [],
                'large_components': []
            },
            'async_issues': [],
            'performance_antipatterns': []
        }

        # Analyze React components
        for js_file in self.portfolio_path.rglob('*.jsx'):
            content = js_file.read_text(encoding='utf-8')

            # Check for large components
            if len(content.splitlines()) > 200:
                code_analysis['react_patterns']['large_components'].append(str(js_file))

            # Check for missing keys in lists
            if '.map(' in content and 'key=' not in content:
                code_analysis['react_patterns']['missing_keys'].append(str(js_file))

        return code_analysis

    def check_portfolio_specific_issues(self) -> List[str]:
        """Check for portfolio-specific performance issues"""
        print("🎨 Checking portfolio-specific issues...")

        issues = []

        # Check for syntax highlighting libraries
        syntax_libraries = ['prism', 'highlight.js', 'monaco-editor']
        for lib in syntax_libraries:
            if any(lib in f.name.lower() for f in self.portfolio_path.rglob('*')):
                issues.append(f"Consider optimizing syntax highlighting with {lib}")

        # Check for heavy third-party embeds
        embed_patterns = ['codepen', 'codesandbox', 'github.com/embed']
        for pattern in embed_patterns:
            if any(pattern in f.read_text(encoding='utf-8') for f in self.portfolio_path.rglob('*.jsx')):
                issues.append(f"Consider lazy loading {pattern} embeds")

        return issues

    def generate_recommendations(self, metrics: PerformanceMetrics,
                               bundle_analysis: Dict,
                               image_analysis: Dict,
                               code_analysis: Dict) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []

        # Core Web Vitals recommendations
        if metrics.lcp > self.budget['lcp']:
            recommendations.append("🎯 Optimize Largest Contentful Paint - preload critical resources")

        if metrics.fid > self.budget['fid']:
            recommendations.append("⚡ Reduce First Input Delay - minimize JavaScript execution time")

        if metrics.cls > self.budget['cls']:
            recommendations.append("📐 Reduce Cumulative Layout Shift - specify image dimensions")

        # Bundle size recommendations
        if bundle_analysis['total_size'] > self.budget['bundle_size']:
            recommendations.append("📦 Implement code splitting and tree shaking")

        # Image recommendations
        if image_analysis['unoptimized_formats']:
            recommendations.append("🖼️ Convert images to WebP/AVIF formats")

        # Code recommendations
        if code_analysis['react_patterns']['large_components']:
            recommendations.append("🧩 Break down large React components")

        return recommendations

    def calculate_performance_grade(self, metrics: PerformanceMetrics) -> str:
        """Calculate overall performance grade"""
        score = 0
        max_score = 5

        if metrics.lighthouse_score >= 95:
            score += 1
        if metrics.fcp <= self.budget['fcp']:
            score += 1
        if metrics.lcp <= self.budget['lcp']:
            score += 1
        if metrics.fid <= self.budget['fid']:
            score += 1
        if metrics.cls <= self.budget['cls']:
            score += 1

        grades = ['F', 'D', 'C', 'B', 'A+']
        return grades[min(score, 4)]

    def run_audit(self, url: Optional[str] = None) -> AuditResult:
        """Run complete performance audit"""
        print("🚀 Starting Portfolio Performance Audit")

        # Use provided URL or detect from Next.js project
        if not url:
            # Try to detect if it's a running Next.js app
            url = "http://localhost:3000"
            try:
                requests.get(url, timeout=5)
            except requests.RequestException:
                print("⚠️ No running portfolio detected. Please provide --url parameter")
                return None

        # Run Lighthouse audit
        lighthouse_data = self.run_lighthouse_audit(url)

        # Extract metrics
        performance_score = lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0) * 100

        # Get audits data
        audits = lighthouse_data.get('audits', {})

        metrics = PerformanceMetrics(
            lighthouse_score=performance_score,
            fcp=audits.get('first-contentful-paint', {}).get('numericValue', 0),
            lcp=audits.get('largest-contentful-paint', {}).get('numericValue', 0),
            tti=audits.get('interactive', {}).get('numericValue', 0),
            cls=audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
            fid=audits.get('max-potential-fid', {}).get('numericValue', 0),
            bundle_size=0,
            total_requests=audits.get('network-requests', {}).get('numericValue', 0),
            total_size=audits.get('total-byte-weight', {}).get('numericValue', 0),
            performance_grade=""
        )

        # Run additional analyses
        bundle_analysis = self.analyze_bundle_size()
        image_analysis = self.analyze_images()
        code_analysis = self.analyze_code_patterns()
        portfolio_issues = self.check_portfolio_specific_issues()

        metrics.bundle_size = bundle_analysis['total_size']
        metrics.performance_grade = self.calculate_performance_grade(metrics)

        # Generate recommendations
        recommendations = self.generate_recommendations(metrics, bundle_analysis, image_analysis, code_analysis)

        # Check budget compliance
        budget_compliance = {
            'lighthouse_score': metrics.lighthouse_score >= self.budget['lighthouse_score'],
            'fcp': metrics.fcp <= self.budget['fcp'],
            'lcp': metrics.lcp <= self.budget['lcp'],
            'fid': metrics.fid <= self.budget['fid'],
            'cls': metrics.cls <= self.budget['cls'],
            'bundle_size': metrics.bundle_size <= self.budget['bundle_size']
        }

        return AuditResult(
            url=url,
            timestamp=datetime.now(),
            metrics=metrics,
            issues=lighthouse_data.get('audits', {}),
            recommendations=recommendations,
            budget_compliance=budget_compliance,
            portfolio_specific_issues=portfolio_issues
        )

    def generate_report(self, result: AuditResult) -> str:
        """Generate comprehensive performance report"""
        report = []

        report.append("# Portfolio Performance Audit Report")
        report.append(f"Generated: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"URL: {result.url}")
        report.append("")

        # Performance Summary
        report.append("## 🎯 Performance Summary")
        report.append(f"**Performance Grade:** {result.metrics.performance_grade}")
        report.append(f"**Lighthouse Score:** {result.metrics.lighthouse_score:.0f}")
        report.append(f"**First Contentful Paint:** {result.metrics.fcp:.0f}ms")
        report.append(f"**Largest Contentful Paint:** {result.metrics.lcp:.0f}ms")
        report.append(f"**First Input Delay:** {result.metrics.fid:.0f}ms")
        report.append(f"**Cumulative Layout Shift:** {result.metrics.cls:.3f}")
        report.append(f"**Bundle Size:** {result.metrics.bundle_size / 1024:.1f}KB")
        report.append("")

        # Core Web Vitals Status
        report.append("## 📊 Core Web Vitals Status")
        for metric, compliant in result.budget_compliance.items():
            status = "✅" if compliant else "❌"
            report.append(f"{status} {metric.replace('_', ' ').title()}")
        report.append("")

        # Recommendations
        if result.recommendations:
            report.append("## 💡 Optimization Recommendations")
            for rec in result.recommendations:
                report.append(f"- {rec}")
            report.append("")

        # Portfolio Specific Issues
        if result.portfolio_specific_issues:
            report.append("## 🎨 Portfolio-Specific Issues")
            for issue in result.portfolio_specific_issues:
                report.append(f"- {issue}")
            report.append("")

        # Performance Budget Analysis
        report.append("## 📈 Performance Budget Analysis")
        report.append("```json")
        report.append(json.dumps(result.budget_compliance, indent=2))
        report.append("```")
        report.append("")

        return "\n".join(report)

    def save_report(self, result: AuditResult, filename: Optional[str] = None) -> str:
        """Save audit report to file"""
        if not filename:
            timestamp = result.timestamp.strftime('%Y%m%d_%H%M%S')
            filename = f"performance_audit_{timestamp}.md"

        report_path = self.output_dir / filename
        report_content = self.generate_report(result)

        report_path.write_text(report_content, encoding='utf-8')
        print(f"📄 Report saved: {report_path}")

        return str(report_path)

def main():
    parser = argparse.ArgumentParser(description='Portfolio Performance Auditor')
    parser.add_argument('portfolio_path', help='Path to portfolio project')
    parser.add_argument('--url', help='Portfolio URL to audit')
    parser.add_argument('--output', default='./reports', help='Output directory for reports')
    parser.add_argument('--format', choices=['md', 'json'], default='md', help='Report format')

    args = parser.parse_args()

    # Initialize auditor
    auditor = PortfolioPerformanceAuditor(args.portfolio_path, args.output)

    # Run audit
    result = auditor.run_audit(args.url)

    if result:
        # Generate and save report
        auditor.save_report(result)

        # Print summary
        print("\n🎯 Audit Summary:")
        print(f"Performance Grade: {result.metrics.performance_grade}")
        print(f"Lighthouse Score: {result.metrics.lighthouse_score:.0f}")
        print(f"Budget Compliance: {sum(result.budget_compliance.values())}/{len(result.budget_compliance)}")
    else:
        print("❌ Audit failed")
        sys.exit(1)

if __name__ == "__main__":
    main()