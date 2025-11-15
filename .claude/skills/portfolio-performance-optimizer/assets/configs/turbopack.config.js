/** @type {import('next').TurboConfig} */
const turboConfig = {
  // Turbopack optimization for Next.js 16
  turbo: {
    // Custom loaders for portfolio assets
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
      '*.module.css': {
        loaders: [
          {
            loader: 'css-loader',
            options: {
              modules: {
                localIdentName: '[name]__[local]___[hash:base64:5]',
              },
            },
          },
        ],
      },
      '*.mdx': {
        loaders: ['@next/mdx'],
        as: '*.js',
      },
    },

    // Resolve aliases for faster builds and better DX
    resolveAlias: {
      '@': './src',
      '@components': './src/components',
      '@lib': './src/lib',
      '@styles': './src/styles',
      '@assets': './public/assets',
      '@hooks': './src/hooks',
      '@utils': './src/utils',
      '@types': './src/types',
      '@config': './config',
    },

    // Dependency optimization for portfolio libraries
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-hook-form',
        'framer-motion',
        'lucide-react',
        'date-fns',
        'clsx',
        'tailwind-merge',
        'next-themes',
      ],
      exclude: [
        'sharp',
        'canvas',
        'node-gyp',
        'bufferutil',
        'utf-8-validate',
      ],
    },

    // Environment-specific optimizations
    ...(process.env.NODE_ENV === 'production' && {
      minify: true,
      treeshake: true,
      deadCodeElimination: true,
      // Remove console.log in production
      define: {
        'process.env.NODE_ENV': JSON.stringify('production'),
      },
    }),

    // Development optimizations
    ...(process.env.NODE_ENV === 'development' && {
      fastRefresh: true,
      devIndicators: {
        buildActivity: true,
        buildActivityPosition: 'bottom-right',
      },
    }),

    // Bundle splitting optimization
    splitBundles: true,
    bundleSplitting: {
      chunks: 'all',
      cacheGroups: {
        // Essential libraries
        essentials: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'essentials',
          priority: 20,
        },
        // UI libraries
        ui: {
          test: /[\\/]node_modules[\\/](@radix-ui|framer-motion|lucide-react)[\\/]/,
          name: 'ui',
          priority: 15,
        },
        // Utility libraries
        utils: {
          test: /[\\/]node_modules[\\/](date-fns|clsx|tailwind-merge)[\\/]/,
          name: 'utils',
          priority: 10,
        },
        // Portfolio-specific libraries
        portfolio: {
          test: /[\\/]node_modules[\\/](prismjs|remark|react-syntax-highlighter)[\\/]/,
          name: 'portfolio',
          priority: 12,
        },
      },
    },

    // CSS optimization
    css: {
      modules: {
        localsConvention: 'camelCase',
      },
      postcss: {
        plugins: [
          'tailwindcss',
          'autoprefixer',
          ...(process.env.NODE_ENV === 'production' ? ['cssnano'] : []),
        ],
      },
    },

    // Performance monitoring hooks
    perf: {
      timings: true,
      logging: process.env.NODE_ENV === 'development',
    },

    // Advanced optimizations
    experimental: {
      optimizePackageImports: [
        'lucide-react',
        'date-fns',
        'framer-motion',
        '@radix-ui/react-icons',
      ],
      // Enable React concurrent features
      concurrentFeatures: true,
      // Server components optimization
      serverComponents: true,
      // Incremental Static Regeneration optimization
      isr: {
        maxAge: 60, // 1 minute
        staggerConcurrency: true,
      },
    },
  },

  // Webpack optimizations for compatibility
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Optimize for client-side
      config.optimization = {
        ...config.optimization,
        runtimeChunk: 'single',
        moduleIds: 'deterministic',
      }
    }

    return config
  },
}

// Performance budgets
module.exports = {
  ...turboConfig,
  performance: {
    maxAssetSize: 244 * 1024, // 244KB
    maxEntrypointSize: 244 * 1024,
    hints: 'warning',
  },
}

module.exports = turboConfig