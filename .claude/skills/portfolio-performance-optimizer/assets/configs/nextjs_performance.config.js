/** @type {import('next').NextConfig} */
const nextConfig = {
  // Performance optimizations
  reactStrictMode: true,
  swcMinify: true,

  // Experimental features for Next.js 16
  experimental: {
    // Enable Turbopack for development
    turbo: {
      loaders: {
        '.svg': ['@svgr/webpack'],
      },
    },

    // Partial Pre-Rendering
    ppr: 'incremental',

    // Optimize package imports
    optimizePackageImports: ['lucide-react', 'date-fns', 'lodash-es', 'framer-motion'],

    // Optimize CSS
    optimizeCss: true,

    // Optimize Server Components
    serverComponentsExternalPackages: ['sharp'],
  },

  // Bundle analysis and optimization
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Bundle analyzer
    if (!dev && !isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            default: {
              minChunks: 2,
              priority: -20,
              reuseExistingChunk: true,
            },
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendors',
              priority: -10,
              chunks: 'all',
            },
            common: {
              name: 'common',
              minChunks: 3,
              priority: -20,
              reuseExistingChunk: true,
            },
            // Portfolio-specific chunks
            syntax: {
              test: /[\\/]node_modules[\\/](prismjs|highlight\.js|shiki)[\\/]/,
              name: 'syntax-highlight',
              chunks: 'all',
              priority: 10,
            },
            ui: {
              test: /[\\/]node_modules[\\/](@radix-ui|@headlessui|framer-motion)[\\/]/,
              name: 'ui-libraries',
              chunks: 'all',
              priority: 15,
            },
            // External embed libraries
            embeds: {
              test: /[\\/]node_modules[\\/](react-player|react-gist|react-embed)[\\/]/,
              name: 'embed-libraries',
              chunks: 'all',
              priority: 12,
            },
          },
        },
      }

      // Add bundle analyzer plugin for analysis
      if (process.env.ANALYZE === 'true') {
        const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
        config.plugins.push(
          new BundleAnalyzerPlugin({
            analyzerMode: 'static',
            openAnalyzer: false,
          })
        )
      }

      // Performance monitoring
      config.plugins.push(
        new webpack.DefinePlugin({
          'process.env.PERFORMANCE_MONITORING': JSON.stringify(
            process.env.NODE_ENV === 'production'
          ),
        })
      )
    }

    // Optimize image handling
    config.module.rules.push({
      test: /\.(png|jpe?g|gif|webp|avif)$/i,
      type: 'asset',
      parser: {
        dataUrlCondition: {
          maxSize: 8 * 1024, // 8kb
        },
      },
      generator: {
        filename: 'static/images/[hash][ext][query]',
      },
    })

    // SVG optimization
    config.module.rules.push({
      test: /\.svg$/,
      use: [
        {
          loader: '@svgr/webpack',
          options: {
            svgo: true,
            svgoConfig: {
              plugins: [
                {
                  name: 'preset-default',
                  params: {
                    overrides: {
                      removeViewBox: false,
                    },
                  },
                },
              ],
            },
          },
        },
      ],
    })

    return config
  },

  // Image optimization configuration
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 31536000, // 1 year
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",

    // Portfolio-specific image domains
    domains: [
      'localhost',
      'your-domain.com',
      'cdn.your-domain.com',
      'images.unsplash.com',
      'github.com',
    ],

    // Remote patterns for external images
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      {
        protocol: 'https',
        hostname: 'github.com',
      },
    ],
  },

  // Compression
  compress: true,

  // Performance budgeting
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },

  // Output configuration
  output: 'standalone',

  // Caching headers for optimal performance
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/images/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
          {
            key: 'Vary',
            value: 'Accept',
          },
        ],
      },
      {
        source: '/fonts/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/(.*)\\.(js|css|woff|woff2)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ]
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
        ],
      },
    ]
  },

  // Redirects for portfolio-specific routes
  async redirects() {
    return [
      {
        source: '/github',
        destination: 'https://github.com/yourusername',
        permanent: true,
      },
      {
        source: '/linkedin',
        destination: 'https://linkedin.com/in/yourusername',
        permanent: true,
      },
      {
        source: '/twitter',
        destination: 'https://twitter.com/yourusername',
        permanent: true,
      },
    ]
  },

  // Rewrites for API routes and external services
  async rewrites() {
    return [
      {
        source: '/api/projects',
        destination: 'https://api.github.com/users/yourusername/repos',
      },
    ]
  },
}

// Environment-specific configurations
if (process.env.NODE_ENV === 'development') {
  nextConfig.compiler = {
    removeConsole: false,
  }
}

// Production optimizations
if (process.env.NODE_ENV === 'production') {
  nextConfig.compiler = {
    removeConsole: true,
  }
}

module.exports = nextConfig