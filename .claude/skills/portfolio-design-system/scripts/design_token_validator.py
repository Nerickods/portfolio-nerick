#!/usr/bin/env python3
"""
Portfolio Design System - Design Token Validator

Validates design tokens against consistency standards, accessibility requirements,
and best practices for professional design systems.
"""

import json
import re
import math
import argparse
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    level: ValidationLevel
    category: str
    message: str
    token_path: str
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report"""
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    passed: bool = True

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)
        if issue.level == ValidationLevel.ERROR:
            self.passed = False

    def get_summary(self) -> Dict[str, int]:
        summary = {"error": 0, "warning": 0, "info": 0}
        for issue in self.issues:
            summary[issue.level.value] += 1
        return summary


class DesignTokenValidator:
    """Validates design tokens against standards and best practices"""

    def __init__(self):
        self.report = ValidationReport()

        # Standard spacing scale (8-point grid)
        self.spacing_scale = [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256]

        # Standard font sizes (modular scale)
        self.typographic_scale = {
            'xs': 0.75,    # 12px
            'sm': 0.875,   # 14px
            'base': 1.0,   # 16px
            'lg': 1.125,   # 18px
            'xl': 1.25,    # 20px
            '2xl': 1.5,    # 24px
            '3xl': 1.875,  # 30px
            '4xl': 2.25,   # 36px
            '5xl': 3.0,    # 48px
            '6xl': 3.75,   # 60px
            '7xl': 4.5,    # 72px
        }

        # Standard breakpoints
        self.breakpoints = {
            'sm': 640,
            'md': 768,
            'lg': 1024,
            'xl': 1280,
            '2xl': 1536
        }

        # Standard border radius values
        self.border_radius_scale = [0, 2, 4, 6, 8, 12, 16, 24, 32]

        # Standard z-index scale
        self.z_index_scale = {
            'hide': -1,
            'auto': 0,
            'base': 10,
            'dock': 20,
            'dropdown': 30,
            'sticky': 40,
            'banner': 50,
            'overlay': 60,
            'modal': 70,
            'popover': 80,
            'skiplink': 90,
            'toast': 100,
            'tooltip': 110
        }

    def validate_colors(self, colors: Dict, path: str = "colors") -> None:
        """Validate color tokens"""

        # Check for required color categories
        required_categories = ['primary', 'secondary', 'neutral']
        for category in required_categories:
            if category not in colors:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="colors",
                    message=f"Missing required color category: {category}",
                    token_path=f"{path}.{category}",
                    suggestion=f"Add {category} color scale with 9 shades (50-900)"
                ))

        # Validate color scales
        for color_name, color_value in colors.items():
            color_path = f"{path}.{color_name}"

            if color_name in ['primary', 'secondary', 'neutral']:
                self._validate_color_scale(color_value, color_path)
            elif isinstance(color_value, dict):
                # Check for semantic colors
                self._validate_semantic_colors(color_value, color_path)
            elif color_name == 'tech':
                self._validate_tech_colors(color_value, color_path)

    def _validate_color_scale(self, color_scale: Any, path: str) -> None:
        """Validate individual color scale"""
        if not isinstance(color_scale, dict):
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="colors",
                message=f"Color scale must be a dictionary",
                token_path=path,
                suggestion="Use object with shade keys (50, 100, 200, ..., 900)"
            ))
            return

        # Check for required shades
        required_shades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']
        missing_shades = [shade for shade in required_shades if shade not in color_scale]

        if missing_shades:
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.WARNING,
                category="colors",
                message=f"Missing color shades: {', '.join(missing_shades)}",
                token_path=path,
                suggestion=f"Add missing shades: {', '.join(missing_shades)}"
            ))

        # Validate color format and contrast
        for shade, hex_color in color_scale.items():
            shade_path = f"{path}.{shade}"

            if not self._is_valid_hex_color(hex_color):
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="colors",
                    message=f"Invalid hex color format: {hex_color}",
                    token_path=shade_path,
                    suggestion="Use valid 6-character hex color (e.g., #3B82F6)"
                ))

    def _validate_semantic_colors(self, semantic_colors: Dict, path: str) -> None:
        """Validate semantic color tokens"""
        expected_semantic = ['success', 'warning', 'error', 'info']

        for semantic_type in expected_semantic:
            if semantic_type not in semantic_colors:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="colors",
                    message=f"Missing semantic color: {semantic_type}",
                    token_path=f"{path}.{semantic_type}",
                    suggestion=f"Add {semantic_type} color scale for consistent UI states"
                ))

    def _validate_tech_colors(self, tech_colors: Dict, path: str) -> None:
        """Validate technology color associations"""
        expected_tech = [
            'javascript', 'typescript', 'react', 'vue', 'angular',
            'nodejs', 'python', 'java', 'docker', 'git', 'github'
        ]

        missing_tech = [tech for tech in expected_tech if tech not in tech_colors]

        if missing_tech:
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.INFO,
                category="colors",
                message=f"Missing tech colors: {', '.join(missing_tech)}",
                token_path=path,
                suggestion=f"Consider adding colors for: {', '.join(missing_tech)}"
            ))

    def _is_valid_hex_color(self, color: str) -> bool:
        """Check if string is a valid hex color"""
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color))

    def validate_typography(self, typography: Dict, path: str = "typography") -> None:
        """Validate typography tokens"""

        # Check font families
        if 'font_family' not in typography:
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="typography",
                message="Missing font family definitions",
                token_path=f"{path}.font_family",
                suggestion="Define font families for sans, serif, and mono fonts"
            ))
        else:
            self._validate_font_families(typography['font_family'], f"{path}.font_family")

        # Check font sizes
        if 'scale' not in typography:
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="typography",
                message="Missing font size scale",
                token_path=f"{path}.scale",
                suggestion="Define modular scale for font sizes (xs to 7xl)"
            ))
        else:
            self._validate_font_scale(typography['scale'], f"{path}.scale")

    def _validate_font_families(self, font_families: Dict, path: str) -> None:
        """Validate font family definitions"""
        required_families = ['sans', 'serif', 'mono']

        for family in required_families:
            if family not in font_families:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="typography",
                    message=f"Missing font family: {family}",
                    token_path=f"{path}.{family}",
                    suggestion=f"Add {family} font stack with fallbacks"
                ))
            else:
                font_stack = font_families[family]
                if not isinstance(font_stack, list) or len(font_stack) < 2:
                    self.report.add_issue(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="typography",
                        message=f"Font family '{family}' should have multiple fonts for fallback",
                        token_path=f"{path}.{family}",
                        suggestion=f"Include fallback fonts (e.g., ['Inter', 'system-ui', 'sans-serif'])"
                    ))

    def _validate_font_scale(self, font_scale: Dict, path: str) -> None:
        """Validate font size scale"""
        required_sizes = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl']

        for size in required_sizes:
            if size not in font_scale:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="typography",
                    message=f"Missing font size: {size}",
                    token_path=f"{path}.{size}",
                    suggestion=f"Add {size} font size to maintain consistent scale"
                ))

    def validate_spacing(self, spacing: Dict, path: str = "spacing") -> None:
        """Validate spacing tokens"""

        if 'scale' not in spacing:
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="spacing",
                message="Missing spacing scale",
                token_path=f"{path}.scale",
                suggestion="Define 8-point grid spacing scale"
            ))
            return

        scale = spacing['scale']
        if not isinstance(scale, list):
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="spacing",
                message="Spacing scale must be an array",
                token_path=f"{path}.scale",
                suggestion="Use array of numbers following 8-point grid"
            ))
            return

        # Validate 8-point grid adherence
        for i, value in enumerate(scale):
            if value not in self.spacing_scale:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="spacing",
                    message=f"Spacing value {value}px doesn't follow 8-point grid",
                    token_path=f"{path}.scale[{i}]",
                    suggestion=f"Use standard spacing values: {', '.join(map(str, self.spacing_scale))}"
                ))

    def validate_breakpoints(self, breakpoints: Dict, path: str = "breakpoints") -> None:
        """Validate breakpoint tokens"""
        if not isinstance(breakpoints, dict):
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="layout",
                message="Breakpoints must be a dictionary",
                token_path=path,
                suggestion="Use object with sm, md, lg, xl keys"
            ))
            return

        for name, value in self.breakpoints.items():
            if name not in breakpoints:
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="layout",
                    message=f"Missing breakpoint: {name}",
                    token_path=f"{path}.{name}",
                    suggestion=f"Add {name} breakpoint at {value}px"
                ))

    def validate_border_radius(self, border_radius: Any, path: str = "borderRadius") -> None:
        """Validate border radius tokens"""
        if isinstance(border_radius, dict):
            for name, value in border_radius.items():
                if not isinstance(value, (int, float)) or value < 0:
                    self.report.add_issue(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        category="visual",
                        message=f"Invalid border radius value: {value}",
                        token_path=f"{path}.{name}",
                        suggestion="Use positive number values for border radius"
                    ))
        elif isinstance(border_radius, list):
            for i, value in enumerate(border_radius):
                if value not in self.border_radius_scale:
                    self.report.add_issue(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="visual",
                        message=f"Border radius {value}px not in standard scale",
                        token_path=f"{path}[{i}]",
                        suggestion=f"Use standard values: {', '.join(map(str, self.border_radius_scale))}"
                    ))

    def validate_z_index(self, z_index: Any, path: str = "zIndex") -> None:
        """Validate z-index tokens"""
        if not isinstance(z_index, dict):
            self.report.add_issue(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="layout",
                message="Z-index tokens must be a dictionary",
                token_path=path,
                suggestion="Use object with semantic keys (modal, dropdown, etc.)"
            ))
            return

        for name, value in z_index.items():
            if not isinstance(value, int):
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="layout",
                    message=f"Z-index value must be integer: {value}",
                    token_path=f"{path}.{name}",
                    suggestion="Use integer values for z-index"
                ))

    def validate_naming_conventions(self, tokens: Dict, path: str = "") -> None:
        """Validate naming conventions"""
        for key, value in tokens.items():
            current_path = f"{path}.{key}" if path else key

            # Check kebab-case for most tokens
            if not re.match(r'^[a-z][a-z0-9]*([A-Z][a-z0-9]*)*$', key) and not key.replace('_', '').replace('-', '').isalnum():
                self.report.add_issue(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="naming",
                    message=f"Inconsistent naming: {key}",
                    token_path=current_path,
                    suggestion="Use camelCase for object keys"
                ))

            # Recursively validate nested objects
            if isinstance(value, dict):
                self.validate_naming_conventions(value, current_path)

    def validate_accessibility(self, tokens: Dict) -> None:
        """Validate accessibility-related tokens"""
        if 'colors' not in tokens:
            return

        colors = tokens['colors']

        # Check for high contrast variants
        if 'primary' in colors and isinstance(colors['primary'], dict):
            primary_colors = colors['primary']
            if '500' in primary_colors and '700' in primary_colors:
                # Calculate contrast between primary-500 and primary-700
                contrast = self._calculate_contrast(primary_colors['500'], primary_colors['700'])
                if contrast < 3.0:
                    self.report.add_issue(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="accessibility",
                        message="Primary color contrast may be insufficient for accessibility",
                        token_path="colors.primary",
                        suggestion="Consider adjusting primary colors for better contrast (minimum 3:1 for large text)"
                    ))

    def _calculate_contrast(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def calculate_luminance(r, g, b):
            def normalize(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

            r_norm = normalize(r)
            g_norm = normalize(g)
            b_norm = normalize(b)

            return 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)

        l1 = calculate_luminance(r1, g1, b1)
        l2 = calculate_luminance(r2, g2, b2)

        lighter = max(l1, l2)
        darker = min(l1, l2)

        return (lighter + 0.05) / (darker + 0.05)

    def validate_tokens(self, tokens: Dict) -> ValidationReport:
        """Perform complete validation of design tokens"""
        self.report = ValidationReport()

        # Validate each category
        if 'colors' in tokens:
            self.validate_colors(tokens['colors'])

        if 'typography' in tokens:
            self.validate_typography(tokens['typography'])

        if 'spacing' in tokens:
            self.validate_spacing(tokens['spacing'])

        if 'breakpoints' in tokens:
            self.validate_breakpoints(tokens['breakpoints'])

        if 'borderRadius' in tokens:
            self.validate_border_radius(tokens['borderRadius'])

        if 'zIndex' in tokens:
            self.validate_z_index(tokens['zIndex'])

        # Cross-cutting validations
        self.validate_naming_conventions(tokens)
        self.validate_accessibility(tokens)

        # Update summary
        self.report.summary = self.report.get_summary()

        return self.report

    def generate_report(self, tokens_file: str, output_format: str = "console") -> str:
        """Generate validation report"""
        try:
            with open(tokens_file, 'r') as f:
                tokens = json.load(f)
        except Exception as e:
            return f"Error loading tokens file: {e}"

        report = self.validate_tokens(tokens)

        if output_format == "json":
            return json.dumps({
                "passed": report.passed,
                "summary": report.summary,
                "issues": [
                    {
                        "level": issue.level.value,
                        "category": issue.category,
                        "message": issue.message,
                        "token_path": issue.token_path,
                        "suggestion": issue.suggestion
                    }
                    for issue in report.issues
                ]
            }, indent=2)

        else:  # console format
            lines = []
            lines.append("🎨 Design Token Validation Report")
            lines.append("=" * 40)

            if report.passed:
                lines.append("✅ All tokens passed validation!")
            else:
                lines.append("❌ Validation issues found")

            lines.append(f"\n📊 Summary: {report.summary['error']} errors, {report.summary['warning']} warnings, {report.summary['info']} info")

            if report.issues:
                lines.append("\n🔍 Issues:")

                for level in [ValidationLevel.ERROR, ValidationLevel.WARNING, ValidationLevel.INFO]:
                    level_issues = [i for i in report.issues if i.level == level]
                    if level_issues:
                        icon = "❌" if level == ValidationLevel.ERROR else "⚠️" if level == ValidationLevel.WARNING else "ℹ️"
                        lines.append(f"\n{icon} {level.value.title()}s:")

                        for issue in level_issues:
                            lines.append(f"  • {issue.token_path}: {issue.message}")
                            if issue.suggestion:
                                lines.append(f"    💡 {issue.suggestion}")

            return "\n".join(lines)

    def save_report(self, tokens_file: str, output_file: str, output_format: str = "json"):
        """Save validation report to file"""
        report_content = self.generate_report(tokens_file, output_format)

        with open(output_file, 'w') as f:
            f.write(report_content)

        print(f"Validation report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Validate design tokens against standards')
    parser.add_argument('tokens_file', help='Path to design tokens JSON file')
    parser.add_argument('--output', '-o', help='Output file for report')
    parser.add_argument('--format', choices=['console', 'json'], default='console', help='Report format')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')

    args = parser.parse_args()

    validator = DesignTokenValidator()

    if args.output:
        validator.save_report(args.tokens_file, args.output, args.format)
    else:
        report = validator.generate_report(args.tokens_file, args.format)
        print(report)

    # Return appropriate exit code
    if args.format == 'json':
        return 0
    else:
        report = validator.validate_tokens(json.load(open(args.tokens_file)))
        return 0 if report.passed or (args.strict and report.summary['warning'] == 0) else 1


if __name__ == '__main__':
    exit(main())