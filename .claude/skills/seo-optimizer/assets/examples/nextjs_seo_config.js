// next.config.js - Complete SEO Configuration for Developer Portfolio
const withTM = require('next-transpile-modules')(['shared-ui']);

const nextConfig = {
  // Production optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Image optimization
  images: {
    domains: [
      'images.unsplash.com',
      'github.com',
      'linkedin.com',
      'twitter.com',
      'sarahchen.dev' // Add your own domain
    ],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60 * 60 * 24 * 365, // 1 year
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Bundle analysis and optimization
  webpack: (config, { isServer, dev }) => {
    if (!isServer) {
      // Code splitting optimization
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
            priority: 10,
          },
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            priority: 5,
            enforce: true,
          },
          // React and related libraries
          react: {
            test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
            name: 'react-vendor',
            chunks: 'all',
            priority: 15,
          },
          // Charts and visualization libraries
          charts: {
            test: /[\\/]node_modules[\\/](recharts|d3|chart\.js)[\\/]/,
            name: 'charts-vendor',
            chunks: 'all',
            priority: 12,
          },
        },
      };

      // Tree shaking for unused exports
      config.optimization.usedExports = true;
      config.optimization.sideEffects = false;
    }

    // Enable React Fast Refresh in development
    if (dev) {
      config.resolve.alias = {
        ...config.resolve.alias,
        'react-dom': '@hot-loader/react-dom',
      };
    }

    return config;
  },

  // Compression
  compress: true,

  // Performance optimizations
  poweredByHeader: false,
  generateEtags: true,

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
      // Cache static assets
      {
        source: '/images/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      // Cache API responses
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=86400',
          },
        ],
      },
    ];
  },

  // Redirects for SEO
  async redirects() {
    return [
      // Redirect old URLs to new ones
      {
        source: '/portfolio/:path*',
        destination: '/projects/:path*',
        permanent: true,
      },
      // Redirect trailing slashes
      {
        source: '/:path*//',
        destination: '/:path*',
        permanent: true,
      },
      // Redirect common typos
      {
        source: '/projcts/:path*',
        destination: '/projects/:path*',
        permanent: true,
      },
    ];
  },

  // Rewrites for clean URLs
  async rewrites() {
    return [
      // Clean URLs for projects
      {
        source: '/project/:slug',
        destination: '/projects/[slug]',
      },
      // Clean URLs for blog posts
      {
        source: '/blog/:slug',
        destination: '/blog/[slug]',
      },
    ];
  },

  // Experimental features
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', 'date-fns'],
    scrollRestoration: true,
  },

  // Environment variables for SEO
  env: {
    SITE_URL: process.env.SITE_URL || 'https://sarahchen.dev',
    NEXT_PUBLIC_GA_ID: process.env.NEXT_PUBLIC_GA_ID,
    NEXT_PUBLIC_SITE_NAME: process.env.NEXT_PUBLIC_SITE_NAME || 'Sarah Chen - Portfolio',
  },
};

// SEO Helper Functions
const seoConfig = {
  // Default SEO metadata
  siteMetadata: {
    title: 'Sarah Chen | Senior React Developer',
    description: 'Senior React Developer with 8+ years building scalable web applications for fintech startups. Specializing in React, TypeScript, and Node.js.',
    author: 'Sarah Chen',
    siteUrl: 'https://sarahchen.dev',
    image: '/images/og-default.jpg',
    twitterUsername: '@sarahchen_dev',
  },

  // Open Graph configurations
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://sarahchen.dev',
    site_name: 'Sarah Chen - Portfolio',
    images: [
      {
        url: '/images/og-default.jpg',
        width: 1200,
        height: 630,
        alt: 'Sarah Chen - Senior React Developer',
      },
    ],
  },

  // Twitter Card configurations
  twitter: {
    cardType: 'summary_large_image',
    handle: '@sarahchen_dev',
  },

  // Schema.org configurations
  schema: {
    person: {
      '@context': 'https://schema.org',
      '@type': 'Person',
      name: 'Sarah Chen',
      jobTitle: 'Senior React Developer',
      url: 'https://sarahchen.dev',
      sameAs: [
        'https://github.com/sarahchen',
        'https://linkedin.com/in/sarahchen',
        'https://twitter.com/sarahchen_dev',
      ],
    },
  },
};

// SEO Helper Functions
function generateSEOMetadata(pageData, config = seoConfig) {
  const {
    title,
    description,
    image,
    url,
    type = 'website',
    keywords,
    noindex = false,
  } = pageData;

  const metadata = {
    title: title || config.siteMetadata.title,
    description: description || config.siteMetadata.description,
    keywords: keywords || '',
    canonical: url || config.siteMetadata.siteUrl,
    openGraph: {
      ...config.openGraph,
      title: title || config.openGraph.title,
      description: description || config.openGraph.description,
      url: url || config.openGraph.url,
      type,
      images: image
        ? [
            {
              url: image,
              width: 1200,
              height: 630,
              alt: title || config.siteMetadata.title,
            },
          ]
        : config.openGraph.images,
    },
    twitter: {
      ...config.twitter,
      title: title || config.openGraph.title,
      description: description || config.openGraph.description,
      image: image || config.openGraph.images[0].url,
    },
    robots: {
      index: !noindex,
      follow: !noindex,
      googleBot: {
        index: !noindex,
        follow: !noindex,
        'max-video-preview': -1,
        'max-image-preview': 'large',
        'max-snippet': -1,
      },
    },
  };

  return metadata;
}

// Sitemap generation helper
function generateSitemapPages() {
  const staticPages = [
    {
      url: '/',
      changefreq: 'weekly',
      priority: 1.0,
    },
    {
      url: '/about',
      changefreq: 'monthly',
      priority: 0.8,
    },
    {
      url: '/projects',
      changefreq: 'weekly',
      priority: 0.9,
    },
    {
      url: '/skills',
      changefreq: 'monthly',
      priority: 0.7,
    },
    {
      url: '/contact',
      changefreq: 'monthly',
      priority: 0.8,
    },
  ];

  return staticPages;
}

// Robots.txt generation
function generateRobotsTxt() {
  return `User-agent: *
Allow: /
Disallow: /api/
Disallow: /_next/static/
Disallow: /admin/
Disallow: /*.json$

Sitemap: https://sarahchen.dev/sitemap.xml
Sitemap: https://sarahchen.dev/sitemap-projects.xml

# Crawl delay
Crawl-delay: 1

# Allow important resources
Allow: /images/
Allow: /css/
Allow: /js/

# Block crawlers on API routes
User-agent: *
Disallow: /api/`;
}

module.exports = withTM(nextConfig);
module.exports.seoConfig = seoConfig;
module.exports.generateSEOMetadata = generateSEOMetadata;
module.exports.generateSitemapPages = generateSitemapPages;
module.exports.generateRobotsTxt = generateRobotsTxt;