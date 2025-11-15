#!/usr/bin/env python3
"""
Portfolio Design System - Component Scaffolder

Generates consistent React components with TypeScript, proper accessibility,
and Storybook integration for the portfolio design system.
"""

import json
import re
import argparse
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComponentTemplate:
    """Template data for component generation"""
    name: str
    type: str
    props: List[str]
    description: str
    variants: List[str] = None
    dependencies: List[str] = None


class ComponentScaffolder:
    """Generates React components with consistent structure"""

    # Component type templates
    COMPONENT_TYPES = {
        'Button': {
            'description': 'Interactive button component with multiple variants and sizes',
            'default_props': ['children', 'variant?', 'size?', 'disabled?', 'onClick?'],
            'variants': ['primary', 'secondary', 'outline', 'ghost'],
            'sizes': ['sm', 'md', 'lg'],
            'dependencies': []
        },
        'Card': {
            'description': 'Container component for content grouping',
            'default_props': ['children', 'variant?', 'elevation?', 'padding?'],
            'variants': ['default', 'elevated', 'outlined', 'project'],
            'dependencies': []
        },
        'Input': {
            'description': 'Form input component with validation states',
            'default_props': ['value', 'onChange', 'placeholder?', 'label?', 'error?', 'disabled?', 'type?'],
            'variants': ['default', 'filled', 'outlined'],
            'dependencies': []
        },
        'Modal': {
            'description': 'Overlay modal component with portal rendering',
            'default_props': ['isOpen', 'onClose', 'children', 'size?', 'title?'],
            'variants': ['default', 'fullscreen'],
            'dependencies': ['react-dom']
        },
        'Navigation': {
            'description': 'Navigation component with responsive menu',
            'default_props': ['items', 'logo?', 'mobileMenuOpen?', 'onMobileMenuToggle?'],
            'variants': ['horizontal', 'vertical'],
            'dependencies': []
        },
        'Hero': {
            'description': 'Hero section component for landing pages',
            'default_props': ['title', 'subtitle?', 'cta?', 'background?'],
            'variants': ['centered', 'left-aligned', 'split'],
            'dependencies': []
        },
        'ProjectCard': {
            'description': 'Card component specifically for project showcases',
            'default_props': ['project', 'variant?', 'showTags?', 'showLinks?'],
            'variants': ['default', 'compact', 'featured'],
            'dependencies': []
        },
        'SkillBar': {
            'description': 'Progress bar component for skill visualization',
            'default_props': ['skill', 'level', 'variant?', 'showLabel?', 'animated?'],
            'variants': ['default', 'compact', 'circular'],
            'dependencies': []
        },
        'Timeline': {
            'description': 'Timeline component for experience/education',
            'default_props': ['items', 'variant?', 'orientation?'],
            'variants': ['default', 'alternate', 'compact'],
            'dependencies': []
        },
        'Footer': {
            'description': 'Footer component with social links and navigation',
            'default_props': ['links?', 'socialLinks?', 'copyright?', 'variant?'],
            'variants': ['default', 'minimal', 'expanded'],
            'dependencies': []
        }
    }

    # TypeScript prop types mapping
    PROP_TYPES = {
        'children': 'React.ReactNode',
        'onClick': '(event: React.MouseEvent) => void',
        'onChange': '(value: string) => void',
        'isOpen': 'boolean',
        'onClose': '() => void',
        'disabled': 'boolean',
        'error': 'string | undefined',
        'value': 'string',
        'placeholder': 'string',
        'label': 'string',
        'title': 'string',
        'subtitle': 'string',
        'type': 'string',
        'size': '"sm" | "md" | "lg"',
        'variant': 'string',
        'elevation': 'number',
        'padding': 'number',
        'items': 'any[]',
        'logo': 'React.ReactNode',
        'mobileMenuOpen': 'boolean',
        'onMobileMenuToggle': '(open: boolean) => void',
        'cta': 'React.ReactNode',
        'background': 'string',
        'project': 'Project',
        'showTags': 'boolean',
        'showLinks': 'boolean',
        'skill': 'string',
        'level': 'number',
        'showLabel': 'boolean',
        'animated': 'boolean',
        'orientation': '"vertical" | "horizontal"',
        'links': 'FooterLink[]',
        'socialLinks': 'SocialLink[]',
        'copyright': 'string'
    }

    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'assets' / 'components' / 'react_components'
        self.stories_dir = Path(__file__).parent.parent / 'assets' / 'components' / 'storybook_stories'

    def parse_props(self, props_str: str) -> List[Tuple[str, Optional[str]]]:
        """Parse props string into (name, type) tuples"""
        if not props_str:
            return []

        props = props_str.split(',')
        parsed_props = []

        for prop in props:
            prop = prop.strip()
            if not prop:
                continue

            # Handle optional props (ending with ?)
            is_optional = prop.endswith('?')
            prop_name = prop.rstrip('?')

            # Get type from mapping or default to string
            prop_type = self.PROP_TYPES.get(prop_name, 'string')

            parsed_props.append((prop_name, prop_type, is_optional))

        return parsed_props

    def generate_interface(self, component_name: str, props: List[Tuple[str, str, bool]]) -> str:
        """Generate TypeScript interface for component props"""
        interface_lines = [f"export interface {component_name}Props {{"]

        for prop_name, prop_type, is_optional in props:
            optional_suffix = '?' if is_optional else ''
            interface_lines.append(f"  {prop_name}{optional_suffix}: {prop_type};")

        # Add common props
        interface_lines.extend([
            "  className?: string;",
            "  'data-testid'?: string;",
            "  children?: React.ReactNode;"
        ])

        interface_lines.append("}")
        return "\n".join(interface_lines)

    def generate_component(self, template: ComponentTemplate) -> str:
        """Generate React component code"""
        component_name = template.name
        props = self.parse_props(','.join(template.props)) if template.props else []

        # Generate interface
        interface = self.generate_interface(component_name, props)

        # Generate component code
        component_lines = [
            "import React from 'react';",
            "",
            interface,
            "",
            f"/**",
            f" * {template.description}",
            f" * @component",
            f" */",
            f"export const {component_name}: React.FC<{component_name}Props> = ({",
            "  children,",
            "  className,",
            "  'data-testid': testId,",
        ]

        # Add props destructuring
        for prop_name, _, _ in props:
            component_lines.append(f"  {prop_name},")

        component_lines.extend([
            "  ...rest",
            "}) => {",
            "  return (",
            f"    <div",
            f"      className={{{component_name}ClassNames({{ variant, size, className, error, disabled }})}}",
            f"      data-testid={{testId || '{component_name.lower()}'}}",
            f"      {...rest}",
            f"    >",
            f"      {{children}}",
            f"    </div>",
            f"  );",
            f"};",
            "",
            f"// Helper function for CSS classes",
            f"const {component_name}ClassNames = ({{",
            "  variant = 'default',",
            "  size = 'md',",
            "  className = '',",
            "  error = false,",
            "  disabled = false",
            f"}}: Partial<{component_name}Props> & {{ className?: string }}) => {{",
            f"  const baseClasses = ['{component_name.lower()}-component'];",
            "  ",
            f"  if (variant) baseClasses.push(`{component_name.lower()}-{{variant}}`);",
            f"  if (size) baseClasses.push(`{component_name.lower()}-{{size}}`);",
            f"  if (error) baseClasses.push('{component_name.lower()}-error');",
            f"  if (disabled) baseClasses.push('{component_name.lower()}-disabled');",
            "  ",
            "  return [...baseClasses, className].filter(Boolean).join(' ');",
            "};"
        ])

        return "\n".join(component_lines)

    def generate_story(self, template: ComponentTemplate) -> str:
        """Generate Storybook story for component"""
        component_name = template.name
        props = self.parse_props(','.join(template.props)) if template.props else []

        story_lines = [
            "import type { Meta, StoryObj } from '@storybook/react';",
            f"import {{ {component_name} }} from './{component_name}';",
            "",
            f"const meta: Meta<typeof {component_name}> = {{",
            f"  title: 'Components/{component_name}',",
            f"  component: {component_name},",
            f"  parameters: {{",
            "    layout: 'centered',",
            "    tags: ['autodocs'],",
            "  },",
            f"  argTypes: {{",
        ]

        # Add argTypes for props
        for prop_name, prop_type, is_optional in props:
            if prop_name == 'children':
                continue  # Skip children in controls

            control_type = 'text'
            if 'boolean' in prop_type:
                control_type = 'boolean'
            elif prop_type in ['onClick', 'onChange', 'onClose', 'onMobileMenuToggle']:
                control_type = 'action'
            elif variant_match := re.search(r'"([^"]+)"', prop_type):
                # Extract enum values
                enum_values = variant_match.group(1).replace('"', '').split(' | ')
                story_lines.append(f"    {prop_name}: {{ control: {{ type: 'select' }}, options: {enum_values} }},")
                continue

            story_lines.append(f"    {prop_name}: {{ control: '{control_type}' }},")

        story_lines.extend([
            "  },",
            "};",
            "",
            f"export default meta;",
            f"type Story = StoryObj<typeof meta>;",
            ""
        ])

        # Generate default story
        story_lines.extend([
            f"export const Default: Story = {{",
            f"  args: {{",
        ])

        # Add default args
        for prop_name, prop_type, is_optional in props:
            if prop_name == 'children':
                story_lines.append(f"    children: '{component_name} Content',")
            elif prop_type == 'boolean':
                story_lines.append(f"    {prop_name}: false,")
            elif is_optional and 'onClick' not in prop_type and 'onChange' not in prop_type:
                if 'string' in prop_type.lower():
                    story_lines.append(f"    {prop_name}: '',")

        story_lines.extend([
            "  },",
            "};",
            ""
        ])

        # Generate variant stories if available
        if template.variants:
            story_lines.append("// Variant stories")
            for variant in template.variants:
                variant_name = variant.replace(' ', '').replace('-', '').title()
                story_lines.extend([
                    f"export const {variant_name}: Story = {{",
                    f"  args: {{",
                    f"    ...Default.args,",
                    f"    variant: '{variant}',",
                    "  },",
                    "};",
                    ""
                ])

        return "\n".join(story_lines)

    def generate_test(self, template: ComponentTemplate) -> str:
        """Generate basic test file for component"""
        component_name = template.name

        test_lines = [
            "import { render, screen } from '@testing-library/react';",
            "import { axe, toHaveNoViolations } from 'jest-axe';",
            f"import {{ {component_name} }} from './{component_name}';",
            "",
            "// Extend Jest matchers",
            "expect.extend(toHaveNoViolations);",
            "",
            f"describe('{component_name}', () => {{",
            f"  it('renders without crashing', () => {{",
            f"    render(<{component_name}>Test Content</{component_name}>);",
            f"    expect(screen.getByText('Test Content')).toBeInTheDocument();",
            "  });",
            "",
            f"  it('has no accessibility violations', async () => {{",
            f"    const {{ container }} = render(<{component_name}>Test Content</{component_name}>);",
            f"    const results = await axe(container);",
            f"    expect(results).toHaveNoViolations();",
            "  });",
            "",
            f"  it('applies custom className', () => {{",
            f"    render(<{component_name} className='custom-class'>Test</{component_name}>);",
            f"    const element = screen.getByText('Test');",
            f"    expect(element).toHaveClass('custom-class');",
            "  });",
            ""
        ]

        # Add test for required props
        if template.props:
            for prop in template.props:
                prop_name = prop.rstrip('?').strip()
                if prop_name in ['onClick', 'onChange', 'onClose']:
                    test_lines.extend([
                        f"  it('calls {prop_name} when triggered', async () => {{",
                        f"    const mock{prop_name.title()} = jest.fn();",
                        f"    render(<{component_name} {prop_name}={{mock{prop_name.title()}}}>Test</{component_name}>);",
                        f"    // Add interaction test based on component type",
                        "  });",
                        ""
                    ])

        test_lines.append("});")

        return "\n".join(test_lines)

    def generate_index(self, component_name: str) -> str:
        """Generate index file for component exports"""
        return f"export {{ {component_name} }} from './{component_name}';"

    def save_component(self, template: ComponentTemplate, output_dir: str):
        """Save component files to specified directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        component_name = template.name
        component_dir = output_path / component_name
        component_dir.mkdir(exist_ok=True)

        # Generate and save component file
        component_code = self.generate_component(template)
        component_file = component_dir / f"{component_name}.tsx"
        with open(component_file, 'w') as f:
            f.write(component_code)

        # Generate and save story file
        story_code = self.generate_story(template)
        story_file = component_dir / f"{component_name}.stories.tsx"
        with open(story_file, 'w') as f:
            f.write(story_code)

        # Generate and save test file
        test_code = self.generate_test(template)
        test_file = component_dir / f"{component_name}.test.tsx"
        with open(test_file, 'w') as f:
            f.write(test_code)

        # Generate and save index file
        index_code = self.generate_index(component_name)
        index_file = component_dir / "index.ts"
        with open(index_file, 'w') as f:
            f.write(index_code)

        print(f"Component '{component_name}' created successfully:")
        print(f"  📁 {component_dir}")
        print(f"    📄 {component_name}.tsx")
        print(f"    📄 {component_name}.stories.tsx")
        print(f"    📄 {component_name}.test.tsx")
        print(f"    📄 index.ts")

    def list_component_types(self):
        """List available component types"""
        print("Available component types:")
        for name, config in self.COMPONENT_TYPES.items():
            print(f"  {name}: {config['description']}")

    def create_component_from_type(self, component_type: str, name: str = None, props: str = None):
        """Create component from predefined type"""
        if component_type not in self.COMPONENT_TYPES:
            raise ValueError(f"Unknown component type: {component_type}")

        type_config = self.COMPONENT_TYPES[component_type]
        component_name = name or component_type

        # Use custom props if provided, otherwise use defaults
        component_props = props.split(',') if props else type_config['default_props']

        template = ComponentTemplate(
            name=component_name,
            type=component_type,
            props=component_props,
            description=type_config['description'],
            variants=type_config.get('variants', []),
            dependencies=type_config.get('dependencies', [])
        )

        return template

    def generate_component_library(self, output_dir: str):
        """Generate complete component library"""
        print("Generating complete component library...")

        for component_type in self.COMPONENT_TYPES.keys():
            template = self.create_component_from_type(component_type)
            self.save_component(template, output_dir)

        # Generate main index file
        main_index_path = Path(output_dir) / "index.ts"
        with open(main_index_path, 'w') as f:
            exports = []
            for component_type in self.COMPONENT_TYPES.keys():
                exports.append(f"export {{ {component_type} }} from './{component_type}';")
            f.write("\n".join(exports))

        print(f"\nComponent library generated in {output_dir}")
        print(f"📄 Main index file: {main_index_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate React components for portfolio design system')
    parser.add_argument('--type', help='Component type (use --list-types to see options)')
    parser.add_argument('--name', help='Custom component name')
    parser.add_argument('--props', help='Comma-separated list of props (e.g., "title,description,onClick?")')
    parser.add_argument('--description', help='Component description')
    parser.add_argument('--variants', help='Comma-separated list of variants')
    parser.add_argument('--output', default='./components', help='Output directory')
    parser.add_argument('--list-types', action='store_true', help='List available component types')
    parser.add_argument('--generate-library', action='store_true', help='Generate complete component library')

    args = parser.parse_args()

    scaffolder = ComponentScaffolder()

    if args.list_types:
        scaffolder.list_component_types()
        return 0

    if args.generate_library:
        scaffolder.generate_component_library(args.output)
        return 0

    if not args.type:
        print("Error: --type is required (use --list-types to see options)")
        return 1

    try:
        if args.type in scaffolder.COMPONENT_TYPES:
            template = scaffolder.create_component_from_type(args.type, args.name, args.props)
        else:
            # Custom component
            if not args.name:
                print("Error: --name is required for custom components")
                return 1

            template = ComponentTemplate(
                name=args.name,
                type='custom',
                props=args.props.split(',') if args.props else [],
                description=args.description or f"Custom {args.name} component",
                variants=args.variants.split(',') if args.variants else []
            )

        scaffolder.save_component(template, args.output)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())