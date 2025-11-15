#!/usr/bin/env python3
"""
Portfolio Design System - Accessibility Checker

Comprehensive accessibility auditing tool for React components and design systems,
ensuring WCAG 2.1 compliance and inclusive design practices.
"""

import json
import re
import os
import math
import argparse
from typing import Dict, List, Tuple, Optional, Any, Set
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from bs4 import BeautifulSoup


class WCAGLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


class IssueSeverity(Enum):
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue"""
    rule_id: str
    title: str
    description: str
    severity: IssueSeverity
    wcag_level: WCAGLevel
    element: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: Optional[str] = None


@dataclass
class AccessibilityReport:
    """Complete accessibility audit report"""
    issues: List[AccessibilityIssue] = field(default_factory=list)
    score: float = 0.0
    wcag_compliance: str = ""
    summary: Dict[str, int] = field(default_factory=dict)

    def add_issue(self, issue: AccessibilityIssue):
        self.issues.append(issue)

    def calculate_score(self) -> float:
        """Calculate accessibility score (0-100)"""
        if not self.issues:
            return 100.0

        # Weight issues by severity
        weights = {
            IssueSeverity.CRITICAL: 10,
            IssueSeverity.SERIOUS: 5,
            IssueSeverity.MODERATE: 2,
            IssueSeverity.MINOR: 1
        }

        total_weight = sum(weights[issue.severity] for issue in self.issues)
        max_possible_weight = len(self.issues) * 10  # All issues as critical

        return max(0, 100 - (total_weight / max_possible_weight * 100))

    def get_summary(self) -> Dict[str, int]:
        """Get issue count by severity"""
        summary = {severity.value: 0 for severity in IssueSeverity}
        for issue in self.issues:
            summary[issue.severity.value] += 1
        return summary

    def determine_wcag_compliance(self) -> str:
        """Determine WCAG compliance level"""
        critical_count = sum(1 for issue in self.issues if issue.severity == IssueSeverity.CRITICAL)
        serious_count = sum(1 for issue in self.issues if issue.severity == IssueSeverity.SERIOUS)

        if critical_count == 0 and serious_count == 0:
            return "WCAG 2.1 AAA"
        elif critical_count == 0:
            return "WCAG 2.1 AA"
        elif critical_count <= 1:
            return "WCAG 2.1 A (Partial)"
        else:
            return "Non-compliant"


class ColorContrastChecker:
    """Handles color contrast calculations and validation"""

    def __init__(self):
        self.contrast_ratios = {
            WCAGLevel.A: {"normal": 3.0, "large": 2.0},
            WCAGLevel.AA: {"normal": 4.5, "large": 3.0},
            WCAGLevel.AAA: {"normal": 7.0, "large": 4.5}
        }

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = hex_color * 2
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def calculate_luminance(self, r: int, g: int, b: int) -> float:
        """Calculate relative luminance"""
        def normalize(c: int) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

        r_norm = normalize(r)
        g_norm = normalize(g)
        b_norm = normalize(b)

        return 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

    def calculate_contrast(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)

        l1 = self.calculate_luminance(r1, g1, b1)
        l2 = self.calculate_luminance(r2, g2, b2)

        lighter = max(l1, l2)
        darker = min(l1, l2)

        return (lighter + 0.05) / (darker + 0.05)

    def check_contrast(self, foreground: str, background: str,
                      level: WCAGLevel = WCAGLevel.AA, is_large: bool = False) -> Dict[str, Any]:
        """Check color contrast compliance"""
        contrast = self.calculate_contrast(foreground, background)
        required_ratio = self.contrast_ratios[level]["large" if is_large else "normal"]

        return {
            "contrast": round(contrast, 2),
            "required": required_ratio,
            "passes": contrast >= required_ratio,
            "level": level.value,
            "is_large": is_large
        }


class AccessibilityChecker:
    """Main accessibility checking engine"""

    def __init__(self, target_level: WCAGLevel = WCAGLevel.AA):
        self.report = AccessibilityReport()
        self.target_level = target_level
        self.contrast_checker = ColorContrastChecker()

        # WCAG success criteria mapping
        self.wcag_criteria = {
            "1.1.1": "Non-text Content",
            "1.2.1": "Audio-only and Video-only (Prerecorded)",
            "1.2.3": "Audio Description or Media Alternative (Prerecorded)",
            "1.2.5": "Audio Description (Prerecorded)",
            "1.3.1": "Info and Relationships",
            "1.3.2": "Meaningful Sequence",
            "1.3.3": "Sensory Characteristics",
            "1.4.1": "Use of Color",
            "1.4.2": "Audio Control",
            "1.4.3": "Contrast (Minimum)",
            "1.4.4": "Resize text",
            "1.4.5": "Images of Text",
            "1.4.10": "Reflow",
            "1.4.11": "Non-text Contrast",
            "1.4.12": "Text Spacing",
            "2.1.1": "Keyboard",
            "2.1.2": "No Keyboard Trap",
            "2.1.4": "Character Key Shortcuts",
            "2.2.1": "Timing Adjustable",
            "2.2.2": "Pause, Stop, Hide",
            "2.3.1": "Three Flashes or Below Threshold",
            "2.4.1": "Bypass Blocks",
            "2.4.2": "Page Titled",
            "2.4.3": "Focus Order",
            "2.4.4": "Link Purpose (In Context)",
            "2.4.5": "Multiple Ways",
            "2.4.6": "Headings and Labels",
            "2.4.7": "Focus Visible",
            "3.1.1": "Language of Page",
            "3.1.2": "Language of Parts",
            "3.2.1": "On Focus",
            "3.2.2": "On Input",
            "3.2.3": "Consistent Navigation",
            "3.2.4": "Consistent Identification",
            "3.3.1": "Error Identification",
            "3.3.2": "Labels or Instructions",
            "3.3.3": "Error Suggestion",
            "3.3.4": "Error Prevention (Legal, Financial, Data)",
            "4.1.1": "Parsing",
            "4.1.2": "Name, Role, Value",
            "4.1.3": "Status Messages"
        }

    def check_react_components(self, component_dir: str) -> AccessibilityReport:
        """Check React components for accessibility"""
        component_path = Path(component_dir)

        if not component_path.exists():
            self.report.add_issue(AccessibilityIssue(
                rule_id="directory_not_found",
                title="Component directory not found",
                description=f"The specified component directory does not exist: {component_dir}",
                severity=IssueSeverity.CRITICAL,
                wcag_level=self.target_level,
                recommendation="Verify the component directory path is correct"
            ))
            return self.report

        # Find all React component files
        component_files = list(component_path.rglob("*.tsx")) + list(component_path.rglob("*.jsx"))

        for file_path in component_files:
            self._check_component_file(file_path)

        return self.report

    def _check_component_file(self, file_path: Path):
        """Check individual React component file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Parse the component
            self._check_component_structure(content, str(file_path), lines)

        except Exception as e:
            self.report.add_issue(AccessibilityIssue(
                rule_id="file_parsing_error",
                title="File parsing error",
                description=f"Could not parse component file: {e}",
                severity=IssueSeverity.MINOR,
                wcag_level=self.target_level,
                element=str(file_path)
            ))

    def _check_component_structure(self, content: str, file_path: str, lines: List[str]):
        """Check component structure for accessibility issues"""

        # Check for semantic HTML usage
        self._check_semantic_html(content, file_path, lines)

        # Check for ARIA attributes
        self._check_aria_attributes(content, file_path, lines)

        # Check for keyboard navigation
        self._check_keyboard_navigation(content, file_path, lines)

        # Check for accessibility props
        self._check_accessibility_props(content, file_path, lines)

        # Check for image alt attributes
        self._check_image_alts(content, file_path, lines)

        # Check for form labels
        self._check_form_labels(content, file_path, lines)

        # Check for heading structure
        self._check_heading_structure(content, file_path, lines)

    def _check_semantic_html(self, content: str, file_path: str, lines: List[str]):
        """Check for proper semantic HTML usage"""
        # Check for div overuse
        div_count = len(re.findall(r'<div[^>]*>', content))
        if div_count > 10:
            self.report.add_issue(AccessibilityIssue(
                rule_id="semantic_html_div_overuse",
                title="Excessive use of div elements",
                description="Consider using semantic HTML elements for better accessibility",
                severity=IssueSeverity.MODERATE,
                wcag_level=WCAGLevel.AA,
                element=file_path,
                recommendation="Replace generic divs with semantic elements like <main>, <section>, <nav>, <article>, <header>, <footer>"
            ))

        # Check for button vs div with click handler
        if re.search(r'div[^>]*onClick=', content):
            self.report.add_issue(AccessibilityIssue(
                rule_id="button_semantics",
                title="Interactive div instead of button",
                description="Use <button> elements for interactive controls instead of divs",
                severity=IssueSeverity.SERIOUS,
                wcag_level=WCAGLevel.A,
                element=file_path,
                recommendation="Replace interactive divs with <button> elements"
            ))

    def _check_aria_attributes(self, content: str, file_path: str, lines: List[str]):
        """Check ARIA attributes usage"""
        # Check for missing aria-labels when using aria-labelledby
        if 'aria-labelledby' in content and 'aria-label' not in content:
            self.report.add_issue(AccessibilityIssue(
                rule_id="aria_label_missing",
                title="Missing aria-label",
                description="Elements with aria-labelledby should also have aria-label as fallback",
                severity=IssueSeverity.MODERATE,
                wcag_level=WCAGLevel.A,
                element=file_path,
                recommendation="Add aria-label as fallback for screen readers"
            ))

        # Check for aria-hidden on focusable elements
        aria_hidden_focusable = re.findall(r'aria-hidden=[\'"]true[\'"][^>]*tabIndex', content)
        if aria_hidden_focusable:
            self.report.add_issue(AccessibilityIssue(
                rule_id="aria_hidden_focusable",
                title="Focusable element with aria-hidden",
                description="Elements with aria-hidden='true' should not be focusable",
                severity=IssueSeverity.SERIOUS,
                wcag_level=WCAGLevel.A,
                element=file_path,
                recommendation="Remove tabIndex or aria-hidden from focusable elements"
            ))

    def _check_keyboard_navigation(self, content: str, file_path: str, lines: List[str]):
        """Check keyboard navigation support"""
        # Check for custom event handlers without keyboard support
        mouse_only_handlers = ['onMouseEnter', 'onMouseLeave', 'onHover']
        for handler in mouse_only_handlers:
            if handler in content:
                # Check for corresponding keyboard events
                keyboard_equivalents = {
                    'onMouseEnter': 'onFocus',
                    'onMouseLeave': 'onBlur',
                    'onHover': 'onFocus'
                }

                if keyboard_equivalents[handler] not in content:
                    self.report.add_issue(AccessibilityIssue(
                        rule_id="keyboard_navigation_missing",
                        title="Mouse-only interaction without keyboard support",
                        description=f"Component uses {handler} without keyboard equivalent",
                        severity=IssueSeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        element=file_path,
                        recommendation=f"Add {keyboard_equivalents[handler]} handler for keyboard accessibility"
                    ))

    def _check_accessibility_props(self, content: str, file_path: str, lines: List[str]):
        """Check for accessibility-specific React props"""
        # Check for missing data-testid (useful for testing)
        if 'export const' in content and 'data-testid' not in content:
            self.report.add_issue(AccessibilityIssue(
                rule_id="testing_identifiers",
                title="Missing testing identifiers",
                description="Components should include data-testid props for accessibility testing",
                severity=IssueSeverity.MINOR,
                wcag_level=WCAGLevel.AA,
                element=file_path,
                recommendation="Add data-testid prop to interactive components"
            ))

        # Check for role attributes on interactive elements
        interactive_elements = ['button', 'a', 'input', 'select', 'textarea']
        for element in interactive_elements:
            if f'<{element}' in content and 'role=' in content:
                self.report.add_issue(AccessibilityIssue(
                    rule_id="redundant_role",
                    title=f"Redundant role on {element} element",
                    description=f"Native {element} elements should not have explicit roles",
                    severity=IssueSeverity.MODERATE,
                    wcag_level=WCAGLevel.A,
                    element=file_path,
                    recommendation=f"Remove role attribute from native {element} element"
                ))

    def _check_image_alts(self, content: str, file_path: str, lines: List[str]):
        """Check for image alt attributes"""
        img_tags = re.finditer(r'<img[^>]*>', content)

        for match in img_tags:
            img_tag = match.group()
            if 'alt=' not in img_tag:
                line_num = content[:match.start()].count('\n') + 1
                self.report.add_issue(AccessibilityIssue(
                    rule_id="image_alt_missing",
                    title="Missing alt attribute on image",
                    description="All images must have alt attributes for accessibility",
                    severity=IssueSeverity.SERIOUS,
                    wcag_level=WCAGLevel.A,
                    element=file_path,
                    line_number=line_num,
                    recommendation="Add descriptive alt attribute to the image"
                ))

    def _check_form_labels(self, content: str, file_path: str, lines: List[str]):
        """Check form field labels"""
        input_tags = re.finditer(r'<input[^>]*>', content)

        for match in input_tags:
            input_tag = match.group()
            if 'type=' not in input_tag or 'hidden' not in input_tag:
                # Check if input has associated label
                has_id = 'id=' in input_tag
                has_aria_label = 'aria-label=' in input_tag or 'aria-labelledby=' in input_tag

                if not (has_id or has_aria_label):
                    line_num = content[:match.start()].count('\n') + 1
                    self.report.add_issue(AccessibilityIssue(
                        rule_id="form_label_missing",
                        title="Form input without proper label",
                        description="Form inputs must have associated labels",
                        severity=IssueSeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        element=file_path,
                        line_number=line_num,
                        recommendation="Add id attribute and corresponding label, or use aria-label"
                    ))

    def _check_heading_structure(self, content: str, file_path: str, lines: List[str]):
        """Check heading hierarchy"""
        headings = []
        for match in re.finditer(r'<h([1-6])[^>]*>', content):
            level = int(match.group(1))
            line_num = content[:match.start()].count('\n') + 1
            headings.append((level, line_num))

        # Check for skipped heading levels
        for i in range(1, len(headings)):
            current_level = headings[i][0]
            prev_level = headings[i-1][0]

            if current_level > prev_level + 1:
                self.report.add_issue(AccessibilityIssue(
                    rule_id="heading_hierarchy_skipped",
                    title="Skipped heading level",
                    description=f"Heading h{current_level} follows h{prev_level}, skipping levels",
                    severity=IssueSeverity.MODERATE,
                    wcag_level=WCAGLevel.AA,
                    element=file_path,
                    line_number=headings[i][1],
                    recommendation="Use proper heading hierarchy without skipping levels"
                ))

    def check_color_contrast(self, theme_file: str) -> AccessibilityReport:
        """Check color contrast in theme/design tokens"""
        try:
            with open(theme_file, 'r') as f:
                theme = json.load(f)
        except Exception as e:
            self.report.add_issue(AccessibilityIssue(
                rule_id="theme_parsing_error",
                title="Theme file parsing error",
                description=f"Could not parse theme file: {e}",
                severity=IssueSeverity.CRITICAL,
                wcag_level=self.target_level,
                element=theme_file
            ))
            return self.report

        if 'colors' not in theme:
            self.report.add_issue(AccessibilityIssue(
                rule_id="colors_missing",
                title="Missing colors in theme",
                description="Theme file must include color definitions",
                severity=IssueSeverity.SERIOUS,
                wcag_level=self.target_level,
                element=theme_file,
                recommendation="Add color definitions to theme file"
            ))
            return self.report

        colors = theme['colors']

        # Check primary color contrast
        if 'primary' in colors and 'neutral' in colors:
            self._check_color_pair_contrast(colors['primary'], colors['neutral'], theme_file)

        return self.report

    def _check_color_pair_contrast(self, primary_colors: Dict, neutral_colors: Dict, theme_file: str):
        """Check contrast between primary and neutral colors"""
        if not isinstance(primary_colors, dict) or not isinstance(neutral_colors, dict):
            return

        # Common contrast checks
        test_combinations = [
            ('500', '0'),    # Primary medium on white
            ('600', '0'),    # Primary dark on white
            ('500', '900'),  # Primary medium on dark
            ('800', '0'),    # Primary dark on white
        ]

        for primary_shade, neutral_shade in test_combinations:
            if primary_shade in primary_colors and neutral_shade in neutral_colors:
                foreground = primary_colors[primary_shade]
                background = neutral_colors[neutral_shade]

                result = self.contrast_checker.check_contrast(
                    foreground, background, self.target_level
                )

                if not result['passes']:
                    self.report.add_issue(AccessibilityIssue(
                        rule_id="insufficient_contrast",
                        title="Insufficient color contrast",
                        description=f"Contrast ratio {result['contrast']}:1 is below required {result['required']}:1",
                        severity=IssueSeverity.SERIOUS,
                        wcag_level=self.target_level,
                        element=theme_file,
                        recommendation=f"Adjust colors to achieve at least {result['required']}:1 contrast ratio"
                    ))

    def check_storybook_stories(self, stories_dir: str) -> AccessibilityReport:
        """Check Storybook stories for accessibility testing"""
        stories_path = Path(stories_dir)

        if not stories_path.exists():
            return self.report

        story_files = list(stories_path.rglob("*.stories.*"))

        for file_path in story_files:
            self._check_storybook_story(file_path)

        return self.report

    def _check_storybook_story(self, file_path: Path):
        """Check individual Storybook story file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for accessibility parameters
            if 'parameters:' in content:
                if 'a11y' not in content and 'accessibility' not in content:
                    self.report.add_issue(AccessibilityIssue(
                        rule_id="storybook_a11y_missing",
                        title="Missing accessibility testing in Storybook",
                        description="Stories should include accessibility testing parameters",
                        severity=IssueSeverity.MODERATE,
                        wcag_level=WCAGLevel.AA,
                        element=str(file_path),
                        recommendation="Add @storybook/addon-a11y for accessibility testing"
                    ))

        except Exception as e:
            self.report.add_issue(AccessibilityIssue(
                rule_id="story_parsing_error",
                title="Story file parsing error",
                description=f"Could not parse story file: {e}",
                severity=IssueSeverity.MINOR,
                wcag_level=self.target_level,
                element=str(file_path)
            ))

    def generate_report(self, output_format: str = "console") -> str:
        """Generate accessibility report"""
        self.report.score = self.report.calculate_score()
        self.report.wcag_compliance = self.report.determine_wcag_compliance()
        self.report.summary = self.report.get_summary()

        if output_format == "json":
            return json.dumps({
                "score": self.report.score,
                "wcag_compliance": self.report.wcag_compliance,
                "summary": self.report.summary,
                "issues": [
                    {
                        "rule_id": issue.rule_id,
                        "title": issue.title,
                        "description": issue.description,
                        "severity": issue.severity.value,
                        "wcag_level": issue.wcag_level.value,
                        "element": issue.element,
                        "line_number": issue.line_number,
                        "recommendation": issue.recommendation
                    }
                    for issue in self.report.issues
                ]
            }, indent=2)

        else:  # console format
            lines = []
            lines.append("♿ Accessibility Audit Report")
            lines.append("=" * 40)

            # Score and compliance
            score_emoji = "🟢" if self.report.score >= 90 else "🟡" if self.report.score >= 70 else "🔴"
            lines.append(f"{score_emoji} Accessibility Score: {self.report.score:.1f}/100")
            lines.append(f"📋 WCAG Compliance: {self.report.wcag_compliance}")

            # Summary
            summary = self.report.summary
            total_issues = sum(summary.values())
            lines.append(f"\n📊 Summary: {total_issues} issues found")

            if summary["critical"] > 0:
                lines.append(f"  ❌ {summary['critical']} Critical")
            if summary["serious"] > 0:
                lines.append(f"  ⚠️  {summary['serious']} Serious")
            if summary["moderate"] > 0:
                lines.append(f"  🔸 {summary['moderate']} Moderate")
            if summary["minor"] > 0:
                lines.append(f"  ℹ️  {summary['minor']} Minor")

            # Issues by category
            if self.report.issues:
                lines.append(f"\n🔍 Issues by Severity:")

                for severity in [IssueSeverity.CRITICAL, IssueSeverity.SERIOUS,
                               IssueSeverity.MODERATE, IssueSeverity.MINOR]:
                    severity_issues = [i for i in self.report.issues if i.severity == severity]
                    if severity_issues:
                        emoji = {"critical": "❌", "serious": "⚠️", "moderate": "🔸", "minor": "ℹ️"}
                        lines.append(f"\n{emoji[severity.value]} {severity.value.title()} Issues:")

                        for issue in severity_issues:
                            lines.append(f"  • {issue.title}")
                            if issue.element:
                                lines.append(f"    📁 {issue.element}")
                            if issue.line_number:
                                lines.append(f"    📍 Line {issue.line_number}")
                            if issue.recommendation:
                                lines.append(f"    💡 {issue.recommendation}")

            return "\n".join(lines)

    def save_report(self, output_file: str, output_format: str = "json"):
        """Save accessibility report to file"""
        report_content = self.generate_report(output_format)

        with open(output_file, 'w') as f:
            f.write(report_content)

        print(f"Accessibility report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Check accessibility of React components and design systems')
    parser.add_argument('--components', help='Path to React components directory')
    parser.add_argument('--theme', help='Path to theme/design tokens file')
    parser.add_argument('--stories', help='Path to Storybook stories directory')
    parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA', help='WCAG compliance level')
    parser.add_argument('--output', '-o', help='Output file for report')
    parser.add_argument('--format', choices=['console', 'json'], default='console', help='Report format')

    args = parser.parse_args()

    target_level = WCAGLevel[args.level]
    checker = AccessibilityChecker(target_level)

    # Run checks based on provided arguments
    if args.components:
        print(f"Checking React components in: {args.components}")
        checker.check_react_components(args.components)

    if args.theme:
        print(f"Checking color contrast in theme: {args.theme}")
        checker.check_color_contrast(args.theme)

    if args.stories:
        print(f"Checking Storybook stories in: {args.stories}")
        checker.check_storybook_stories(args.stories)

    # Generate and output report
    if args.output:
        checker.save_report(args.output, args.format)
    else:
        report = checker.generate_report(args.format)
        print(f"\n{report}")

    # Return appropriate exit code
    critical_issues = sum(1 for issue in checker.report.issues if issue.severity == IssueSeverity.CRITICAL)
    return 1 if critical_issues > 0 else 0


if __name__ == '__main__':
    exit(main())