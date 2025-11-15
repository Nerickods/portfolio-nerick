# Performance Monitoring Strategies for Developer Portfolios

## Overview

Effective performance monitoring is essential for maintaining optimal portfolio performance over time. This guide covers comprehensive monitoring strategies specifically designed for developer portfolios, from real-time user monitoring to automated alerting systems.

## Monitoring Framework

### Types of Performance Monitoring

1. **Real User Monitoring (RUM)**: Actual user experience data
2. **Synthetic Monitoring**: Automated testing from multiple locations
3. **Continuous Integration Testing**: Automated performance checks in CI/CD
4. **Production Monitoring**: Real-time performance tracking in production
5. **Performance Budget Enforcement**: Automated budget violation detection

### Key Performance Indicators (KPIs)

```javascript
// lib/monitoring/kpis.js
export const portfolioKPIs = {
  // Core Web Vitals
  coreWebVitals: {
    LCP: { target: 2500, warning: 2000, critical: 4000 },
    FID: { target: 100, warning: 80, critical: 300 },
    CLS: { target: 0.1, warning: 0.05, critical: 0.25 },
    INP: { target: 200, warning: 150, critical: 500 }
  },

  // Additional metrics
  performance: {
    FCP: { target: 1000, warning: 800, critical: 1800 },
    TTFB: { target: 600, warning: 400, critical: 1000 },
    SpeedIndex: { target: 1500, warning: 1200, critical: 3000 },
    TTI: { target: 3000, warning: 2000, critical: 5000 }
  },

  // Resource metrics
  resources: {
    bundleSize: { target: 250000, warning: 200000, critical: 500000 }, // bytes
    imageCount: { target: 20, warning: 15, critical: 30 },
    scriptCount: { target: 15, warning: 12, critical: 25 },
    totalRequests: { target: 50, warning: 40, critical: 75 }
  },

  // Business metrics
  business: {
    bounceRate: { target: 40, warning: 50, critical: 70 }, // percentage
    avgSessionDuration: { target: 120, warning: 90, critical: 60 }, // seconds
    conversionRate: { target: 5, warning: 3, critical: 1 } // percentage
  }
}
```

## Real User Monitoring (RUM)

### Web Vitals Collection

```javascript
// lib/monitoring/rum.js
import { getCLS, getFID, getFCP, getLCP, getTTFB, getINP } from 'web-vitals'

class RealUserMonitoring {
  constructor(apiEndpoint = '/api/analytics') {
    this.apiEndpoint = apiEndpoint
    this.queue = []
    this.sessionId = this.generateSessionId()
    this.init()
  }

  generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2)
  }

  init() {
    // Collect Core Web Vitals
    getCLS((metric) => this.sendMetric(metric))
    getFID((metric) => this.sendMetric(metric))
    getFCP((metric) => this.sendMetric(metric))
    getLCP((metric) => this.sendMetric(metric))
    getTTFB((metric) => this.sendMetric(metric))
    getINP((metric) => this.sendMetric(metric))

    // Monitor route changes
    if (typeof window !== 'undefined') {
      this.observeNavigation()

      // Monitor page visibility changes
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          this.trackPageView()
        }
      })
    }
  }

  observeNavigation() {
    let currentUrl = window.location.pathname

    // Simple SPA navigation detection
    const originalPushState = history.pushState
    history.pushState = function(...args) {
      originalPushState.apply(this, args)
      setTimeout(() => {
        if (window.location.pathname !== currentUrl) {
          currentUrl = window.location.pathname
          window.dispatchEvent(new Event('routechange'))
        }
      }, 0)
    }
  }

  async sendMetric(metric) {
    const payload = {
      ...metric,
      sessionId: this.sessionId,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: Date.now(),
      connection: this.getConnectionInfo(),
      device: this.getDeviceInfo()
    }

    try {
      await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    } catch (error) {
      // Queue for retry
      this.queue.push(payload)
      if (this.queue.length > 10) {
        this.queue.shift()
      }
    }
  }

  getConnectionInfo() {
    if ('connection' in navigator) {
      const conn = navigator.connection
      return {
        effectiveType: conn.effectiveType,
        downlink: conn.downlink,
        rtt: conn.rtt
      }
    }
    return null
  }

  getDeviceInfo() {
    return {
      width: window.screen.width,
      height: window.screen.height,
      pixelRatio: window.devicePixelRatio,
      memory: navigator.deviceMemory,
      hardwareConcurrency: navigator.hardwareConcurrency
    }
  }

  trackPageView() {
    this.sendMetric({
      name: 'pageView',
      value: 1,
      id: `page-${Date.now()}`
    })
  }

  // Send queued metrics when online
  flushQueue() {
    while (this.queue.length > 0) {
      const metric = this.queue.shift()
      this.sendMetric(metric)
    }
  }
}

// Initialize RUM
export const rum = new RealUserMonitoring()

// Handle connection state changes
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => rum.flushQueue())
}
```

### Advanced RUM Features

```javascript
// lib/monitoring/advancedRum.js
export class AdvancedRUM extends RealUserMonitoring {
  constructor(apiEndpoint) {
    super(apiEndpoint)
    this.observeLongTasks()
    this.observeResourceTiming()
    this.trackUserInteractions()
  }

  observeLongTasks() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          this.sendMetric({
            name: 'long-task',
            value: entry.duration,
            id: `long-task-${Date.now()}`,
            startTime: entry.startTime,
            attribution: entry.attribution
          })
        })
      })

      observer.observe({ entryTypes: ['longtask'] })
    }
  }

  observeResourceTiming() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.duration > 1000) { // Only log slow resources
            this.sendMetric({
              name: 'slow-resource',
              value: entry.duration,
              id: `resource-${entry.name}`,
              resourceType: this.getResourceType(entry.name),
              size: entry.transferSize,
              url: entry.name
            })
          }
        })
      })

      observer.observe({ entryTypes: ['resource'] })
    }
  }

  getResourceType(url) {
    if (url.match(/\.(js|jsx|ts|tsx)$/)) return 'script'
    if (url.match(/\.css$/)) return 'stylesheet'
    if (url.match(/\.(png|jpg|jpeg|gif|webp|avif|svg)$/)) return 'image'
    if (url.match(/\.(woff|woff2|ttf|otf)$/)) return 'font'
    return 'other'
  }

  trackUserInteractions() {
    const interactionTypes = ['click', 'keydown', 'scroll']
    let lastInteraction = Date.now()

    interactionTypes.forEach(type => {
      document.addEventListener(type, (event) => {
        const now = Date.now()
        const timeSinceLastInteraction = now - lastInteraction

        this.sendMetric({
          name: 'user-interaction',
          value: timeSinceLastInteraction,
          id: `interaction-${Date.now()}`,
          type: type,
          target: event.target.tagName
        })

        lastInteraction = now
      }, { passive: true })
    })
  }

  trackCustomEvent(name, value, metadata = {}) {
    this.sendMetric({
      name,
      value,
      id: `custom-${name}-${Date.now()}`,
      ...metadata
    })
  }
}
```

## API Endpoint for Analytics

```javascript
// app/api/analytics/route.js
import { NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { checkPerformanceBudgets } from '@/lib/performanceBudget'

export async function POST(request) {
  try {
    const metric = await request.json()

    // Store raw metric data
    await db.performanceMetric.create({
      data: {
        sessionId: metric.sessionId,
        metricName: metric.name,
        value: metric.value,
        url: metric.url,
        userAgent: metric.userAgent,
        timestamp: new Date(metric.timestamp),
        deviceInfo: metric.device,
        connectionInfo: metric.connection
      }
    })

    // Check for performance issues
    await checkPerformanceIssues(metric)

    // Update real-time metrics
    await updateRealTimeMetrics(metric)

    return NextResponse.json({ success: true })

  } catch (error) {
    console.error('Analytics API error:', error)
    return NextResponse.json(
      { error: 'Failed to store metric' },
      { status: 500 }
    )
  }
}

async function checkPerformanceIssues(metric) {
  const thresholds = {
    'largest-contentful-paint': { warning: 2500, critical: 4000 },
    'first-input-delay': { warning: 100, critical: 300 },
    'cumulative-layout-shift': { warning: 0.1, critical: 0.25 },
    'first-contentful-paint': { warning: 1000, critical: 1800 }
  }

  const threshold = thresholds[metric.name]
  if (!threshold) return

  let severity = null
  if (metric.value > threshold.critical) severity = 'critical'
  else if (metric.value > threshold.warning) severity = 'warning'

  if (severity) {
    await db.performanceAlert.create({
      data: {
        metricName: metric.name,
        value: metric.value,
        threshold: severity === 'critical' ? threshold.critical : threshold.warning,
        severity,
        url: metric.url,
        timestamp: new Date()
      }
    })

    // Send notification
    await sendPerformanceAlert(metric, severity)
  }
}

async function sendPerformanceAlert(metric, severity) {
  const message = `
🚨 Performance Alert - ${severity.toUpperCase()}

Metric: ${metric.name}
Value: ${metric.value}
URL: ${metric.url}
Time: ${new Date(metric.timestamp).toISOString()}

View details: ${process.env.NEXT_PUBLIC_APP_URL}/performance-dashboard
  `.trim()

  // Send to Slack
  if (process.env.SLACK_WEBHOOK_URL) {
    await fetch(process.env.SLACK_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: message })
    })
  }

  // Send email (implement your email service)
  // await sendEmailAlert(message)
}
```

## Synthetic Monitoring

### Automated Performance Testing

```javascript
// scripts/syntheticMonitoring.js
const puppeteer = require('puppeteer')
const lighthouse = require('lighthouse')
const { URLs } = require('./testConfig')

class SyntheticMonitoring {
  constructor() {
    this.results = []
  }

  async runTests() {
    console.log('🚀 Starting synthetic monitoring...')

    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    })

    try {
      for (const url of URLs) {
        console.log(`Testing ${url}...`)
        const result = await this.testPage(browser, url)
        this.results.push(result)
        await this.delay(5000) // 5 second delay between tests
      }
    } finally {
      await browser.close()
    }

    await this.analyzeResults()
    await this.sendResults()
  }

  async testPage(browser, url) {
    const page = await browser.newPage()

    // Set viewport
    await page.setViewport({ width: 1920, height: 1080 })

    // Enable performance monitoring
    await page.evaluateOnNewDocument(() => {
      window.performanceMetrics = {}
    })

    const startTime = Date.now()

    try {
      // Navigate to page
      const response = await page.goto(url, {
        waitUntil: 'networkidle2',
        timeout: 30000
      })

      // Wait for specific elements
      await page.waitForSelector('h1', { timeout: 10000 })

      // Collect performance metrics
      const metrics = await page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0]
        return {
          loadEventEnd: navigation.loadEventEnd,
          domContentLoaded: navigation.domContentLoadedEventEnd,
          firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
          firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
          largestContentfulPaint: performance.getEntriesByName('largest-contentful-paint')[0]?.startTime
        }
      })

      // Collect bundle information
      const bundleInfo = await this.analyzeBundles(page)

      // Check for layout shifts
      const clsValue = await page.evaluate(() => {
        return new Promise((resolve) => {
          let clsValue = 0
          const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach((entry) => {
              if (!entry.hadRecentInput) {
                clsValue += entry.value
              }
            })
          })
          observer.observe({ entryTypes: ['layout-shift'] })

          setTimeout(() => {
            observer.disconnect()
            resolve(clsValue)
          }, 5000)
        })
      })

      return {
        url,
        timestamp: new Date().toISOString(),
        loadTime: Date.now() - startTime,
        responseCode: response.status(),
        metrics,
        cls: clsValue,
        bundleInfo,
        success: true
      }

    } catch (error) {
      return {
        url,
        timestamp: new Date().toISOString(),
        error: error.message,
        success: false
      }
    } finally {
      await page.close()
    }
  }

  async analyzeBundles(page) {
    return await page.evaluate(() => {
      const scripts = Array.from(document.querySelectorAll('script[src]'))
      const totalSize = scripts.reduce((sum, script) => {
        // Estimate size from script length (approximation)
        return sum + script.textContent.length
      }, 0)

      return {
        scriptCount: scripts.length,
        estimatedSize: totalSize,
        bundles: scripts.map(script => ({
          src: script.src,
          type: script.type || 'text/javascript',
          async: script.async,
          defer: script.defer
        }))
      }
    })
  }

  async analyzeResults() {
    console.log('\n📊 Analyzing results...')

    const successful = this.results.filter(r => r.success)
    const failed = this.results.filter(r => !r.success)

    console.log(`✅ Successful tests: ${successful.length}`)
    console.log(`❌ Failed tests: ${failed.length}`)

    if (successful.length > 0) {
      const avgLoadTime = successful.reduce((sum, r) => sum + r.loadTime, 0) / successful.length
      const avgFCP = successful.reduce((sum, r) => sum + (r.metrics.firstContentfulPaint || 0), 0) / successful.length
      const avgCLS = successful.reduce((sum, r) => sum + (r.cls || 0), 0) / successful.length

      console.log(`📈 Average load time: ${avgLoadTime.toFixed(0)}ms`)
      console.log(`📈 Average FCP: ${avgFCP.toFixed(0)}ms`)
      console.log(`📈 Average CLS: ${avgCLS.toFixed(3)}`)

      // Check for performance regressions
      await this.checkRegressions(successful)
    }

    if (failed.length > 0) {
      console.log('\n❌ Failed tests:')
      failed.forEach(test => {
        console.log(`  ${test.url}: ${test.error}`)
      })
    }
  }

  async checkRegressions(results) {
    // Compare with historical data
    const historical = await this.getHistoricalData()

    if (historical.length > 0) {
      const historicalAvg = historical.reduce((sum, r) => sum + r.loadTime, 0) / historical.length
      const currentAvg = results.reduce((sum, r) => sum + r.loadTime, 0) / results.length

      const regression = (currentAvg - historicalAvg) / historicalAvg

      if (regression > 0.1) { // 10% regression
        console.warn(`⚠️ Performance regression detected: ${(regression * 100).toFixed(1)}% slower`)
        await this.sendRegressionAlert(regression, currentAvg, historicalAvg)
      }
    }

    // Store current results
    await this.storeResults(results)
  }

  async sendResults() {
    if (process.env.SLACK_WEBHOOK_URL) {
      const message = this.formatResultsMessage()
      await fetch(process.env.SLACK_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message })
      })
    }
  }

  formatResultsMessage() {
    const successful = this.results.filter(r => r.success)
    const failed = this.results.filter(r => !r.success)

    return `
🔍 Synthetic Monitoring Report

✅ Successful: ${successful.length}
❌ Failed: ${failed.length}

Performance Summary:
- Avg Load Time: ${successful.length > 0 ? (successful.reduce((sum, r) => sum + r.loadTime, 0) / successful.length).toFixed(0) : 0}ms
- Avg FCP: ${successful.length > 0 ? (successful.reduce((sum, r) => sum + (r.metrics.firstContentfulPaint || 0), 0) / successful.length).toFixed(0) : 0}ms
- Avg CLS: ${successful.length > 0 ? (successful.reduce((sum, r) => sum + (r.cls || 0), 0) / successful.length).toFixed(3) : 0}

${failed.length > 0 ? 'Failed URLs:\n' + failed.map(r => `• ${r.url}: ${r.error}`).join('\n') : ''}
    `.trim()
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// Test configuration
const URLs = [
  'http://localhost:3000',
  'http://localhost:3000/projects',
  'http://localhost:3000/about',
  'http://localhost:3000/contact'
]

// Run monitoring
if (require.main === module) {
  const monitoring = new SyntheticMonitoring()
  monitoring.runTests().catch(console.error)
}

module.exports = SyntheticMonitoring
```

## Performance Dashboard

### Real-Time Dashboard

```jsx
// app/performance-dashboard/page.jsx
import { getPerformanceMetrics } from '@/lib/monitoring'
import { MetricCard } from '@/components/MetricCard'
import { PerformanceChart } from '@/components/PerformanceChart'
import { AlertsPanel } from '@/components/AlertsPanel'

export default async function PerformanceDashboard() {
  const metrics = await getPerformanceMetrics()

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Performance Dashboard
          </h1>
          <div className="flex space-x-4">
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Refresh
            </button>
            <a
              href="/api/performance/export"
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              Export Data
            </a>
          </div>
        </div>

        {/* Core Web Vitals */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Largest Contentful Paint"
            value={metrics.lcp.current}
            target={metrics.lcp.target}
            unit="ms"
            trend={metrics.lcp.trend}
            status={metrics.lcp.status}
          />

          <MetricCard
            title="First Input Delay"
            value={metrics.fid.current}
            target={metrics.fid.target}
            unit="ms"
            trend={metrics.fid.trend}
            status={metrics.fid.status}
          />

          <MetricCard
            title="Cumulative Layout Shift"
            value={metrics.cls.current}
            target={metrics.cls.target}
            unit=""
            trend={metrics.cls.trend}
            status={metrics.cls.status}
          />

          <MetricCard
            title="Bundle Size"
            value={metrics.bundleSize.current}
            target={metrics.bundleSize.target}
            unit="KB"
            trend={metrics.bundleSize.trend}
            status={metrics.bundleSize.status}
          />
        </div>

        {/* Performance Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Performance Trends (24h)</h2>
          <PerformanceChart data={metrics.historical} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Alerts */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
            <AlertsPanel alerts={metrics.recentAlerts} />
          </div>

          {/* Device Performance */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Performance by Device</h2>
            <DevicePerformanceChart data={metrics.devicePerformance} />
          </div>
        </div>

        {/* Geographical Performance */}
        <div className="bg-white rounded-lg shadow p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Geographical Performance</h2>
          <GeoPerformanceMap data={metrics.geoPerformance} />
        </div>
      </div>
    </div>
  )
}
```

### Alert Component

```jsx
// components/AlertsPanel.jsx
'use client'
import { useState, useEffect } from 'react'

export function AlertsPanel({ alerts }) {
  const [expandedAlert, setExpandedAlert] = useState(null)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Fetch new alerts
        fetch('/api/alerts')
          .then(res => res.json())
          .then(data => {
            // Update alerts
          })
      }, 30000) // Refresh every 30 seconds

      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 border-red-400 text-red-700'
      case 'warning': return 'bg-yellow-100 border-yellow-400 text-yellow-700'
      case 'info': return 'bg-blue-100 border-blue-400 text-blue-700'
      default: return 'bg-gray-100 border-gray-400 text-gray-700'
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium">Performance Alerts</h3>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
            className="mr-2"
          />
          Auto-refresh
        </label>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No recent alerts
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`border-l-4 p-4 cursor-pointer ${getSeverityColor(alert.severity)}`}
              onClick={() => setExpandedAlert(expandedAlert === alert.id ? null : alert.id)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className="font-medium">
                    {alert.metricName} - {alert.severity.toUpperCase()}
                  </div>
                  <div className="text-sm opacity-75">
                    Value: {alert.value} (threshold: {alert.threshold})
                  </div>
                  <div className="text-xs opacity-50">
                    {new Date(alert.timestamp).toLocaleString()}
                  </div>
                </div>
                <svg
                  className={`w-5 h-5 transform transition-transform ${expandedAlert === alert.id ? 'rotate-90' : ''}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </div>

              {expandedAlert === alert.id && (
                <div className="mt-3 pt-3 border-t border-current border-opacity-20">
                  <div className="text-sm">
                    <div className="font-medium mb-1">URL: {alert.url}</div>
                    <div className="font-medium mb-1">User Agent:</div>
                    <div className="text-xs font-mono break-all opacity-75">
                      {alert.userAgent}
                    </div>
                    <div className="mt-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          // Dismiss alert
                          fetch(`/api/alerts/${alert.id}/dismiss`, { method: 'POST' })
                        }}
                        className="text-sm underline"
                      >
                        Dismiss Alert
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
```

## CI/CD Integration

### GitHub Actions Performance Monitoring

```yaml
# .github/workflows/monitoring.yml
name: Performance Monitoring

on:
  schedule:
    # Run every 4 hours
    - cron: '0 */4 * * *'
  workflow_dispatch:

jobs:
  performance-monitoring:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build
        env:
          NODE_ENV: production

      - name: Start application
        run: |
          npm run start &
          sleep 30

      - name: Run Lighthouse tests
        run: npm run lighthouse:ci

      - name: Run synthetic monitoring
        run: npm run monitoring:synthetic

      - name: Check for regressions
        run: npm run monitoring:check-regressions

      - name: Upload performance reports
        uses: actions/upload-artifact@v3
        with:
          name: performance-reports
          path: performance-reports/

      - name: Send notifications on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: 'Performance monitoring detected issues!'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

By implementing these comprehensive monitoring strategies, your developer portfolio will maintain optimal performance and quickly identify and resolve any performance issues before they impact user experience.