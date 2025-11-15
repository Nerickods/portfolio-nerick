#!/usr/bin/env python3
"""
Bundle Optimizer for Developer Portfolios
Next.js 16 and Turbopack optimization tools
"""

import json
import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import dataclasses

@dataclasses.dataclass
class BundleAnalysis:
    """Bundle analysis data structure"""
    total_size: int
    chunks: List[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]
    duplicate_modules: List[str]
    unused_exports: List[str]
    optimization_opportunities: List[str]

@dataclasses.dataclass
class OptimizationResult:
    """Optimization result structure"""
    original_size: int
    optimized_size: int
    size_reduction: float
    optimizations_applied: List[str]
    recommendations: List[str]
    configuration_changes: Dict[str, Any]

class BundleOptimizer:
    """Main bundle optimizer class for Next.js portfolios"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.next_config_path = self.project_path / 'next.config.js'
        self.package_json_path = self.project_path / 'package.json'
        self.turbopack_config_path = self.project_path / 'turbopack.config.js'

    def analyze_current_bundle(self) -> BundleAnalysis:
        """Analyze current bundle structure"""
        print("📦 Analyzing current bundle structure...")

        analysis = BundleAnalysis(
            total_size=0,
            chunks=[],
            dependencies=[],
            duplicate_modules=[],
            unused_exports=[],
            optimization_opportunities=[]
        )

        # Analyze .next build output
        next_dir = self.project_path / '.next'
        if next_dir.exists():
            for chunk_file in next_dir.rglob('*.js'):
                size = chunk_file.stat().st_size
                analysis.total_size += size

                chunk_info = {
                    'name': chunk_file.name,
                    'size': size,
                    'size_human': self.format_size(size),
                    'path': str(chunk_file.relative_to(self.project_path))
                }
                analysis.chunks.append(chunk_info)

        # Analyze package.json dependencies
        if self.package_json_path.exists():
            with open(self.package_json_path, 'r') as f:
                package_data = json.load(f)

                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})

                for dep, version in dependencies.items():
                    analysis.dependencies.append({
                        'name': dep,
                        'version': version,
                        'type': 'dependency'
                    })

                for dep, version in dev_dependencies.items():
                    analysis.dependencies.append({
                        'name': dep,
                        'version': version,
                        'type': 'devDependency'
                    })

        # Detect optimization opportunities
        analysis.optimization_opportunities = self.detect_optimization_opportunities(analysis)

        return analysis

    def detect_optimization_opportunities(self, analysis: BundleAnalysis) -> List[str]:
        """Detect potential bundle optimization opportunities"""
        opportunities = []

        # Check for large chunks
        large_chunks = [c for c in analysis.chunks if c['size'] > 100 * 1024]  # 100KB
        if large_chunks:
            opportunities.append(f"Found {len(large_chunks)} large chunks that could benefit from code splitting")

        # Check for heavy dependencies
        heavy_deps = [d for d in analysis.dependencies if d['name'] in [
            'moment', 'lodash', 'axios', 'date-fns', 'three', '@material-ui/core'
        ]]
        if heavy_deps:
            opportunities.append(f"Consider tree-shaking or alternatives for heavy libraries: {', '.join([d['name'] for d in heavy_deps])}")

        # Check total bundle size
        if analysis.total_size > 250 * 1024:  # 250KB
            opportunities.append("Bundle exceeds recommended size (250KB gzipped)")

        return opportunities

    def analyze_webpack_config(self) -> Dict[str, Any]:
        """Analyze existing Webpack configuration"""
        print("⚙️ Analyzing Webpack configuration...")

        config_analysis = {
            'has_split_chunks': False,
            'has_compression': False,
            'has_minification': True,
            'has_tree_shaking': True,
            'optimization_level': 'basic'
        }

        if self.next_config_path.exists():
            content = self.next_config_path.read_text(encoding='utf-8')

            # Check for optimization configurations
            if 'splitChunks' in content:
                config_analysis['has_split_chunks'] = True
            if 'compression' in content:
                config_analysis['has_compression'] = True
            if 'minify' in content:
                config_analysis['has_minification'] = True

            # Determine optimization level
            optimization_features = sum([
                config_analysis['has_split_chunks'],
                config_analysis['has_compression'],
                config_analysis['has_tree_shaking']
            ])

            if optimization_features >= 3:
                config_analysis['optimization_level'] = 'advanced'
            elif optimization_features >= 2:
                config_analysis['optimization_level'] = 'intermediate'

        return config_analysis

    def generate_nextjs_config(self) -> str:
        """Generate optimized Next.js 16 configuration"""
        config = '''/** @type {import('next').NextConfig} */
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
    optimizePackageImports: ['lucide-react', 'date-fns', 'lodash-es'],

    // Optimize CSS
    optimizeCss: true,

    // Optimize Server Components
    serverComponentsExternalPackages: ['sharp'],
  },

  // Bundle analysis
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
              test: /[\\\\/]node_modules[\\\\/]/,
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
            // Specific chunks for portfolio libraries
            syntax: {
              test: /[\\\\/]node_modules[\\\\/](prismjs|highlight\.js|shiki)[\\\\/]/,
              name: 'syntax-highlight',
              chunks: 'all',
              priority: 10,
            },
            ui: {
              test: /[\\\\/]node_modules[\\\\/](@radix-ui|@headlessui|framer-motion)[\\\\/]/,
              name: 'ui-libraries',
              chunks: 'all',
              priority: 15,
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
    }

    // Optimize image handling
    config.module.rules.push({
      test: /\.(png|jpe?g|gif|webp)$/i,
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

    return config
  },

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 31536000, // 1 year
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
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

  // Caching headers
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
    ]
  },
}

module.exports = nextConfig'''

        return config

    def generate_turbopack_config(self) -> str:
        """Generate Turbopack configuration for Next.js 16"""
        config = '''/** @type {import('next').TurboConfig} */
const turboConfig = {
  // Turbopack optimizations
  turbo: {
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
    },

    // Resolve aliases for faster builds
    resolveAlias: {
      '@': './src',
      '@components': './src/components',
      '@lib': './src/lib',
      '@styles': './src/styles',
      '@assets': './public/assets',
    },

    // Optimizations
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'framer-motion',
        'lucide-react',
        'date-fns',
      ],
      exclude: ['sharp', 'canvas'],
    },

    // Environment-specific optimizations
    ...(process.env.NODE_ENV === 'production' && {
      minify: true,
      treeshake: true,
      deadCodeElimination: true,
    }),
  },
}

module.exports = turboConfig'''

        return config

    def optimize_package_json(self) -> Dict[str, Any]:
        """Optimize package.json dependencies"""
        print("📚 Analyzing package dependencies...")

        if not self.package_json_path.exists():
            return {}

        with open(self.package_json_path, 'r') as f:
            package_data = json.load(f)

        optimization_suggestions = []

        # Check for heavy dependencies that could be replaced
        heavy_alternatives = {
            'moment': 'date-fns',
            'lodash': 'lodash-es',
            'axios': 'fetch API / undici',
            'classnames': 'clsx',
            'prop-types': 'TypeScript',
        }

        dependencies = package_data.get('dependencies', {})

        for heavy, alternative in heavy_alternatives.items():
            if heavy in dependencies:
                optimization_suggestions.append(f"Consider replacing {heavy} with {alternative}")

        return {
            'current_dependencies': dependencies,
            'optimization_suggestions': optimization_suggestions,
            'recommended_dev_dependencies': [
                '@next/bundle-analyzer',
                'webpack-bundle-analyzer',
                'eslint-plugin-unused-imports',
                'lighthouse',
            ]
        }

    def generate_code_splitting_recommendations(self) -> List[str]:
        """Generate code splitting recommendations"""
        recommendations = []

        # Portfolio-specific recommendations
        portfolio_routes = [
            "Dynamic import for project detail pages",
            "Lazy load syntax highlighting libraries",
            "Split large project galleries into separate chunks",
            "Lazy load contact forms and interactive components",
            "Separate admin/development tools from main bundle",
        ]

        recommendations.extend(portfolio_routes)

        # Generic recommendations
        generic_recommendations = [
            "Implement React.lazy() for route-based splitting",
            "Use dynamic imports for third-party libraries",
            "Split vendor libraries from application code",
            "Create separate chunks for different page categories",
            "Implement intersection observer for lazy loading",
        ]

        recommendations.extend(generic_recommendations)

        return recommendations

    def apply_optimizations(self, dry_run: bool = True) -> OptimizationResult:
        """Apply bundle optimizations"""
        print("⚡ Applying bundle optimizations...")

        # Analyze current state
        original_analysis = self.analyze_current_bundle()
        original_size = original_analysis.total_size

        optimizations_applied = []

        if not dry_run:
            # Backup original config
            if self.next_config_path.exists():
                backup_path = self.next_config_path.with_suffix('.js.backup')
                self.next_config_path.rename(backup_path)
                print(f"📋 Backed up original config to {backup_path}")

            # Generate optimized Next.js config
            optimized_config = self.generate_nextjs_config()
            self.next_config_path.write_text(optimized_config, encoding='utf-8')
            optimizations_applied.append("Next.js configuration optimized")

            # Generate Turbopack config
            turbopack_config = self.generate_turbopack_config()
            self.turbopack_config_path.write_text(turbopack_config, encoding='utf-8')
            optimizations_applied.append("Turbopack configuration created")

        # Calculate potential improvements
        estimated_reduction = min(original_size * 0.3, 100 * 1024)  # Max 100KB reduction
        optimized_size = original_size - estimated_reduction

        # Generate recommendations
        recommendations = self.generate_code_splitting_recommendations()

        return OptimizationResult(
            original_size=original_size,
            optimized_size=optimized_size,
            size_reduction=estimated_reduction / original_size * 100,
            optimizations_applied=optimizations_applied,
            recommendations=recommendations,
            configuration_changes={
                'next_config': 'Optimized for performance',
                'turbopack_config': 'Created for Next.js 16',
                'webpack_optimizations': 'Advanced splitting and minification',
            }
        )

    def format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} GB"

    def generate_optimization_report(self, analysis: BundleAnalysis,
                                   optimization_result: OptimizationResult) -> str:
        """Generate comprehensive bundle optimization report"""
        report = []

        report.append("# Bundle Optimization Report")
        report.append("")

        # Bundle Analysis
        report.append("## 📦 Current Bundle Analysis")
        report.append(f"**Total Size:** {self.format_size(analysis.total_size)}")
        report.append(f"**Number of Chunks:** {len(analysis.chunks)}")
        report.append(f"**Dependencies:** {len(analysis.dependencies)}")
        report.append("")

        # Largest chunks
        report.append("### Largest Chunks")
        for chunk in sorted(analysis.chunks, key=lambda x: x['size'], reverse=True)[:5]:
            report.append(f"- **{chunk['name']}**: {chunk['size_human']}")
        report.append("")

        # Optimization Opportunities
        if analysis.optimization_opportunities:
            report.append("## 🎯 Optimization Opportunities")
            for opportunity in analysis.optimization_opportunities:
                report.append(f"- {opportunity}")
            report.append("")

        # Optimization Results
        report.append("## ⚡ Optimization Results")
        report.append(f"**Original Size:** {self.format_size(optimization_result.original_size)}")
        report.append(f"**Estimated Optimized Size:** {self.format_size(optimization_result.optimized_size)}")
        report.append(f"**Size Reduction:** {optimization_result.size_reduction:.1f}%")
        report.append("")

        if optimization_result.optimizations_applied:
            report.append("### Applied Optimizations")
            for opt in optimization_result.optimizations_applied:
                report.append(f"- {opt}")
            report.append("")

        # Recommendations
        if optimization_result.recommendations:
            report.append("## 💡 Code Splitting Recommendations")
            for rec in optimization_result.recommendations:
                report.append(f"- {rec}")
            report.append("")

        # Next Steps
        report.append("## 🚀 Next Steps")
        report.append("1. Run `npm run build` to generate optimized bundle")
        report.append("2. Analyze the bundle with `ANALYZE=true npm run build`")
        report.append("3. Test application functionality")
        report.append("4. Monitor bundle size in production")
        report.append("5. Set up bundle size monitoring in CI/CD")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Bundle Optimizer for Developer Portfolios')
    parser.add_argument('project_path', help='Path to Next.js project')
    parser.add_argument('--analyze', action='store_true', help='Analyze current bundle')
    parser.add_argument('--optimize', action='store_true', help='Apply optimizations')
    parser.add_argument('--dry-run', action='store_true', help='Show optimizations without applying')
    parser.add_argument('--output', help='Output directory for reports')

    args = parser.parse_args()

    if not args.project_path:
        print("❌ Project path is required")
        sys.exit(1)

    # Initialize optimizer
    optimizer = BundleOptimizer(args.project_path)

    if args.analyze or args.optimize:
        # Analyze current bundle
        analysis = optimizer.analyze_current_bundle()
        print(f"📊 Current bundle size: {optimizer.format_size(analysis.total_size)}")

        if args.optimize:
            # Apply optimizations
            result = optimizer.apply_optimizations(dry_run=args.dry_run)

            # Generate report
            report = optimizer.generate_optimization_report(analysis, result)

            if args.output:
                output_path = Path(args.output) / 'bundle_optimization_report.md'
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(report, encoding='utf-8')
                print(f"📄 Report saved to: {output_path}")
            else:
                print("\n" + report)

            if not args.dry_run:
                print("✅ Optimizations applied successfully!")
            else:
                print("🔍 Dry run completed. Use --optimize to apply changes.")
        else:
            # Just show analysis
            print(f"📦 Found {len(analysis.chunks)} chunks")
            print(f"📚 {len(analysis.dependencies)} dependencies")

            if analysis.optimization_opportunities:
                print("\n🎯 Optimization opportunities:")
                for opportunity in analysis.optimization_opportunities:
                    print(f"  - {opportunity}")
    else:
        print("Use --analyze to inspect current bundle or --optimize to apply optimizations")

if __name__ == "__main__":
    main()