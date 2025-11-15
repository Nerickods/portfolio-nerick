#!/usr/bin/env python3
"""
Performance Monitor for Developer Portfolios
Real-time Core Web Vitals monitoring and performance regression detection
"""

import json
import os
import sys
import argparse
import time
import threading
import requests
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclasses, asdict
import subprocess
import signal

@dataclasses.dataclass
class CoreWebVitals:
    """Core Web Vitals metrics"""
    lcp: float  # Largest Contentful Paint
    fid: float  # First Input Delay
    cls: float  # Cumulative Layout Shift
    fcp: float  # First Contentful Paint
    ttfb: float  # Time to First Byte
    inp: float  # Interaction to Next Paint

@dataclasses.dataclass
class PerformanceSnapshot:
    """Performance snapshot at a point in time"""
    timestamp: datetime
    url: str
    core_web_vitals: CoreWebVitals
    lighthouse_score: float
    bundle_size: int
    total_requests: int
    user_agent: str
    connection_type: str

@dataclasses.dataclass
class PerformanceAlert:
    """Performance alert configuration"""
    metric: str
    threshold: float
    condition: str  # 'greater_than', 'less_than'
    severity: str  # 'warning', 'error', 'critical'
    enabled: bool

class PerformanceMonitor:
    """Main performance monitoring class"""

    def __init__(self, project_path: str, output_dir: str = "./monitoring"):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Monitoring configuration
        self.monitoring_active = False
        self.monitoring_thread = None
        self.data_file = self.output_dir / "performance_data.json"
        self.alerts_file = self.output_dir / "alerts.json"

        # Default performance thresholds (portfolio-specific)
        self.thresholds = {
            'lcp': 2500,  # 2.5s
            'fid': 100,   # 100ms
            'cls': 0.1,   # 0.1
            'fcp': 1000,  # 1.0s
            'ttfb': 600,  # 600ms
            'inp': 200,   # 200ms
            'lighthouse_score': 90,  # 90+
            'bundle_size': 250 * 1024,  # 250KB
            'total_requests': 50
        }

        # Performance alerts
        self.alerts = self.initialize_alerts()

        # Performance history
        self.performance_history: List[PerformanceSnapshot] = []
        self.load_history()

    def initialize_alerts(self) -> List[PerformanceAlert]:
        """Initialize default performance alerts"""
        alerts = [
            PerformanceAlert('lcp', 2500, 'greater_than', 'warning', True),
            PerformanceAlert('fid', 100, 'greater_than', 'warning', True),
            PerformanceAlert('cls', 0.1, 'greater_than', 'warning', True),
            PerformanceAlert('fcp', 1000, 'greater_than', 'warning', True),
            PerformanceAlert('ttfb', 600, 'greater_than', 'warning', True),
            PerformanceAlert('lighthouse_score', 90, 'less_than', 'error', True),
            PerformanceAlert('bundle_size', 250 * 1024, 'greater_than', 'warning', True),
            PerformanceAlert('total_requests', 50, 'greater_than', 'warning', True),
        ]

        # Load custom alerts if file exists
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r') as f:
                    custom_alerts_data = json.load(f)
                    # Convert JSON data to PerformanceAlert objects
                    custom_alerts = [
                        PerformanceAlert(**alert_data) for alert_data in custom_alerts_data
                    ]
                    alerts.extend(custom_alerts)
            except Exception as e:
                print(f"⚠️ Could not load custom alerts: {e}")

        return alerts

    def load_history(self):
        """Load performance history from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for snapshot_data in data:
                        snapshot = PerformanceSnapshot(
                            timestamp=datetime.fromisoformat(snapshot_data['timestamp']),
                            url=snapshot_data['url'],
                            core_web_vitals=CoreWebVitals(**snapshot_data['core_web_vitals']),
                            lighthouse_score=snapshot_data['lighthouse_score'],
                            bundle_size=snapshot_data['bundle_size'],
                            total_requests=snapshot_data['total_requests'],
                            user_agent=snapshot_data['user_agent'],
                            connection_type=snapshot_data['connection_type']
                        )
                        self.performance_history.append(snapshot)
                print(f"📊 Loaded {len(self.performance_history) historical data points")
            except Exception as e:
                print(f"⚠️ Could not load performance history: {e}")

    def save_history(self):
        """Save performance history to file"""
        try:
            data = [asdict(snapshot) for snapshot in self.performance_history]
            # Convert datetime objects to strings
            for item in data:
                item['timestamp'] = item['timestamp'].isoformat()
                item['core_web_vitals'] = asdict(item['core_web_vitals'])

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save performance history: {e}")

    def run_lighthouse_audit(self, url: str) -> Dict[str, Any]:
        """Run Lighthouse audit and return results"""
        try:
            # Check if lighthouse is installed
            subprocess.run(['lighthouse', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Lighthouse not found. Installing...")
            subprocess.run(['npm', 'install', '-g', 'lighthouse'], check=True)

        # Run Lighthouse audit
        cmd = [
            'lighthouse', url,
            '--output=json',
            '--output-path=/tmp/lighthouse_monitor.json',
            '--chrome-flags="--headless"',
            '--quiet',
            '--only-categories=performance'
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)

            with open('/tmp/lighthouse_monitor.json', 'r') as f:
                return json.load(f)

        except subprocess.CalledProcessError as e:
            print(f"❌ Lighthouse audit failed: {e}")
            return {}

    def extract_core_web_vitals(self, lighthouse_data: Dict[str, Any]) -> CoreWebVitals:
        """Extract Core Web Vitals from Lighthouse data"""
        audits = lighthouse_data.get('audits', {})

        return CoreWebVitals(
            lcp=audits.get('largest-contentful-paint', {}).get('numericValue', 0),
            fid=audits.get('max-potential-fid', {}).get('numericValue', 0),
            cls=audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
            fcp=audits.get('first-contentful-paint', {}).get('numericValue', 0),
            ttfb=audits.get('server-response-time', {}).get('numericValue', 0),
            inp=audits.get('interaction-to-next-paint', {}).get('numericValue', 0)
        )

    def get_bundle_metrics(self) -> tuple[int, int]:
        """Get current bundle size and request count"""
        try:
            # Check Next.js build output
            next_dir = self.project_path / '.next'
            total_size = 0
            total_requests = 0

            if next_dir.exists():
                for chunk_file in next_dir.rglob('*.js'):
                    total_size += chunk_file.stat().st_size
                    total_requests += 1

            return total_size, total_requests
        except:
            return 0, 0

    def collect_metrics(self, url: str) -> Optional[PerformanceSnapshot]:
        """Collect current performance metrics"""
        print(f"🔍 Collecting metrics for {url}")

        try:
            # Run Lighthouse audit
            lighthouse_data = self.run_lighthouse_audit(url)

            if not lighthouse_data:
                print("❌ Failed to collect Lighthouse data")
                return None

            # Extract metrics
            core_web_vitals = self.extract_core_web_vitals(lighthouse_data)
            lighthouse_score = lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0) * 100

            # Get bundle metrics
            bundle_size, total_requests = self.get_bundle_metrics()

            # Create snapshot
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now(),
                url=url,
                core_web_vitals=core_web_vitals,
                lighthouse_score=lighthouse_score,
                bundle_size=bundle_size,
                total_requests=total_requests,
                user_agent="Portfolio Monitor",
                connection_type="unknown"
            )

            return snapshot

        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            return None

    def check_alerts(self, snapshot: PerformanceSnapshot) -> List[str]:
        """Check if any alerts are triggered"""
        triggered_alerts = []

        metrics = {
            'lcp': snapshot.core_web_vitals.lcp,
            'fid': snapshot.core_web_vitals.fid,
            'cls': snapshot.core_web_vitals.cls,
            'fcp': snapshot.core_web_vitals.fcp,
            'ttfb': snapshot.core_web_vitals.ttfb,
            'inp': snapshot.core_web_vitals.inp,
            'lighthouse_score': snapshot.lighthouse_score,
            'bundle_size': snapshot.bundle_size,
            'total_requests': snapshot.total_requests
        }

        for alert in self.alerts:
            if not alert.enabled:
                continue

            metric_value = metrics.get(alert.metric)
            if metric_value is None:
                continue

            triggered = False
            if alert.condition == 'greater_than' and metric_value > alert.threshold:
                triggered = True
            elif alert.condition == 'less_than' and metric_value < alert.threshold:
                triggered = True

            if triggered:
                alert_msg = f"🚨 {alert.severity.upper()}: {alert.metric.upper()} = {metric_value} (threshold: {alert.threshold})"
                triggered_alerts.append(alert_msg)

        return triggered_alerts

    def detect_regressions(self, snapshot: PerformanceSnapshot) -> List[str]:
        """Detect performance regressions compared to historical data"""
        regressions = []

        if len(self.performance_history) < 5:
            return regressions  # Not enough data for comparison

        # Calculate historical averages (last 10 snapshots)
        recent_history = self.performance_history[-10:]

        metrics_to_check = ['lcp', 'fid', 'cls', 'fcp', 'ttfb']
        regression_threshold = 0.2  # 20% degradation

        for metric in metrics_to_check:
            current_value = getattr(snapshot.core_web_vitals, metric)
            historical_values = [getattr(s.core_web_vitals, metric) for s in recent_history]

            if not historical_values or current_value == 0:
                continue

            historical_avg = statistics.mean(historical_values)
            if historical_avg == 0:
                continue

            percent_change = (current_value - historical_avg) / historical_avg

            if percent_change > regression_threshold:
                regressions.append(
                    f"📉 Performance regression detected: {metric.upper()} "
                    f"increased by {percent_change*100:.1f}% "
                    f"(current: {current_value:.1f}, historical avg: {historical_avg:.1f})"
                )

        return regressions

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate data for performance dashboard"""
        if not self.performance_history:
            return {}

        # Get recent data (last 24 hours or last 50 snapshots)
        recent_data = self.performance_history[-50:]

        # Calculate averages
        avg_lcp = statistics.mean([s.core_web_vitals.lcp for s in recent_data if s.core_web_vitals.lcp > 0])
        avg_fid = statistics.mean([s.core_web_vitals.fid for s in recent_data if s.core_web_vitals.fid > 0])
        avg_cls = statistics.mean([s.core_web_vitals.cls for s in recent_data if s.core_web_vitals.cls > 0])
        avg_score = statistics.mean([s.lighthouse_score for s in recent_data])

        # Performance trend (last 10 vs previous 10)
        if len(recent_data) >= 20:
            recent_10 = recent_data[-10:]
            previous_10 = recent_data[-20:-10]

            recent_avg = statistics.mean([s.lighthouse_score for s in recent_10])
            previous_avg = statistics.mean([s.lighthouse_score for s in previous_10])
            trend = recent_avg - previous_avg
        else:
            trend = 0

        return {
            'current_metrics': {
                'lcp': recent_data[-1].core_web_vitals.lcp if recent_data else 0,
                'fid': recent_data[-1].core_web_vitals.fid if recent_data else 0,
                'cls': recent_data[-1].core_web_vitals.cls if recent_data else 0,
                'lighthouse_score': recent_data[-1].lighthouse_score if recent_data else 0,
            },
            'averages': {
                'lcp': avg_lcp,
                'fid': avg_fid,
                'cls': avg_cls,
                'lighthouse_score': avg_score,
            },
            'trend': trend,
            'total_snapshots': len(self.performance_history),
            'last_updated': recent_data[-1].timestamp.isoformat() if recent_data else None,
        }

    def monitoring_loop(self, url: str, interval: int = 300):  # 5 minutes default
        """Main monitoring loop"""
        print(f"🚀 Starting performance monitoring for {url}")
        print(f"📊 Collecting metrics every {interval} seconds")

        while self.monitoring_active:
            try:
                # Collect metrics
                snapshot = self.collect_metrics(url)

                if snapshot:
                    # Add to history
                    self.performance_history.append(snapshot)

                    # Check alerts
                    alerts = self.check_alerts(snapshot)
                    if alerts:
                        for alert in alerts:
                            print(alert)

                    # Check regressions
                    regressions = self.detect_regressions(snapshot)
                    if regressions:
                        for regression in regressions:
                            print(regression)

                    # Save history
                    self.save_history()

                    # Print summary
                    print(f"✅ {snapshot.timestamp.strftime('%H:%M:%S')} - "
                          f"Lighthouse: {snapshot.lighthouse_score:.0f}, "
                          f"LCP: {snapshot.core_web_vitals.lcp:.0f}ms, "
                          f"FID: {snapshot.core_web_vitals.fid:.0f}ms")

            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")

            # Wait for next interval
            time.sleep(interval)

    def start_monitoring(self, url: str, interval: int = 300):
        """Start performance monitoring"""
        if self.monitoring_active:
            print("⚠️ Monitoring is already active")
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self.monitoring_loop,
            args=(url, interval),
            daemon=True
        )
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring_active:
            print("⚠️ Monitoring is not active")
            return

        print("⏹️ Stopping performance monitoring...")
        self.monitoring_active = False

        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

        print("✅ Monitoring stopped")

    def generate_report(self) -> str:
        """Generate performance monitoring report"""
        if not self.performance_history:
            return "No performance data available"

        dashboard_data = self.generate_dashboard_data()
        report = []

        report.append("# Performance Monitoring Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Current Metrics
        current = dashboard_data.get('current_metrics', {})
        report.append("## 📊 Current Metrics")
        report.append(f"**Lighthouse Score:** {current.get('lighthouse_score', 0):.0f}")
        report.append(f"**Largest Contentful Paint:** {current.get('lcp', 0):.0f}ms")
        report.append(f"**First Input Delay:** {current.get('fid', 0):.0f}ms")
        report.append(f"**Cumulative Layout Shift:** {current.get('cls', 0):.3f}")
        report.append("")

        # Averages
        averages = dashboard_data.get('averages', {})
        report.append("## 📈 Performance Averages")
        report.append(f"**Lighthouse Score:** {averages.get('lighthouse_score', 0):.1f}")
        report.append(f"**Largest Contentful Paint:** {averages.get('lcp', 0):.0f}ms")
        report.append(f"**First Input Delay:** {averages.get('fid', 0):.0f}ms")
        report.append(f"**Cumulative Layout Shift:** {averages.get('cls', 0):.3f}")
        report.append("")

        # Trend
        trend = dashboard_data.get('trend', 0)
        trend_emoji = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
        report.append(f"## {trend_emoji} Performance Trend")
        report.append(f"**Change:** {trend:+.1f} points")
        report.append("")

        # Recent alerts
        recent_snapshot = self.performance_history[-1] if self.performance_history else None
        if recent_snapshot:
            recent_alerts = self.check_alerts(recent_snapshot)
            if recent_alerts:
                report.append("## 🚨 Recent Alerts")
                for alert in recent_alerts:
                    report.append(f"- {alert}")
                report.append("")

        # Summary
        report.append("## 📋 Summary")
        report.append(f"**Total Snapshots:** {dashboard_data.get('total_snapshots', 0)}")
        report.append(f"**Monitoring Period:** {len(self.performance_history)} data points")
        report.append(f"**Last Updated:** {dashboard_data.get('last_updated', 'Never')}")

        return "\n".join(report)

    def export_data(self, format: str = 'json') -> str:
        """Export monitoring data"""
        if format == 'json':
            return json.dumps([asdict(s) for s in self.performance_history], indent=2, default=str)
        elif format == 'csv':
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)

            # Header
            writer.writerow([
                'timestamp', 'url', 'lcp', 'fid', 'cls', 'fcp', 'ttfb', 'inp',
                'lighthouse_score', 'bundle_size', 'total_requests'
            ])

            # Data rows
            for snapshot in self.performance_history:
                writer.writerow([
                    snapshot.timestamp.isoformat(),
                    snapshot.url,
                    snapshot.core_web_vitals.lcp,
                    snapshot.core_web_vitals.fid,
                    snapshot.core_web_vitals.cls,
                    snapshot.core_web_vitals.fcp,
                    snapshot.core_web_vitals.ttfb,
                    snapshot.core_web_vitals.inp,
                    snapshot.lighthouse_score,
                    snapshot.bundle_size,
                    snapshot.total_requests
                ])

            return output.getvalue()

        return ""

def signal_handler(signum, frame, monitor):
    """Handle shutdown signals"""
    print("\n⏹️ Shutting down performance monitor...")
    monitor.stop_monitoring()
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Performance Monitor for Developer Portfolios')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--url', help='Portfolio URL to monitor')
    parser.add_argument('--interval', type=int, default=300, help='Monitoring interval in seconds')
    parser.add_argument('--output', default='./monitoring', help='Output directory for monitoring data')
    parser.add_argument('--watch', action='store_true', help='Start continuous monitoring')
    parser.add_argument('--report', help='Generate monitoring report and save to file')
    parser.add_argument('--export', choices=['json', 'csv'], help='Export monitoring data')
    parser.add_argument('--dashboard', action='store_true', help='Generate dashboard data')

    args = parser.parse_args()

    # Initialize monitor
    monitor = PerformanceMonitor(args.project_path, args.output)

    # Set up signal handlers
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, monitor))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, monitor))

    if args.watch:
        if not args.url:
            print("❌ URL is required for continuous monitoring")
            sys.exit(1)

        # Start continuous monitoring
        monitor.start_monitoring(args.url, args.interval)

        try:
            # Keep the main thread alive
            while monitor.monitoring_active:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()

    elif args.report:
        # Generate and save report
        report = monitor.generate_report()

        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.report}")
        else:
            print(report)

    elif args.export:
        # Export data
        data = monitor.export_data(args.export)

        if data:
            export_file = monitor.output_dir / f"performance_data.{args.export}"
            export_file.write_text(data, encoding='utf-8')
            print(f"📊 Data exported to: {export_file}")

    elif args.dashboard:
        # Generate dashboard data
        dashboard_data = monitor.generate_dashboard_data()
        print(json.dumps(dashboard_data, indent=2, default=str))

    else:
        print("Use --watch to start monitoring, --report to generate report, or --export to export data")

if __name__ == "__main__":
    main()