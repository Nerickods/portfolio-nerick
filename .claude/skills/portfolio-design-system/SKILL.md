# Portfolio Design System

Professional design system builder for developer portfolios with component libraries, responsive patterns, and visual consistency.

**License:** MIT

## Overview

This skill provides a comprehensive design system specifically tailored for developer portfolios, implementing atomic design principles, accessibility standards, and modern web technologies to ensure professional visual consistency and exceptional user experience.

## Features

### 🎨 Component Library System
- Atomic design principles (atoms, molecules, organisms, templates, pages)
- Reusable React components with TypeScript
- Consistent naming conventions and prop interfaces
- Storybook integration for documentation
- Theme provider with multiple themes

### 🎯 Professional Color Schemes
- Color palettes optimized for tech portfolios
- Dark/light theme system
- Accessibility compliance (WCAG AA/AAA)
- Brand color generation based on tech personality
- Color coding for technologies and skills

### ✍️ Typography System
- Font stacks optimized for code and content
- Consistent type scales (modular scale)
- Syntax highlighting typography
- Responsive typography with clamp()
- Performance optimization for font loading

### 📐 Layout & Spacing System
- 8-point grid system for consistency
- Standardized responsive breakpoints
- Container systems with max-widths
- Spacing utilities and margin/padding patterns
- Flexbox and Grid layout patterns

### ⚡ Interactive Components
- Button variants and states system
- Form components with validation states
- Navigation patterns (header, footer, breadcrumbs)
- Card components for projects and skills
- Modal, drawer, overlay patterns

## Tech Stack Integration

- **Tailwind CSS** - Utility-first styling
- **CSS Variables** - Theme switching
- **Radix UI** - Accessible components
- **Framer Motion** - Micro-animations
- **Next.js 16** - App Router integration

## Design Tokens System

### Colors
- Primary, secondary, semantic, neutral colors
- Tech stack color coding
- Accessibility-approved contrast ratios

### Typography
- Font families, sizes, weights, line-heights
- Code-friendly monospace fonts
- Responsive type scales

### Spacing
- 8-point grid system
- Breakpoint definitions
- Container max-widths

### Visual Effects
- Shadows and borders
- Animations and transitions
- Border radius values

## Available Tools

### 🎨 Theme Generator
Generate professional color schemes optimized for developer portfolios:
```bash
theme_generator.py --personality innovative --output ./themes/
```

### 🧩 Component Scaffolder
Create new React components with consistent structure:
```bash
component_scaffolder.py --type Card --name ProjectCard --props "title,description,tags"
```

### ✅ Design Token Validator
Validate design tokens against accessibility and consistency standards:
```bash
design_token_validator.py --tokens ./tokens/ --report
```

### 🔍 Accessibility Checker
Audit components for WCAG compliance:
```bash
accessibility_checker.py --components ./src/components/ --level AA
```

## Component Library

### Header Components
- Navigation with responsive menu
- Logo container with variants
- Call-to-action buttons
- Mobile hamburger menu

### Hero Section
- Attention-grabbing headlines
- Subheadings with proper hierarchy
- Primary and secondary CTAs
- Background patterns and gradients

### Project Cards
- Image containers with lazy loading
- Title and description typography
- Technology tags with color coding
- Action links and buttons

### Skill Sections
- Tech stack displays with icons
- Skill progress indicators
- Category organization
- Visual skill bars

### Timeline Components
- Experience and education entries
- Project milestone markers
- Vertical and horizontal layouts
- Interactive hover states

### Contact Forms
- Input field variants
- Validation state indicators
- Textarea and select components
- Form submission states

### Footer Components
- Social media links
- Copyright information
- Secondary navigation
- Contact information

## Responsive Patterns

### Mobile-First Approach
- Base styles for mobile devices (320px+)
- Touch-friendly interaction areas
- Optimized typography for small screens

### Tablet Adaptations
- Medium breakpoint adjustments (768px+)
- Two-column layouts
- Enhanced navigation patterns

### Desktop Enhancements
- Large breakpoint optimizations (1024px+)
- Multi-column layouts
- Hover-based interactions

### Progressive Enhancement
- Core functionality without JavaScript
- Enhanced experiences with modern browsers
- Graceful degradation strategies

## Documentation System

### Storybook Integration
- Interactive component playground
- Prop documentation
- Usage examples
- Accessibility testing

### Design Guidelines
- Component usage rules
- Visual hierarchy principles
- Brand application guidelines
- Performance recommendations

### Code Examples
- Implementation examples
- Best practices
- Common patterns
- Integration guides

## Getting Started

### Installation
1. Copy the design system files to your project
2. Install dependencies: `npm install tailwindcss framer-motion @radix-ui/react-*`
3. Configure Tailwind CSS with provided config
4. Import components and utilities

### Basic Usage
```jsx
import { ThemeProvider, Button, Card, Header } from './portfolio-design-system';

function App() {
  return (
    <ThemeProvider theme="dark">
      <Header />
      <main>
        <Card variant="project">
          <Card.Title>My Project</Card.Title>
          <Card.Description>Project description here</Card.Description>
        </Card>
      </main>
    </ThemeProvider>
  );
}
```

## Performance Optimization

### Font Loading
- Preload critical fonts
- Font display strategies
- Subset font files

### Bundle Optimization
- Tree-shaking utilities
- Dynamic imports for components
- CSS purging for unused styles

### Image Optimization
- Responsive image techniques
- Lazy loading implementation
- Modern format support

## Accessibility Standards

- WCAG 2.1 AA compliance minimum
- Semantic HTML structure
- Keyboard navigation support
- Screen reader optimization
- Color contrast validation
- Focus management

## Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Progressive enhancement for older browsers
- Feature detection and polyfills when needed

## Contributing

1. Follow the established design tokens
2. Maintain accessibility standards
3. Update documentation
4. Test across devices and browsers
5. Ensure component consistency

## License

MIT License - see LICENSE file for details.