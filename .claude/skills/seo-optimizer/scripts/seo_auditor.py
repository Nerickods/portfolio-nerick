#!/usr/bin/env python3
"""
SEO Auditor for Developer Portfolios
Comprehensive technical SEO analysis and optimization recommendations
"""

import re
import requests
import json
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import time


@dataclass
class SEOAuditResult:
    """Results from SEO audit"""
    score: int
    issues: List[Dict]
    recommendations: List[str]
    technical_seo: Dict
    performance: Dict
    content_optimization: Dict


class SEOAuditor:
    """Comprehensive SEO auditor for developer portfolios"""

    def __init__(self):
        self.tech_keywords = [
            'react', 'next.js', 'node.js', 'python', 'javascript', 'typescript',
            'vue.js', 'angular', 'django', 'flask', 'express', 'mongodb',
            'postgresql', 'mysql', 'aws', 'docker', 'kubernetes', 'git',
            'github', 'html', 'css', 'sass', 'webpack', 'rest api', 'graphql'
        ]

        self.recruiter_keywords = [
            'developer', 'engineer', 'full stack', 'frontend', 'backend',
            'software engineer', 'web developer', 'mobile developer',
            'devops', 'senior', 'junior', 'mid-level', 'lead', 'principal'
        ]

    def audit_portfolio(self, url: str, html_content: str = None) -> SEOAuditResult:
        """Perform comprehensive SEO audit"""

        if html_content is None:
            try:
                response = requests.get(url, timeout=10)
                html_content = response.text
            except requests.RequestException as e:
                return self._create_error_result(f"Failed to fetch URL: {e}")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Technical SEO Analysis
        technical_seo = self._analyze_technical_seo(soup, url)

        # Performance Analysis
        performance = self._analyze_performance(html_content)

        # Content Optimization
        content_optimization = self._analyze_content(soup)

        # Calculate overall score
        score = self._calculate_score(technical_seo, performance, content_optimization)

        # Generate issues and recommendations
        issues = self._identify_issues(technical_seo, performance, content_optimization)
        recommendations = self._generate_recommendations(issues)

        return SEOAuditResult(
            score=score,
            issues=issues,
            recommendations=recommendations,
            technical_seo=technical_seo,
            performance=performance,
            content_optimization=content_optimization
        )

    def _analyze_technical_seo(self, soup: BeautifulSoup, url: str) -> Dict:
        """Analyze technical SEO elements"""

        # Title tag analysis
        title_tag = soup.find('title')
        title_length = len(title_tag.text) if title_tag else 0
        title_optimized = title_tag and 50 <= title_length <= 60 and 'developer' in title_tag.text.lower()

        # Meta description analysis
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc_length = len(meta_desc['content']) if meta_desc and meta_desc.get('content') else 0
        desc_optimized = meta_desc and 120 <= desc_length <= 160

        # Heading structure
        headings = {
            f'h{i}': len(soup.find_all(f'h{i}'))
            for i in range(1, 7)
        }

        h1_count = headings['h1']
        proper_h1 = h1_count == 1

        # Image alt text
        images = soup.find_all('img')
        images_with_alt = sum(1 for img in images if img.get('alt'))
        alt_coverage = (images_with_alt / len(images) * 100) if images else 100

        # Meta tags
        meta_tags = {
            'viewport': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'og_title': bool(soup.find('meta', property='og:title')),
            'og_description': bool(soup.find('meta', property='og:description')),
            'og_image': bool(soup.find('meta', property='og:image')),
            'twitter_card': bool(soup.find('meta', name='twitter:card')),
            'canonical': bool(soup.find('link', rel='canonical')),
            'robots': bool(soup.find('meta', name='robots'))
        }

        # Schema markup
        scripts = soup.find_all('script', type='application/ld+json')
        schema_present = len(scripts) > 0
        project_schema = any('"@type": "Project"' in str(script) for script in scripts)
        person_schema = any('"@type": "Person"' in str(script) for script in scripts)

        return {
            'title': {
                'present': bool(title_tag),
                'length': title_length,
                'optimized': title_optimized,
                'content': title_tag.text.strip() if title_tag else None
            },
            'meta_description': {
                'present': bool(meta_desc),
                'length': desc_length,
                'optimized': desc_optimized,
                'content': meta_desc.get('content', '') if meta_desc else None
            },
            'headings': headings,
            'h1_proper': proper_h1,
            'images': {
                'total': len(images),
                'with_alt': images_with_alt,
                'alt_coverage': alt_coverage
            },
            'meta_tags': meta_tags,
            'schema': {
                'present': schema_present,
                'project_schema': project_schema,
                'person_schema': person_schema
            }
        }

    def _analyze_performance(self, html_content: str) -> Dict:
        """Analyze performance-related elements"""

        # Count external resources
        soup = BeautifulSoup(html_content, 'html.parser')

        external_scripts = len([
            script for script in soup.find_all('script', src=True)
            if script['src'].startswith('http')
        ])

        external_stylesheets = len([
            link for link in soup.find_all('link', rel='stylesheet')
            if link.get('href', '').startswith('http')
        ])

        # Check for optimization elements
        has_defer_js = any(script.get('defer') for script in soup.find_all('script'))
        has_async_js = any(script.get('async') for script in soup.find_all('script'))

        inline_css = len(soup.find_all('style'))
        inline_js = len(soup.find_all('script', string=True))

        # Image optimization
        images = soup.find_all('img')
        responsive_images = any(img.get('srcset') for img in images)
        lazy_loading = any(img.get('loading') == 'lazy' for img in images)

        return {
            'external_resources': {
                'scripts': external_scripts,
                'stylesheets': external_stylesheets,
                'total': external_scripts + external_stylesheets
            },
            'optimization': {
                'defer_js': has_defer_js,
                'async_js': has_async_js,
                'inline_css': inline_css,
                'inline_js': inline_js
            },
            'images': {
                'total': len(images),
                'responsive': responsive_images,
                'lazy_loading': lazy_loading
            },
            'html_size': len(html_content)
        }

    def _analyze_content(self, soup: BeautifulSoup) -> Dict:
        """Analyze content for SEO optimization"""

        # Extract text content
        text_content = soup.get_text()
        text_lower = text_content.lower()

        # Word count
        word_count = len(text_content.split())

        # Keyword analysis
        tech_keyword_count = sum(
            1 for keyword in self.tech_keywords
            if keyword in text_lower
        )

        recruiter_keyword_count = sum(
            1 for keyword in self.recruiter_keywords
            if keyword in text_lower
        )

        # Check for location keywords (common cities)
        location_keywords = [
            'new york', 'san francisco', 'london', 'remote', 'los angeles',
            'chicago', 'boston', 'seattle', 'austin', 'denver'
        ]

        location_count = sum(
            1 for location in location_keywords
            if location in text_lower
        )

        # Internal links
        internal_links = len([
            a for a in soup.find_all('a', href=True)
            if not a['href'].startswith('http') and a['href'] != '#'
        ])

        # External links
        external_links = len([
            a for a in soup.find_all('a', href=True)
            if a['href'].startswith('http')
        ])

        # Contact information
        contact_methods = []
        if '@' in text_content:
            contact_methods.append('email')
        if 'linkedin' in text_lower:
            contact_methods.append('linkedin')
        if 'github' in text_lower:
            contact_methods.append('github')
        if 'twitter' in text_lower:
            contact_methods.append('twitter')

        return {
            'content_length': {
                'words': word_count,
                'characters': len(text_content)
            },
            'keywords': {
                'tech_count': tech_keyword_count,
                'recruiter_count': recruiter_keyword_count,
                'location_count': location_count,
                'tech_keywords_found': [
                    kw for kw in self.tech_keywords if kw in text_lower
                ],
                'recruiter_keywords_found': [
                    kw for kw in self.recruiter_keywords if kw in text_lower
                ]
            },
            'links': {
                'internal': internal_links,
                'external': external_links
            },
            'contact_methods': contact_methods
        }

    def _calculate_score(self, technical_seo: Dict, performance: Dict, content: Dict) -> int:
        """Calculate overall SEO score"""

        score = 0
        max_score = 100

        # Technical SEO (40 points)
        if technical_seo['title']['optimized']:
            score += 8
        if technical_seo['meta_description']['optimized']:
            score += 8
        if technical_seo['h1_proper']:
            score += 6
        score += min(8, technical_seo['images']['alt_coverage'] / 12.5)  # Max 8 points for alt text

        meta_tags = technical_seo['meta_tags']
        score += sum([
            2 for tag, present in meta_tags.items()
            if present and tag != 'robots'  # robots is optional
        ])

        # Performance (30 points)
        perf = performance['external_resources']
        if perf['total'] <= 10:
            score += 10
        elif perf['total'] <= 20:
            score += 5

        if performance['optimization']['defer_js'] or performance['optimization']['async_js']:
            score += 10

        if performance['images']['responsive'] or performance['images']['lazy_loading']:
            score += 5

        if performance['html_size'] < 100000:  # Less than 100KB
            score += 5

        # Content (30 points)
        if content['content_length']['words'] >= 300:
            score += 10
        elif content['content_length']['words'] >= 150:
            score += 5

        if content['keywords']['tech_count'] >= 3:
            score += 10
        elif content['keywords']['tech_count'] >= 1:
            score += 5

        if content['keywords']['recruiter_count'] >= 2:
            score += 5

        if content['links']['internal'] >= 3:
            score += 3

        if len(content['contact_methods']) >= 2:
            score += 2

        return min(score, max_score)

    def _identify_issues(self, technical_seo: Dict, performance: Dict, content: Dict) -> List[Dict]:
        """Identify SEO issues"""

        issues = []

        # Technical SEO issues
        if not technical_seo['title']['present']:
            issues.append({
                'type': 'critical',
                'category': 'technical',
                'message': 'Missing title tag',
                'impact': 'High - Title tags are essential for SEO'
            })
        elif not technical_seo['title']['optimized']:
            issues.append({
                'type': 'high',
                'category': 'technical',
                'message': f'Title tag not optimized (length: {technical_seo["title"]["length"]})',
                'impact': 'Medium - Titles should be 50-60 characters and contain developer keywords'
            })

        if not technical_seo['meta_description']['present']:
            issues.append({
                'type': 'critical',
                'category': 'technical',
                'message': 'Missing meta description',
                'impact': 'High - Meta descriptions improve click-through rates'
            })
        elif not technical_seo['meta_description']['optimized']:
            issues.append({
                'type': 'high',
                'category': 'technical',
                'message': f'Meta description not optimized (length: {technical_seo["meta_description"]["length"]})',
                'impact': 'Medium - Descriptions should be 120-160 characters'
            })

        if not technical_seo['h1_proper']:
            issues.append({
                'type': 'high',
                'category': 'technical',
                'message': f'Improper H1 usage (found {technical_seo["headings"]["h1"]} H1 tags)',
                'impact': 'Medium - Pages should have exactly one H1 tag'
            })

        if technical_seo['images']['alt_coverage'] < 80:
            issues.append({
                'type': 'medium',
                'category': 'technical',
                'message': f'Low alt text coverage ({technical_seo["images"]["alt_coverage"]:.1f}%)',
                'impact': 'Medium - Alt text improves accessibility and image search'
            })

        # Performance issues
        if performance['external_resources']['total'] > 20:
            issues.append({
                'type': 'medium',
                'category': 'performance',
                'message': f'Too many external resources ({performance["external_resources"]["total"]})',
                'impact': 'Medium - Consider optimizing resource loading'
            })

        if performance['html_size'] > 200000:
            issues.append({
                'type': 'medium',
                'category': 'performance',
                'message': 'Large HTML file size',
                'impact': 'Medium - Consider optimizing HTML size'
            })

        # Content issues
        if content['content_length']['words'] < 150:
            issues.append({
                'type': 'high',
                'category': 'content',
                'message': f'Low content length ({content["content_length"]["words"]} words)',
                'impact': 'Medium - Pages should have at least 150 words'
            })

        if content['keywords']['tech_count'] == 0:
            issues.append({
                'type': 'high',
                'category': 'content',
                'message': 'No technical keywords found',
                'impact': 'High - Include your technical skills and technologies'
            })

        if content['keywords']['recruiter_count'] == 0:
            issues.append({
                'type': 'medium',
                'category': 'content',
                'message': 'No recruiter-friendly keywords found',
                'impact': 'Medium - Include terms like "developer", "engineer", etc.'
            })

        if len(content['contact_methods']) < 2:
            issues.append({
                'type': 'high',
                'category': 'content',
                'message': 'Limited contact methods available',
                'impact': 'High - Make it easy for recruiters to contact you'
            })

        return issues

    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on issues"""

        recommendations = []

        # Group issues by category
        critical_issues = [i for i in issues if i['type'] == 'critical']
        high_issues = [i for i in issues if i['type'] == 'high']
        medium_issues = [i for i in issues if i['type'] == 'medium']

        if critical_issues:
            recommendations.append("🚨 CRITICAL ISSUES TO FIX:")
            for issue in critical_issues:
                recommendations.append(f"  • {issue['message']}")

        if high_issues:
            recommendations.append("\n⚠️  HIGH PRIORITY IMPROVEMENTS:")
            for issue in high_issues:
                recommendations.append(f"  • {issue['message']}")

        if medium_issues:
            recommendations.append("\n📈 MEDIUM PRIORITY OPTIMIZATIONS:")
            for issue in medium_issues:
                recommendations.append(f"  • {issue['message']}")

        # Add general recommendations
        general_recs = [
            "\n🎯 SEO BEST PRACTICES:",
            "  • Add your target location to attract local opportunities",
            "  • Include specific technologies you want to work with",
            "  • Optimize project pages with detailed descriptions",
            "  • Create internal links between related projects",
            "  • Add structured data for projects and skills",
            "  • Ensure mobile responsiveness for better rankings",
            "  • Regularly update content with recent projects"
        ]

        recommendations.extend(general_recs)

        return recommendations

    def _create_error_result(self, error_message: str) -> SEOAuditResult:
        """Create error result when audit fails"""
        return SEOAuditResult(
            score=0,
            issues=[{
                'type': 'critical',
                'category': 'error',
                'message': error_message,
                'impact': 'Unable to perform SEO audit'
            }],
            recommendations=[f"Fix the error: {error_message}"],
            technical_seo={},
            performance={},
            content_optimization={}
        )

    def generate_audit_report(self, result: SEOAuditResult) -> str:
        """Generate a comprehensive audit report"""

        report = []
        report.append("=" * 60)
        report.append("🔍 SEO AUDIT REPORT FOR DEVELOPER PORTFOLIO")
        report.append("=" * 60)

        # Overall Score
        report.append(f"\n📊 OVERALL SEO SCORE: {result.score}/100")

        if result.score >= 90:
            grade = "A+ (Excellent)"
        elif result.score >= 80:
            grade = "A (Very Good)"
        elif result.score >= 70:
            grade = "B (Good)"
        elif result.score >= 60:
            grade = "C (Fair)"
        else:
            grade = "D (Needs Improvement)"

        report.append(f"Grade: {grade}")

        # Technical SEO Section
        report.append("\n🔧 TECHNICAL SEO ANALYSIS")
        report.append("-" * 30)

        if result.technical_seo.get('title'):
            title_info = result.technical_seo['title']
            report.append(f"Title Tag: {'✅' if title_info['optimized'] else '❌'} "
                          f"({title_info['length']} chars)")
            if title_info['content']:
                report.append(f"  Content: {title_info['content'][:60]}...")

        if result.technical_seo.get('meta_description'):
            desc_info = result.technical_seo['meta_description']
            report.append(f"Meta Description: {'✅' if desc_info['optimized'] else '❌'} "
                          f"({desc_info['length']} chars)")
            if desc_info['content']:
                report.append(f"  Content: {desc_info['content'][:80]}...")

        if result.technical_seo.get('h1_proper') is not None:
            report.append(f"H1 Tags: {'✅' if result.technical_seo['h1_proper'] else '❌'}")

        if result.technical_seo.get('images'):
            img_info = result.technical_seo['images']
            report.append(f"Image Alt Text: {img_info['alt_coverage']:.1f}% coverage "
                          f"({img_info['with_alt']}/{img_info['total']})")

        # Performance Section
        report.append("\n⚡ PERFORMANCE ANALYSIS")
        report.append("-" * 25)

        if result.performance.get('external_resources'):
            resources = result.performance['external_resources']['total']
            report.append(f"External Resources: {resources} "
                          f"{'✅' if resources <= 10 else '⚠️' if resources <= 20 else '❌'}")

        # Content Section
        report.append("\n📝 CONTENT OPTIMIZATION")
        report.append("-" * 28)

        if result.content_optimization.get('content_length'):
            word_count = result.content_optimization['content_length']['words']
            report.append(f"Content Length: {word_count} words "
                          f"{'✅' if word_count >= 300 else '⚠️' if word_count >= 150 else '❌'}")

        if result.content_optimization.get('keywords'):
            keywords = result.content_optimization['keywords']
            report.append(f"Technical Keywords: {keywords['tech_count']} found")
            report.append(f"Recruiter Keywords: {keywords['recruiter_count']} found")
            report.append(f"Location Keywords: {keywords['location_count']} found")

        # Issues and Recommendations
        if result.issues:
            report.append("\n🚨 ISSUES FOUND")
            report.append("-" * 17)

            critical_issues = [i for i in result.issues if i['type'] == 'critical']
            high_issues = [i for i in result.issues if i['type'] == 'high']
            medium_issues = [i for i in result.issues if i['type'] == 'medium']

            if critical_issues:
                report.append("\nCRITICAL:")
                for issue in critical_issues:
                    report.append(f"  • {issue['message']}")

            if high_issues:
                report.append("\nHIGH:")
                for issue in high_issues:
                    report.append(f"  • {issue['message']}")

            if medium_issues:
                report.append("\nMEDIUM:")
                for issue in medium_issues:
                    report.append(f"  • {issue['message']}")

        # Recommendations
        report.append("\n💡 RECOMMENDATIONS")
        report.append("-" * 20)
        for recommendation in result.recommendations:
            report.append(recommendation)

        return "\n".join(report)


def main():
    """Example usage of the SEO auditor"""

    # Example HTML content (in real usage, you'd fetch this from a URL)
    example_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>John Doe - Developer</title>
        <meta name="description" content="My portfolio">
    </head>
    <body>
        <h1>John Doe</h1>
        <h2>About Me</h2>
        <p>I am a software developer with experience in React and Node.js.</p>
        <img src="profile.jpg" alt="Profile picture">
        <img src="project1.jpg">
    </body>
    </html>
    """

    auditor = SEOAuditor()
    result = auditor.audit_portfolio("https://example.com", example_html)

    report = auditor.generate_audit_report(result)
    print(report)


if __name__ == "__main__":
    main()