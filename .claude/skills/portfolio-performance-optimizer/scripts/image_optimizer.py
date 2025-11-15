#!/usr/bin/env python3
"""
Image Optimizer for Developer Portfolios
Optimizes images with modern formats, responsive strategies, and portfolio-specific enhancements
"""

import json
import os
import sys
import argparse
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageOps
import dataclasses
import concurrent.futures

@dataclasses.dataclass
class ImageMetrics:
    """Image metrics data structure"""
    original_size: int
    optimized_size: int
    size_reduction: float
    original_format: str
    optimized_format: str
    dimensions: Tuple[int, int]
    file_hash: str
    optimization_level: str

@dataclasses.dataclass
class OptimizationResult:
    """Image optimization result structure"""
    total_images: int
    successfully_optimized: int
    total_size_saved: int
    average_size_reduction: float
    formats_converted: List[str]
    recommendations: List[str]
    responsive_images_generated: int
    critical_images_detected: List[str]

class ImageOptimizer:
    """Main image optimizer class for developer portfolios"""

    def __init__(self, project_path: str, output_dir: str = "./optimized_images"):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Portfolio-specific optimization settings
        self.portfolio_image_types = {
            'profile': {'max_width': 400, 'quality': 85, 'priority': 'high'},
            'project_screenshot': {'max_width': 1200, 'quality': 80, 'priority': 'medium'},
            'thumbnail': {'max_width': 300, 'quality': 75, 'priority': 'low'},
            'hero': {'max_width': 1920, 'quality': 85, 'priority': 'high'},
            'gallery': {'max_width': 800, 'quality': 82, 'priority': 'medium'},
        }

        # Supported formats and their priority
        self.format_priority = {
            'AVIF': 1,
            'WebP': 2,
            'JPEG': 3,
            'PNG': 4,
            'GIF': 5
        }

        # Common portfolio image patterns
        self.portfolio_patterns = {
            'profile': ['profile', 'avatar', 'me', 'photo', 'headshot'],
            'project': ['project', 'screenshot', 'demo', 'preview'],
            'hero': ['hero', 'banner', 'header', 'cover'],
            'thumbnail': ['thumb', 'thumbnail', 'small', 'mini'],
        }

    def find_images(self) -> List[Path]:
        """Find all images in the project"""
        print("🔍 Scanning for images...")

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        images = []

        for ext in image_extensions:
            images.extend(self.project_path.rglob(f'*{ext}'))
            images.extend(self.project_path.rglob(f'*{ext.upper()}'))

        # Exclude node_modules and .next
        images = [
            img for img in images
            if 'node_modules' not in str(img) and '.next' not in str(img)
        ]

        print(f"📸 Found {len(images)} images")
        return images

    def classify_image(self, image_path: Path) -> str:
        """Classify image type based on filename and path"""
        path_str = str(image_path).lower()

        for image_type, patterns in self.portfolio_patterns.items():
            if any(pattern in path_str for pattern in patterns):
                return image_type

        # Fallback classification based on size and location
        if any(folder in path_str for folder in ['profile', 'about', 'me']):
            return 'profile'
        elif any(folder in path_str for folder in ['projects', 'work', 'portfolio']):
            return 'project_screenshot'
        elif any(folder in path_str for folder in ['hero', 'banner']):
            return 'hero'
        elif any(folder in path_str for folder in ['thumb', 'small']):
            return 'thumbnail'

        return 'gallery'  # Default type

    def get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file comparison"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def optimize_single_image(self, image_path: Path) -> Optional[ImageMetrics]:
        """Optimize a single image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                # Classify image and get optimization settings
                image_type = self.classify_image(image_path)
                settings = self.portfolio_image_types.get(image_type, self.portfolio_image_types['gallery'])

                # Calculate new dimensions
                original_width, original_height = img.size
                max_width = settings['max_width']

                if original_width > max_width:
                    ratio = max_width / original_width
                    new_height = int(original_height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # Generate optimized formats
                original_format = image_path.suffix.upper().replace('.', '')
                best_format = self.select_best_format(img, image_type)

                # Create output path
                output_path = self.output_dir / f"{image_path.stem}_{best_format.lower()}.{best_format.lower()}"

                # Save optimized image
                if best_format.upper() == 'AVIF':
                    img.save(output_path, 'AVIF', quality=settings['quality'], speed=6)
                elif best_format.upper() == 'WEBP':
                    img.save(output_path, 'WEBP', quality=settings['quality'], method=6)
                elif best_format.upper() == 'JPEG':
                    img.save(output_path, 'JPEG', quality=settings['quality'], optimize=True)
                else:
                    img.save(output_path, best_format.upper(), optimize=True)

                # Calculate metrics
                original_size = image_path.stat().st_size
                optimized_size = output_path.stat().st_size
                size_reduction = (original_size - optimized_size) / original_size * 100

                return ImageMetrics(
                    original_size=original_size,
                    optimized_size=optimized_size,
                    size_reduction=size_reduction,
                    original_format=original_format,
                    optimized_format=best_format,
                    dimensions=img.size,
                    file_hash=self.get_file_hash(image_path),
                    optimization_level=settings['priority']
                )

        except Exception as e:
            print(f"❌ Error optimizing {image_path}: {e}")
            return None

    def select_best_format(self, img: Image.Image, image_type: str) -> str:
        """Select the best format for an image"""
        # Try to use AVIF for high-quality images
        if image_type in ['hero', 'project_screenshot'] and self.has_avif_support():
            return 'AVIF'

        # Use WebP for most cases
        if self.has_webp_support():
            return 'WebP'

        # Fallback to JPEG for photographs, PNG for graphics
        return 'JPEG' if image_type not in ['profile'] else 'PNG'

    def has_avif_support(self) -> bool:
        """Check if AVIF encoding is available"""
        try:
            from PIL import Image
            test_img = Image.new('RGB', (100, 100))
            test_img.save('/tmp/test.avif', 'AVIF')
            os.remove('/tmp/test.avif')
            return True
        except:
            return False

    def has_webp_support(self) -> bool:
        """Check if WebP encoding is available"""
        try:
            from PIL import Image
            test_img = Image.new('RGB', (100, 100))
            test_img.save('/tmp/test.webp', 'WEBP')
            os.remove('/tmp/test.webp')
            return True
        except:
            return False

    def generate_responsive_images(self, image_path: Path, image_type: str) -> List[Dict[str, Any]]:
        """Generate responsive image variants"""
        responsive_variants = []

        # Define breakpoints for portfolio images
        if image_type == 'hero':
            sizes = [640, 768, 1024, 1280, 1536]
        elif image_type == 'project_screenshot':
            sizes = [400, 800, 1200]
        elif image_type == 'thumbnail':
            sizes = [150, 300]
        else:
            sizes = [400, 800]

        try:
            with Image.open(image_path) as img:
                original_width, original_height = img.size

                for size in sizes:
                    if original_width <= size:
                        continue

                    ratio = size / original_width
                    new_height = int(original_height * ratio)
                    resized_img = img.resize((size, new_height), Image.Resampling.LANCZOS)

                    # Save variant
                    variant_path = self.output_dir / f"{image_path.stem}_{size}w.webp"
                    resized_img.save(variant_path, 'WEBP', quality=80, method=6)

                    responsive_variants.append({
                        'width': size,
                        'height': new_height,
                        'path': str(variant_path),
                        'size': variant_path.stat().st_size
                    })

        except Exception as e:
            print(f"❌ Error generating responsive images for {image_path}: {e}")

        return responsive_variants

    def detect_critical_images(self) -> List[str]:
        """Detect critical above-the-fold images for portfolios"""
        critical_patterns = [
            'hero', 'banner', 'header', 'profile', 'avatar',
            'about', 'intro', 'welcome'
        ]

        critical_images = []
        for pattern in critical_patterns:
            critical_images.extend(
                str(img) for img in self.project_path.rglob('*')
                if pattern in str(img).lower() and img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']
            )

        return list(set(critical_images))

    def optimize_all_images(self, parallel: bool = True) -> OptimizationResult:
        """Optimize all images in the project"""
        images = self.find_images()

        if not images:
            return OptimizationResult(
                total_images=0,
                successfully_optimized=0,
                total_size_saved=0,
                average_size_reduction=0,
                formats_converted=[],
                recommendations=[],
                responsive_images_generated=0,
                critical_images_detected=[]
            )

        print(f"🚀 Optimizing {len(images)} images...")

        optimized_images = []
        total_size_saved = 0
        formats_converted = set()
        responsive_count = 0

        # Process images
        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(self.optimize_single_image, img): img for img in images}

                for future in concurrent.futures.as_completed(futures):
                    img_path = futures[future]
                    result = future.result()
                    if result:
                        optimized_images.append((img_path, result))
                        total_size_saved += result.original_size - result.optimized_size
                        formats_converted.add(f"{result.original_format}→{result.optimized_format}")

                        # Generate responsive images for important types
                        image_type = self.classify_image(img_path)
                        if image_type in ['hero', 'project_screenshot']:
                            variants = self.generate_responsive_images(img_path, image_type)
                            responsive_count += len(variants)

                        print(f"✅ {img_path.name}: {result.size_reduction:.1f}% reduction")
        else:
            for img_path in images:
                result = self.optimize_single_image(img_path)
                if result:
                    optimized_images.append((img_path, result))
                    total_size_saved += result.original_size - result.optimized_size
                    formats_converted.add(f"{result.original_format}→{result.optimized_format}")
                    print(f"✅ {img_path.name}: {result.size_reduction:.1f}% reduction")

        # Calculate metrics
        avg_reduction = sum(r.size_reduction for _, r in optimized_images) / len(optimized_images) if optimized_images else 0

        # Detect critical images
        critical_images = self.detect_critical_images()

        # Generate recommendations
        recommendations = self.generate_recommendations(optimized_images)

        return OptimizationResult(
            total_images=len(images),
            successfully_optimized=len(optimized_images),
            total_size_saved=total_size_saved,
            average_size_reduction=avg_reduction,
            formats_converted=list(formats_converted),
            recommendations=recommendations,
            responsive_images_generated=responsive_count,
            critical_images_detected=critical_images
        )

    def generate_recommendations(self, optimized_images: List[Tuple[Path, ImageMetrics]]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Format recommendations
        if len(optimized_images) > 0:
            formats_used = set(r.optimized_format for _, r in optimized_images)
            if 'AVIF' not in formats_used:
                recommendations.append("Consider using AVIF format for better compression (30% smaller than WebP)")
            if 'WebP' not in formats_used:
                recommendations.append("Convert remaining images to WebP format for 25-35% size reduction")

        # Large image recommendations
        large_images = [r for _, r in optimized_images if r.optimized_size > 500 * 1024]  # 500KB
        if large_images:
            recommendations.append(f"Found {len(large_images)} large images (>500KB) - consider further compression or lazy loading")

        # Critical images recommendations
        critical_images = self.detect_critical_images()
        if critical_images:
            recommendations.append(f"Preload {len(critical_images)} critical above-the-fold images for better LCP")

        # Responsive images
        recommendations.append("Implement responsive images with srcset for different viewport sizes")
        recommendations.append("Use blur-up placeholder technique for better user experience")

        # Next.js Image component
        recommendations.append("Use Next.js Image component for automatic optimization and lazy loading")

        return recommendations

    def generate_nextjs_image_config(self) -> str:
        """Generate Next.js image configuration"""
        config = '''
// Image optimization configuration for portfolios
import { createMDX } from 'next-mdx-imports/file-path'

export const imageConfig = {
  // Default image loader
  loader: 'default',

  // Image domains (add your domains here)
  domains: [
    'localhost',
    'your-domain.com',
    'cdn.your-domain.com'
  ],

  // Image formats (Next.js will automatically choose the best format)
  formats: ['image/avif', 'image/webp'],

  // Device sizes for responsive images
  deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],

  // Image sizes to generate
  imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

  // Quality settings
  quality: 80,

  // Minimum cache TTL (1 year)
  minimumCacheTTL: 31536000,

  // Enable SVG support
  dangerouslyAllowSVG: true,

  // Content Security Policy for SVGs
  contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
}

// Portfolio-specific image loader
export const portfolioLoader = ({ src, width, quality }) => {
  return `https://your-cdn.com/images/${src}?w=${width}&q=${quality || 80}&fm=webp`
}

// Critical images for preloading
export const criticalImages = [
  '/images/hero-banner.webp',
  '/images/profile-photo.webp',
]

// Image optimization utilities
export const optimizeForPortfolio = {
  // Profile picture optimization
  profile: {
    width: 400,
    height: 400,
    quality: 85,
    priority: true,
    placeholder: 'blur',
  },

  // Project screenshot optimization
  project: {
    width: 1200,
    height: 800,
    quality: 80,
    priority: false,
    placeholder: 'blur',
  },

  // Hero image optimization
  hero: {
    width: 1920,
    height: 1080,
    quality: 85,
    priority: true,
    placeholder: 'blur',
  },

  // Gallery image optimization
  gallery: {
    width: 800,
    height: 600,
    quality: 82,
    priority: false,
    placeholder: 'blur',
  },
}
'''

        return config

    def generate_optimization_report(self, result: OptimizationResult) -> str:
        """Generate comprehensive image optimization report"""
        report = []

        report.append("# Image Optimization Report")
        report.append("")

        # Summary
        report.append("## 📊 Optimization Summary")
        report.append(f"**Total Images Processed:** {result.total_images}")
        report.append(f"**Successfully Optimized:** {result.successfully_optimized}")
        report.append(f"**Total Size Saved:** {self.format_size(result.total_size_saved)}")
        report.append(f"**Average Size Reduction:** {result.average_size_reduction:.1f}%")
        report.append(f"**Responsive Images Generated:** {result.responsive_images_generated}")
        report.append(f"**Critical Images Detected:** {len(result.critical_images_detected)}")
        report.append("")

        # Format Conversions
        if result.formats_converted:
            report.append("## 🔄 Format Conversions")
            for conversion in result.formats_converted:
                report.append(f"- {conversion}")
            report.append("")

        # Critical Images
        if result.critical_images_detected:
            report.append("## ⚡ Critical Above-the-Fold Images")
            for critical in result.critical_images_detected[:10]:  # Show first 10
                report.append(f"- `{critical}`")
            if len(result.critical_images_detected) > 10:
                report.append(f"- ... and {len(result.critical_images_detected) - 10} more")
            report.append("")

        # Recommendations
        if result.recommendations:
            report.append("## 💡 Optimization Recommendations")
            for rec in result.recommendations:
                report.append(f"- {rec}")
            report.append("")

        # Next Steps
        report.append("## 🚀 Next Steps")
        report.append("1. Replace original images with optimized versions")
        report.append("2. Update image references to use new formats")
        report.append("3. Implement responsive images with srcset")
        report.append("4. Preload critical images for better LCP")
        report.append("5. Set up CDN for image delivery")
        report.append("6. Monitor image performance in production")

        return "\n".join(report)

    def format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} GB"

def main():
    parser = argparse.ArgumentParser(description='Image Optimizer for Developer Portfolios')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--output', default='./optimized_images', help='Output directory for optimized images')
    parser.add_argument('--parallel', action='store_true', default=True, help='Use parallel processing')
    parser.add_argument('--report', help='Save optimization report to file')
    parser.add_argument('--critical-only', action='store_true', help='Only optimize critical images')

    args = parser.parse_args()

    # Initialize optimizer
    optimizer = ImageOptimizer(args.project_path, args.output)

    # Run optimization
    result = optimizer.optimize_all_images(parallel=args.parallel)

    # Print summary
    print(f"\n🎯 Optimization Complete!")
    print(f"📸 Processed: {result.total_images} images")
    print(f"✅ Optimized: {result.successfully_optimized} images")
    print(f"💾 Space saved: {optimizer.format_size(result.total_size_saved)}")
    print(f"📈 Avg reduction: {result.average_size_reduction:.1f}%")

    # Generate report
    report = optimizer.generate_optimization_report(result)

    if args.report:
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"📄 Report saved to: {args.report}")
    else:
        print("\n" + report)

if __name__ == "__main__":
    main()