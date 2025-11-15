module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      startServerCommand: 'npm run build && npm run start',
      startServerReadyPattern: 'ready on',
      startServerReadyTimeout: 30000,
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        'categories:pwa': 'off',

        // Core Web Vitals thresholds
        'largest-contentful-paint': ['warn', { maxNumericValue: 2500 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 1000 }],
        'speed-index': ['warn', { maxNumericValue: 1500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],

        // Portfolio-specific budgets
        'performance-budget:script:size': ['warn', { maxNumericValue: 250000 }],
        'performance-budget:total:size': ['warn', { maxNumericValue: 1000000 }],
        'performance-budget:image:size': ['warn', { maxNumericValue: 500000 }],
        'performance-budget:font:size': ['warn', { maxNumericValue: 150000 }],
        'performance-budget:stylesheet:size': ['warn', { maxNumericValue: 50000 }],

        // Resource limits
        'resource-summary:script:count': ['warn', { maxNumericValue: 15 }],
        'resource-summary:image:count': ['warn', { maxNumericValue: 20 }],
        'resource-summary:font:count': ['warn', { maxNumericValue: 4 }],
        'resource-summary:stylesheet:count': ['warn', { maxNumericValue: 5 }],

        // Interaction metrics
        'max-potential-fid': ['warn', { maxNumericValue: 100 }],
        'interactive': ['warn', { maxNumericValue: 3000 }],

        // Server metrics
        'server-response-time': ['warn', { maxNumericValue: 600 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};