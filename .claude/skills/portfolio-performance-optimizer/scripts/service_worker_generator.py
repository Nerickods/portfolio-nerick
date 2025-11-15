#!/usr/bin/env python3
"""
Service Worker Generator for Developer Portfolios
Creates advanced service workers with caching strategies optimized for portfolios
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import dataclasses
from datetime import datetime, timedelta

@dataclasses.dataclass
class CacheStrategy:
    """Cache strategy configuration"""
    name: str
    pattern: str
    strategy: str  # cacheFirst, networkFirst, staleWhileRevalidate, etc.
    max_age: int
    max_entries: int
    cache_name: str

@dataclasses.dataclass
class ServiceWorkerConfig:
    """Service worker configuration"""
    version: str
    cache_strategies: List[CacheStrategy]
    precache_assets: List[str]
  runtime_caching: List[Dict[str, Any]]
  offline_fallback: str
  background_sync: bool
  push_notifications: bool
  performance_optimizations: bool

class ServiceWorkerGenerator:
    """Main service worker generator class"""

    def __init__(self, project_path: str, output_dir: str = "./public"):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Portfolio-specific cache configurations
        self.portfolio_cache_patterns = [
            {
                'name': 'static-assets',
                'pattern': '/static/',
                'strategy': 'cacheFirst',
                'max_age': 365 * 24 * 60 * 60,  # 1 year
                'max_entries': 100
            },
            {
                'name': 'images',
                'pattern': '/images/',
                'strategy': 'cacheFirst',
                'max_age': 90 * 24 * 60 * 60,  # 3 months
                'max_entries': 200
            },
            {
                'name': 'api-responses',
                'pattern': '/api/',
                'strategy': 'networkFirst',
                'max_age': 5 * 60,  # 5 minutes
                'max_entries': 50
            },
            {
                'name': 'pages',
                'pattern': '/',
                'strategy': 'networkFirst',
                'max_age': 60,  # 1 minute
                'max_entries': 20
            },
            {
                'name': 'external-cdn',
                'pattern': ['https://fonts.googleapis.com/', 'https://cdn.jsdelivr.net/'],
                'strategy': 'cacheFirst',
                'max_age': 30 * 24 * 60 * 60,  # 30 days
                'max_entries': 50
            }
        ]

    def scan_project_assets(self) -> Dict[str, List[str]]:
        """Scan project for assets to precache"""
        print("🔍 Scanning project assets...")

        assets = {
            'static': [],
            'images': [],
            'pages': [],
            'fonts': [],
            'scripts': [],
            'styles': []
        }

        # Scan static directory
        static_dir = self.project_path / 'public' / 'static'
        if static_dir.exists():
            for file_path in static_dir.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.project_path / 'public')
                    assets['static'].append(f"/{relative_path}")

        # Scan images
        images_dir = self.project_path / 'public' / 'images'
        if images_dir.exists():
            for file_path in images_dir.rglob('*'):
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.avif']:
                    relative_path = file_path.relative_to(self.project_path / 'public')
                    assets['images'].append(f"/{relative_path}")

        # Scan for fonts
        fonts_dir = self.project_path / 'public' / 'fonts'
        if fonts_dir.exists():
            for file_path in fonts_dir.rglob('*'):
                if file_path.suffix.lower() in ['.woff', '.woff2', '.ttf', '.otf']:
                    relative_path = file_path.relative_to(self.project_path / 'public')
                    assets['fonts'].append(f"/{relative_path}")

        # Detect Next.js build outputs
        next_static = self.project_path / '.next' / 'static'
        if next_static.exists():
            for chunk_file in next_static.rglob('*.js'):
                assets['scripts'].append(f"/_next/static/{chunk_file.relative_to(next_static)}")
            for css_file in next_static.rglob('*.css'):
                assets['styles'].append(f"/_next/static/{css_file.relative_to(next_static)}")

        return assets

    def generate_cache_strategy(self, strategy_config: Dict[str, Any]) -> str:
        """Generate cache strategy code"""
        name = strategy_config['name']
        pattern = strategy_config['pattern']
        strategy = strategy_config['strategy']
        max_age = strategy_config['max_age']
        max_entries = strategy_config.get('max_entries', 50)

        strategy_code = f'''
  // {name.replace('-', ' ').title()} Cache Strategy
  registerRoute(
    {self.generate_matcher(pattern)},
    {self.generate_strategy_handler(strategy, max_age, max_entries)},
    '{strategy}'
  )'''

        return strategy_code

    def generate_matcher(self, pattern) -> str:
        """Generate route matcher code"""
        if isinstance(pattern, str):
            if pattern.startswith('/'):
                return f"new RoutePattern('{pattern}')"
            elif pattern.startswith('http'):
                return f"new RegExp('{pattern.replace('/', '\\/')}')"
            else:
                return f"new RoutePattern('{pattern}')"
        elif isinstance(pattern, list):
            patterns = [f"new RegExp('{p.replace('/', '\\/')}')" for p in pattern]
            return f"new RegExp({patterns.join('|')})"
        return "new RegExp('.*')"

    def generate_strategy_handler(self, strategy: str, max_age: int, max_entries: int) -> str:
        """Generate cache strategy handler"""
        handlers = {
            'cacheFirst': f'new CacheFirst({{"cacheName": "cache-first-{max_entries}", "plugins": [new ExpirationPlugin({{"maxEntries": {max_entries}, "maxAgeSeconds": {max_age}}})]}})',
            'networkFirst': f'new NetworkFirst({{"cacheName": "network-first-{max_entries}", "plugins": [new ExpirationPlugin({{"maxEntries": {max_entries}, "maxAgeSeconds": {max_age}}})]}})',
            'staleWhileRevalidate': f'new StaleWhileRevalidate({{"cacheName": "swr-{max_entries}", "plugins": [new ExpirationPlugin({{"maxEntries": {max_entries}, "maxAgeSeconds": {max_age}}})]}})',
            'networkOnly': 'new NetworkOnly()',
            'cacheOnly': 'new CacheOnly()'
        }

        return handlers.get(strategy, handlers['cacheFirst'])

    def generate_precache_manifest(self, assets: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Generate precache manifest"""
        manifest = []

        # Add static assets
        for asset_path in assets.get('static', []):
            manifest.append({
                'url': asset_path,
                'revision': self.generate_revision(),
                'size': self.get_file_size(asset_path)
            })

        # Add images
        for image_path in assets.get('images', []):
            manifest.append({
                'url': image_path,
                'revision': self.generate_revision(),
                'size': self.get_file_size(image_path)
            })

        # Add fonts
        for font_path in assets.get('fonts', []):
            manifest.append({
                'url': font_path,
                'revision': self.generate_revision(),
                'size': self.get_file_size(font_path)
            })

        return manifest

    def generate_revision(self) -> str:
        """Generate revision for cache busting"""
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def get_file_size(self, file_path: str) -> int:
        """Get file size for precache manifest"""
        try:
            full_path = self.project_path / 'public' / file_path.lstrip('/')
            return full_path.stat().st_size if full_path.exists() else 0
        except:
            return 0

    def generate_service_worker(self, config: ServiceWorkerConfig) -> str:
        """Generate complete service worker code"""
        sw_code = f'''// Portfolio Performance Optimized Service Worker
// Version: {config.version}
// Generated: {datetime.now().isoformat()}

// Import Workbox for advanced caching strategies
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-sw.js');

// Service Worker Configuration
const CACHE_VERSION = '{config.version}';
const CACHE_PREFIX = 'portfolio-';

// Portfolio-specific performance optimizations
const PERFORMANCE_CONFIG = {{
  maxAgeImages: 90 * 24 * 60 * 60,  // 3 months
  maxAgeStatic: 365 * 24 * 60 * 60,  // 1 year
  maxAgeAPI: 5 * 60,  // 5 minutes
  maxEntriesImages: 200,
  maxEntriesStatic: 100,
  maxEntriesAPI: 50,
}};

// Precaching Configuration
const PRECACHE_CONFIG = {{
  cacheId: '{{{CACHE_PREFIX}precache}}',
  plugins: [
    new workbox.expiration.ExpirationPlugin({{
      maxEntries: 100,
      maxAgeSeconds: PERFORMANCE_CONFIG.maxAgeStatic,
    }}),
  ],
}};

// Install event - precache critical assets
self.addEventListener('install', (event) => {{
  console.log('🚀 Portfolio SW: Installing...');

  event.waitUntil(
    caches.open(`{{CACHE_PREFIX}}static-v{{CACHE_VERSION}}`)
      .then((cache) => {{
        console.log('📦 Portfolio SW: Precaching static assets');
        return cache.addAll({json.dumps(config.precache_assets, indent=6)});
      }})
      .then(() => self.skipWaiting())
  );
}});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {{
  console.log('✅ Portfolio SW: Activating...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {{
        return Promise.all(
          cacheNames
            .filter((cacheName) => {{
              return cacheName.startsWith(CACHE_PREFIX) &&
                     !cacheName.includes(CACHE_VERSION);
            }})
            .map((cacheName) => {{
              console.log('🗑️ Portfolio SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }})
        );
      }})
      .then(() => self.clients.claim())
  );
}});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {{
  const {{ request }} = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip external requests (except CDN)
  if (url.origin !== location.origin &&
      !url.hostname.includes('cdn.') &&
      !url.hostname.includes('fonts.googleapis.com')) return;

  // Route requests to appropriate caching strategy
  if (shouldCacheFirst(request.url)) {{
    event.respondWith(cacheFirstStrategy(request));
  }} else if (shouldNetworkFirst(request.url)) {{
    event.respondWith(networkFirstStrategy(request));
  }} else if (shouldStaleWhileRevalidate(request.url)) {{
    event.respondWith(staleWhileRevalidateStrategy(request));
  }}
}});

// Helper functions for caching strategies
function shouldCacheFirst(url) {{
  return url.includes('/static/') ||
         url.includes('/images/') ||
         url.includes('/fonts/') ||
         url.hostname.includes('cdn.') ||
         url.hostname.includes('fonts.googleapis.com');
}}

function shouldNetworkFirst(url) {{
  return url.includes('/api/') ||
         url.pathname === '/' ||
         url.pathname.includes('/project/');
}}

function shouldStaleWhileRevalidate(url) {{
  return url.includes('/_next/static/');
}}

// Caching strategy implementations
async function cacheFirstStrategy(request) {{
  const cacheName = `{{CACHE_PREFIX}}cache-first-{{CACHE_VERSION}}`;

  try {{
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {{
      return cachedResponse;
    }}

    const networkResponse = await fetch(request);
    if (networkResponse.ok) {{
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }}

    return networkResponse;
  }} catch (error) {{
    console.error('Cache first strategy failed:', error);
    return new Response('Offline', {{ status: 503 }});
  }}
}}

async function networkFirstStrategy(request) {{
  const cacheName = `{{CACHE_PREFIX}}network-first-{{CACHE_VERSION}}`;

  try {{
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);

    try {{
      const networkResponse = await fetch(request);
      if (networkResponse.ok) {{
        cache.put(request, networkResponse.clone());
      }}
      return networkResponse;
    }} catch (networkError) {{
      console.log('Network failed, serving from cache:', networkError);
      return cachedResponse || new Response('Offline', {{ status: 503 }});
    }}
  }} catch (error) {{
    console.error('Network first strategy failed:', error);
    return new Response('Offline', {{ status: 503 }});
  }}
}}

async function staleWhileRevalidateStrategy(request) {{
  const cacheName = `{{CACHE_PREFIX}}swr-{{CACHE_VERSION}}`;

  try {{
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);

    const fetchPromise = fetch(request).then((networkResponse) => {{
      if (networkResponse.ok) {{
        cache.put(request, networkResponse.clone());
      }}
      return networkResponse;
    }});

    return cachedResponse || await fetchPromise;
  }} catch (error) {{
    console.error('Stale while revalidate strategy failed:', error);
    return new Response('Offline', {{ status: 503 }});
  }}
}}

// Background sync for portfolio updates
{self.generate_background_sync_code(config.background_sync)}

// Push notification handling
{self.generate_push_notification_code(config.push_notifications)}

// Performance monitoring
{self.generate_performance_monitoring_code(config.performance_optimizations)}

// Utility functions
function generateCacheKey(request) {{
  return request.url + (request.method || 'GET');
}}

async function clearOldCaches() {{
  const cacheNames = await caches.keys();
  const currentCacheNames = [
    `{{CACHE_PREFIX}}cache-first-{{CACHE_VERSION}}`,
    `{{CACHE_PREFIX}}network-first-{{CACHE_VERSION}}`,
    `{{CACHE_PREFIX}}swr-{{CACHE_VERSION}}`,
  ];

  return Promise.all(
    cacheNames
      .filter(cacheName => !currentCacheNames.includes(cacheName))
      .map(cacheName => caches.delete(cacheName))
  );
}}

// Portfolio-specific optimizations
function optimizeForPortfolio(request) {{
  // Handle syntax highlighting libraries
  if (request.url.includes('prism') || request.url.includes('highlight.js')) {{
    return cacheFirstStrategy(request);
  }}

  // Handle project screenshots
  if (request.url.includes('/projects/') && request.url.match(/\.(jpg|jpeg|png|webp)$/)) {{
    return cacheFirstStrategy(request);
  }}

  // Handle GitHub embeds
  if (request.url.includes('github.com/embed')) {{
    return networkFirstStrategy(request);
  }}

  return null;
}}

console.log('🎨 Portfolio Performance Service Worker loaded');
'''

        return sw_code

    def generate_background_sync_code(self, enabled: bool) -> str:
        """Generate background sync code"""
        if not enabled:
            return "// Background sync disabled"

        return '''
// Background Sync for portfolio updates
self.addEventListener('sync', (event) => {
  if (event.tag === 'portfolio-update') {
    event.waitUntil(syncPortfolioData());
  }
});

async function syncPortfolioData() {
  try {
    // Sync portfolio data when back online
    const response = await fetch('/api/portfolio/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (response.ok) {
      console.log('📱 Portfolio data synced successfully');
      // Clear cached portfolio data
      await caches.delete(`${CACHE_PREFIX}network-first-${CACHE_VERSION}`);
    }
  } catch (error) {
    console.error('Portfolio sync failed:', error);
  }
}
'''

    def generate_push_notification_code(self, enabled: bool) -> str:
        """Generate push notification code"""
        if not enabled:
            return "// Push notifications disabled"

        return '''
// Push notification handling
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'New portfolio update available',
    icon: '/images/icon-192x192.png',
    badge: '/images/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };

  event.waitUntil(
    self.registration.showNotification('Portfolio Update', options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/')
  );
});
'''

    def generate_performance_monitoring_code(self, enabled: bool) -> str:
        """Generate performance monitoring code"""
        if not enabled:
            return "// Performance monitoring disabled"

        return '''
// Performance monitoring
self.addEventListener('fetch', (event) => {
  const start = performance.now();

  event.respondWith(
    (async () => {
      try {
        const response = await fetch(event.request);
        const duration = performance.now() - start;

        // Log slow requests
        if (duration > 1000) {
          console.warn(`Slow request detected: ${event.request.url} (${duration.toFixed(2)}ms)`);
        }

        return response;
      } catch (error) {
        const duration = performance.now() - start;
        console.error(`Request failed: ${event.request.url} (${duration.toFixed(2)}ms)`, error);
        throw error;
      }
    })()
  );
});
'''

    def generate_registration_script(self) -> str:
        """Generate service worker registration script"""
        return '''
// Service Worker Registration for Portfolio
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('✅ Portfolio SW registered successfully:', registration.scope);

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New content is available
              if (confirm('New version available! Reload to update?')) {
                window.location.reload();
              }
            }
          });
        });
      })
      .catch((error) => {
        console.error('❌ Portfolio SW registration failed:', error);
      });
  });
}
'''

    def save_service_worker(self, sw_code: str, registration_script: str) -> Tuple[str, str]:
        """Save service worker files"""
        # Save main service worker
        sw_path = self.output_dir / 'sw.js'
        sw_path.write_text(sw_code, encoding='utf-8')

        # Save registration script
        reg_path = self.output_dir / 'sw-register.js'
        reg_path.write_text(registration_script, encoding='utf-8')

        print(f"📄 Service worker saved: {sw_path}")
        print(f"📄 Registration script saved: {reg_path}")

        return str(sw_path), str(reg_path)

def main():
    parser = argparse.ArgumentParser(description='Service Worker Generator for Developer Portfolios')
    parser.add_argument('project_path', help='Path to Next.js project')
    parser.add_argument('--output', default='./public', help='Output directory for service worker')
    parser.add_argument('--version', default='1.0.0', help='Service worker version')
    parser.add_argument('--background-sync', action='store_true', help='Enable background sync')
    parser.add_argument('--push-notifications', action='store_true', help='Enable push notifications')
    parser.add_argument('--performance-monitoring', action='store_true', help='Enable performance monitoring')
    parser.add_argument('--caching-strategy', choices=['aggressive', 'balanced', 'conservative'],
                       default='balanced', help='Caching strategy level')

    args = parser.parse_args()

    # Initialize generator
    generator = ServiceWorkerGenerator(args.project_path, args.output)

    # Scan project assets
    assets = generator.scan_project_assets()

    # Create configuration
    precache_assets = assets['static'][:50]  # Limit to 50 most important assets
    if not precache_assets:
        # Fallback precache assets
        precache_assets = [
            '/',
            '/manifest.json',
            '/favicon.ico',
            '/_next/static/css/app.css',
            '/_next/static/chunks/app.js'
        ]

    config = ServiceWorkerConfig(
        version=args.version,
        cache_strategies=[],
        precache_assets=precache_assets,
        runtime_caching=[],
        offline_fallback='/offline',
        background_sync=args.background_sync,
        push_notifications=args.push_notifications,
        performance_optimizations=args.performance_monitoring
    )

    # Generate service worker
    sw_code = generator.generate_service_worker(config)
    registration_script = generator.generate_registration_script()

    # Save files
    sw_path, reg_path = generator.save_service_worker(sw_code, registration_script)

    print(f"\n🎉 Service worker generated successfully!")
    print(f"📁 Assets scanned: {sum(len(v) for v in assets.values())} files")
    print(f"📦 Precache assets: {len(precache_assets)} items")
    print(f"🔧 Features: Background Sync: {args.background_sync}, Push: {args.push_notifications}, Monitoring: {args.performance_monitoring}")
    print(f"\n📝 Next steps:")
    print(f"1. Add `{reg_path}` to your _app.js or layout.tsx")
    print(f"2. Test service worker functionality")
    print(f"3. Verify caching behavior in browser dev tools")

if __name__ == "__main__":
    main()