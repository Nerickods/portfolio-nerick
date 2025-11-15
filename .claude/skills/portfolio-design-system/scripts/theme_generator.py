#!/usr/bin/env python3
"""
Portfolio Design System - Theme Generator

Generates professional color schemes optimized for developer portfolios
with accessibility compliance and tech personality alignment.
"""

import json
import math
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ColorSet:
    """Represents a complete color set for a theme"""
    primary: List[str]
    secondary: List[str]
    neutral: List[str]
    semantic: Dict[str, List[str]]
    tech_colors: Dict[str, str]


class ThemeGenerator:
    """Professional theme generator for developer portfolios"""

    # Tech personality color profiles
    PERSONALITY_PROFILES = {
        'innovative': {
            'primary_hue': 220,  # Blue-purple
            'saturation': 0.75,
            'personality': 'forward-thinking, creative, modern'
        },
        'reliable': {
            'primary_hue': 200,  # Stable blue
            'saturation': 0.65,
            'personality': 'trustworthy, professional, consistent'
        },
        'bold': {
            'primary_hue': 0,    # Red
            'saturation': 0.8,
            'personality': 'confident, impactful, energetic'
        },
        'minimal': {
            'primary_hue': 180,  # Teal
            'saturation': 0.5,
            'personality': 'clean, focused, elegant'
        },
        'creative': {
            'primary_hue': 280,  # Purple
            'saturation': 0.7,
            'personality': 'artistic, imaginative, unique'
        }
    }

    # Technology color associations
    TECH_COLORS = {
        'javascript': '#F7DF1E',
        'typescript': '#3178C6',
        'react': '#61DAFB',
        'vue': '#4FC08D',
        'angular': '#DD0031',
        'nodejs': '#339933',
        'python': '#3776AB',
        'java': '#007396',
        'cpp': '#00599C',
        'rust': '#000000',
        'go': '#00ADD8',
        'swift': '#FA7343',
        'kotlin': '#7F52FF',
        'php': '#777BB4',
        'ruby': '#CC342D',
        'docker': '#2496ED',
        'kubernetes': '#326CE5',
        'aws': '#FF9900',
        'azure': '#0078D4',
        'gcp': '#4285F4',
        'html': '#E34F26',
        'css': '#1572B6',
        'sass': '#CC6699',
        'webpack': '#8DD6F9',
        'babel': '#F5DA55',
        'git': '#F05032',
        'github': '#181717',
        'linux': '#FCC624',
        'ubuntu': '#E95420',
        'mongodb': '#47A248',
        'postgresql': '#336791',
        'mysql': '#4479A1',
        'redis': '#DC382D',
        'graphql': '#E10098'
    }

    def __init__(self):
        self.contrast_ratios = {
            'AAA': 7.0,
            'AA': 4.5,
            'AA_large': 3.0
        }

    def hsl_to_rgb(self, h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL to RGB color space"""
        h = h / 360
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0: t += 1
                if t > 1: t -= 1
                if t < 1/6: return p + (q - p) * 6 * t
                if t < 1/2: return q
                if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                return p

            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)

        return (int(r * 255), int(g * 255), int(b * 255))

    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hexadecimal color"""
        return f"#{r:02x}{g:02x}{b:02x}"

    def calculate_luminance(self, r: int, g: int, b: int) -> float:
        """Calculate relative luminance of a color"""
        def normalize(c: int) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

        r_norm = normalize(r)
        g_norm = normalize(g)
        b_norm = normalize(b)

        return 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

    def calculate_contrast(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)

        l1 = self.calculate_luminance(r1, g1, b1)
        l2 = self.calculate_luminance(r2, g2, b2)

        lighter = max(l1, l2)
        darker = min(l1, l2)

        return (lighter + 0.05) / (darker + 0.05)

    def generate_color_scale(self, hue: float, saturation: float, steps: int = 9) -> List[str]:
        """Generate a color scale with consistent lightness values"""
        colors = []

        # Lightness values for consistent visual steps
        lightness_values = [0.95, 0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25, 0.15]

        for i in range(steps):
            lightness = lightness_values[i]
            r, g, b = self.hsl_to_rgb(hue, saturation, lightness)
            colors.append(self.rgb_to_hex(r, g, b))

        return colors

    def generate_complementary_color(self, hue: float, saturation: float) -> float:
        """Generate a complementary hue"""
        return (hue + 180) % 360

    def generate_analogous_colors(self, hue: float, count: int = 2) -> List[float]:
        """Generate analogous colors"""
        return [(hue + (30 * i)) % 360 for i in range(-count//2, count//2 + 1) if i != 0]

    def generate_semantic_colors(self, base_hue: float) -> Dict[str, List[str]]:
        """Generate semantic colors (success, warning, error, info)"""
        semantic_hues = {
            'success': 120,   # Green
            'warning': 45,    # Orange/Yellow
            'error': 0,       # Red
            'info': 200       # Blue
        }

        semantic_colors = {}
        for name, hue in semantic_hues.items():
            semantic_colors[name] = self.generate_color_scale(hue, 0.7, 5)

        return semantic_colors

    def generate_neutral_colors(self) -> List[str]:
        """Generate neutral gray color scale"""
        return [
            '#ffffff', '#fafafa', '#f5f5f5', '#e5e5e5', '#d4d4d4',
            '#a3a3a3', '#737373', '#525252', '#404040', '#262626',
            '#171717', '#0a0a0a'
        ]

    def generate_theme(self, personality: str, name: str = None) -> Dict:
        """Generate a complete theme based on personality profile"""
        if personality not in self.PERSONALITY_PROFILES:
            raise ValueError(f"Unknown personality: {personality}. Available: {list(self.PERSONALITY_PROFILES.keys())}")

        profile = self.PERSONALITY_PROFILES[personality]
        base_hue = profile['primary_hue']
        saturation = profile['saturation']

        # Generate color sets
        primary_colors = self.generate_color_scale(base_hue, saturation)

        # Generate secondary (complementary or analogous)
        complementary_hue = self.generate_complementary_color(base_hue, saturation)
        secondary_colors = self.generate_color_scale(complementary_hue, saturation * 0.8)

        # Generate neutrals
        neutral_colors = self.generate_neutral_colors()

        # Generate semantic colors
        semantic_colors = self.generate_semantic_colors(base_hue)

        # Theme metadata
        theme_name = name or f"{personality.capitalize()} Theme"

        theme = {
            'name': theme_name,
            'personality': personality,
            'description': f"Professional theme with a {profile['personality']} personality",
            'colors': {
                'primary': primary_colors,
                'secondary': secondary_colors,
                'neutral': neutral_colors,
                'semantic': semantic_colors,
                'tech': self.TECH_COLORS
            },
            'typography': {
                'font_family': {
                    'sans': ['Inter', 'system-ui', 'sans-serif'],
                    'serif': ['Merriweather', 'Georgia', 'serif'],
                    'mono': ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace']
                },
                'scale': {
                    'xs': '0.75rem',
                    'sm': '0.875rem',
                    'base': '1rem',
                    'lg': '1.125rem',
                    'xl': '1.25rem',
                    '2xl': '1.5rem',
                    '3xl': '1.875rem',
                    '4xl': '2.25rem',
                    '5xl': '3rem'
                }
            },
            'spacing': {
                'scale': [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128],
                'container_max_widths': {
                    'sm': '640px',
                    'md': '768px',
                    'lg': '1024px',
                    'xl': '1280px',
                    '2xl': '1536px'
                }
            },
            'breakpoints': {
                'sm': '640px',
                'md': '768px',
                'lg': '1024px',
                'xl': '1280px',
                '2xl': '1536px'
            }
        }

        # Validate accessibility
        accessibility_report = self.validate_accessibility(theme)
        theme['accessibility'] = accessibility_report

        return theme

    def validate_accessibility(self, theme: Dict) -> Dict:
        """Validate theme colors for accessibility compliance"""
        report = {
            'compliance_level': 'AA',
            'issues': [],
            'recommendations': []
        }

        # Check primary colors against neutrals
        primary_colors = theme['colors']['primary']
        neutral_colors = theme['colors']['neutral']

        # Test key combinations
        test_combinations = [
            (primary_colors[5], neutral_colors[0]),  # Primary on white
            (primary_colors[5], neutral_colors[-1]), # Primary on black
            (neutral_colors[-2], neutral_colors[0]), # Dark text on white
            (neutral_colors[0], neutral_colors[-1]), # White text on black
        ]

        for foreground, background in test_combinations:
            contrast = self.calculate_contrast(foreground, background)

            if contrast < self.contrast_ratios['AA']:
                report['issues'].append({
                    'type': 'contrast_failure',
                    'foreground': foreground,
                    'background': background,
                    'contrast_ratio': round(contrast, 2),
                    'required': self.contrast_ratios['AA']
                })
                report['recommendations'].append(
                    f"Adjust contrast between {foreground} and {background}"
                )

        if not report['issues']:
            report['compliance_level'] = 'AAA' if all(
                self.calculate_contrast(fg, bg) >= self.contrast_ratios['AAA']
                for fg, bg in test_combinations[:2]
            ) else 'AA'

        return report

    def generate_css_variables(self, theme: Dict) -> str:
        """Generate CSS custom properties for the theme"""
        css_vars = []
        colors = theme['colors']

        # Primary colors
        for i, color in enumerate(colors['primary']):
            css_vars.append(f"  --color-primary-{i+1}: {color};")

        # Secondary colors
        for i, color in enumerate(colors['secondary']):
            css_vars.append(f"  --color-secondary-{i+1}: {color};")

        # Neutral colors
        for i, color in enumerate(colors['neutral']):
            css_vars.append(f"  --color-neutral-{i}: {color};")

        # Semantic colors
        for semantic_type, color_list in colors['semantic'].items():
            for i, color in enumerate(color_list):
                css_vars.append(f"  --color-{semantic_type}-{i+1}: {color};")

        # Typography
        for scale, value in theme['typography']['scale'].items():
            css_vars.append(f"  --font-size-{scale}: {value};")

        # Spacing
        for i, value in enumerate(theme['spacing']['scale']):
            css_vars.append(f"  --spacing-{i}: {value}px;")

        return ":root {\n" + "\n".join(css_vars) + "\n}"

    def generate_tailwind_config(self, theme: Dict) -> Dict:
        """Generate Tailwind CSS color configuration"""
        colors = theme['colors']

        tailwind_colors = {
            'primary': {},
            'secondary': {},
            'neutral': {},
            'success': {},
            'warning': {},
            'error': {},
            'info': {},
            'tech': colors['tech']
        }

        # Map color scales to Tailwind format
        scale_names = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']

        for i, color in enumerate(colors['primary'][:9]):
            tailwind_colors['primary'][scale_names[i]] = color

        for i, color in enumerate(colors['secondary'][:9]):
            tailwind_colors['secondary'][scale_names[i]] = color

        for i, color in enumerate(colors['neutral'][:12]):
            if i < len(scale_names):
                tailwind_colors['neutral'][scale_names[i]] = color

        # Semantic colors
        for semantic_type, color_list in colors['semantic'].items():
            for i, color in enumerate(color_list):
                if i < len(scale_names):
                    tailwind_colors[semantic_type][scale_names[i]] = color

        return {
            'theme': {
                'extend': {
                    'colors': tailwind_colors,
                    'fontFamily': theme['typography']['font_family'],
                    'fontSize': theme['typography']['scale'],
                    'spacing': {str(i): f"{i}px" for i in theme['spacing']['scale']},
                    'maxWidth': theme['spacing']['container_max_widths']
                }
            }
        }

    def save_theme(self, theme: Dict, output_dir: str, format: str = 'json'):
        """Save theme in specified format"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        theme_name = theme['name'].lower().replace(' ', '-')

        if format == 'json':
            # Save as JSON
            json_file = output_path / f"{theme_name}.json"
            with open(json_file, 'w') as f:
                json.dump(theme, f, indent=2)

            # Save CSS variables
            css_file = output_path / f"{theme_name}.css"
            css_vars = self.generate_css_variables(theme)
            with open(css_file, 'w') as f:
                f.write("/* Theme CSS Variables */\n\n")
                f.write(css_vars)

            # Save Tailwind config
            tailwind_file = output_path / f"{theme_name}-tailwind.json"
            tailwind_config = self.generate_tailwind_config(theme)
            with open(tailwind_file, 'w') as f:
                json.dump(tailwind_config, f, indent=2)

            print(f"Theme saved to {output_path}")
            print(f"  - JSON: {json_file}")
            print(f"  - CSS: {css_file}")
            print(f"  - Tailwind: {tailwind_file}")

        else:
            raise ValueError(f"Unsupported format: {format}")


def main():
    parser = argparse.ArgumentParser(description='Generate professional portfolio themes')
    parser.add_argument('--personality', choices=list(ThemeGenerator.PERSONALITY_PROFILES.keys()),
                       required=True, help='Theme personality profile')
    parser.add_argument('--name', help='Custom theme name')
    parser.add_argument('--output', default='./themes', help='Output directory')
    parser.add_argument('--format', choices=['json'], default='json', help='Output format')
    parser.add_argument('--validate-only', action='store_true', help='Only validate accessibility')

    args = parser.parse_args()

    generator = ThemeGenerator()

    try:
        theme = generator.generate_theme(args.personality, args.name)

        if args.validate_only:
            print("Accessibility Report:")
            print(json.dumps(theme['accessibility'], indent=2))
        else:
            generator.save_theme(theme, args.output, args.format)
            print(f"\nTheme: {theme['name']}")
            print(f"Personality: {theme['description']}")
            print(f"Accessibility Compliance: {theme['accessibility']['compliance_level']}")

            if theme['accessibility']['issues']:
                print(f"\n⚠️  Accessibility Issues Found: {len(theme['accessibility']['issues'])}")
                for issue in theme['accessibility']['issues']:
                    print(f"  - {issue['foreground']} on {issue['background']}: {issue['contrast_ratio']}:1 (minimum {issue['required']}:1)")
            else:
                print("✅ All color combinations pass accessibility standards")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())