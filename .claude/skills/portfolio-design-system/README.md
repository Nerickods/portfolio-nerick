# Portfolio Design System

A comprehensive design system specifically built for developer portfolios, providing professional components, themes, and guidelines to ensure visual consistency and exceptional user experience.

## 🚀 Quick Start

```bash
# Clone the design system
git clone <repository-url>
cd portfolio-design-system

# Generate your first theme
python3 scripts/theme_generator.py --personality innovative --output ./themes

# Create a new component
python3 scripts/component_scaffolder.py --type ProjectCard --name MyProject

# Validate design tokens
python3 scripts/design_token_validator.py --tokens ./themes/innovative-theme.json

# Check accessibility
python3 scripts/accessibility_checker.py --components ./components --level AA
```

## 📁 Structure

```
portfolio-design-system/
├── 📄 SKILL.md              # Main skill documentation
├── 📄 README.md             # This file
├── 📄 tailwind.config.js    # Tailwind CSS configuration
├── 🔧 scripts/              # Automation tools
│   ├── theme_generator.py   # Generate professional themes
│   ├── component_scaffolder.py  # Create React components
│   ├── design_token_validator.py # Validate design tokens
│   └── accessibility_checker.py # Accessibility auditing
├── 📚 references/           # Design guidelines
│   ├── design_principles.md  # Core design principles
│   ├── accessibility_guidelines.md  # WCAG compliance
│   └── responsive_patterns.md   # Mobile-first patterns
├── 🎨 assets/              # Design assets
│   ├── themes/             # Theme files
│   ├── components/         # React components
│   │   ├── react_components/     # Component source code
│   │   ├── storybook_stories/    # Storybook documentation
│   │   └── tailwind_utilities.css # Utility classes
│   └── templates/          # Portfolio layouts
│       ├── portfolio_layouts/    # HTML templates
│       └── component_variants/   # Component variations
└── 📖 .storybook/          # Storybook configuration
    ├── main.ts
    └── preview.ts
```

## 🎨 Theme System

### Generate Professional Themes

Create customized themes based on personality profiles:

```bash
# Innovative personality (forward-thinking, creative)
python3 scripts/theme_generator.py --personality innovative

# Reliable personality (trustworthy, professional)
python3 scripts/theme_generator.py --personality reliable

# Bold personality (confident, impactful)
python3 scripts/theme_generator.py --personality bold
```

### Available Personalities

- **Innovative** - Blue-purple tones, modern and creative
- **Reliable** - Stable blues, professional and consistent
- **Bold** - Strong reds, confident and energetic
- **Minimal** - Clean teals, elegant and focused
- **Creative** - Rich purples, artistic and unique

### Theme Features

- ✅ **WCAG AA/AAA Compliant** - All color combinations tested for accessibility
- ✅ **Dark/Light Variants** - Complete theme switching support
- ✅ **Tech Colors** - Pre-defined colors for 30+ technologies
- ✅ **Design Tokens** - Comprehensive color, typography, and spacing system
- ✅ **Tailwind Integration** - Direct CSS framework integration

## 🧩 Component Library

### Pre-built Components

- **Button** - Interactive buttons with variants, sizes, and states
- **ProjectCard** - Portfolio project showcase component
- **Header** - Responsive navigation with mobile menu
- **Hero** - Landing page hero sections with multiple layouts
- **SkillBar** - Visual skill level indicators
- **Timeline** - Experience and project timelines
- **ContactForm** - Accessible form components
- **Footer** - Professional footer with social links

### Create Custom Components

```bash
# Create from predefined type
python3 scripts/component_scaffolder.py --type Button

# Custom component with props
python3 scripts/component_scaffolder.py \
  --name CustomCard \
  --props "title,description,image,tags" \
  --description "Custom portfolio card component"

# Generate complete library
python3 scripts/component_scaffolder.py --generate-library
```

### Component Features

- ✅ **TypeScript Support** - Full type safety and IntelliSense
- ✅ **Accessibility First** - WCAG 2.1 AA compliant
- ✅ **Responsive Design** - Mobile-first approach
- ✅ **Dark Mode Support** - Automatic theme switching
- ✅ **Storybook Integration** - Interactive documentation
- ✅ **Unit Testing** - Pre-built test templates

## 🎯 Layout Templates

### Portfolio Layouts

1. **Modern Portfolio** (`modern_portfolio.html`)
   - Full-featured portfolio with hero, projects, skills, and contact
   - Responsive navigation with mobile menu
   - Dark mode support
   - Smooth animations and transitions

2. **Minimal Portfolio** (`minimal_portfolio.html`)
   - Clean, minimalist design
   - Typography-focused layout
   - Optimized for developer portfolios
   - Performance-optimized

### Template Features

- ✅ **Mobile-First Design** - Works seamlessly on all devices
- ✅ **SEO Optimized** - Proper semantic HTML and meta tags
- ✅ **Performance Optimized** - Lazy loading and optimized assets
- ✅ **Accessibility Compliant** - WCAG 2.1 AA standard
- ✅ **Cross-Browser Compatible** - Works on all modern browsers

## 🔧 Development Tools

### Design Token Validator

Ensure consistency and accessibility across your design system:

```bash
# Validate theme files
python3 scripts/design_token_validator.py --tokens ./themes/light_theme.json

# Generate detailed report
python3 scripts/design_token_validator.py \
  --tokens ./themes/innovative-theme.json \
  --output ./validation-report.json \
  --format json
```

**Validation Features:**
- ✅ Color contrast compliance
- ✅ Typography scale consistency
- ✅ Spacing system adherence
- ✅ Naming convention checks
- ✅ Accessibility standards

### Accessibility Checker

Comprehensive accessibility auditing for your components:

```bash
# Check React components
python3 scripts/accessibility_checker.py --components ./src/components

# Check color contrast in themes
python3 scripts/accessibility_checker.py --theme ./themes/light_theme.json

# Check Storybook documentation
python3 scripts/accessibility_checker.py --stories ./stories

# Full audit with WCAG AA compliance
python3 scripts/accessibility_checker.py \
  --components ./src/components \
  --level AA \
  --output ./accessibility-report.json
```

**Accessibility Features:**
- ✅ WCAG 2.1 compliance checking
- ✅ Screen reader testing guidelines
- ✅ Keyboard navigation validation
- ✅ Color contrast analysis
- ✅ Semantic HTML verification

## 🎨 Integration Guide

### Tailwind CSS Integration

1. **Install Dependencies**
```bash
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
```

2. **Configure Tailwind**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './assets/components/**/*.{js,ts,jsx,tsx}',
    './templates/**/*.{html}',
  ],
  theme: {
    extend: {
      // Custom theme extensions from portfolio design system
    }
  }
}
```

3. **Include Utilities**
```css
/* Include portfolio design system utilities */
@import './assets/components/tailwind_utilities.css';
```

### React Integration

```jsx
// Import components
import { Button, ProjectCard, Header, Hero } from './assets/components/react_components';

// Use in your app
function App() {
  return (
    <div>
      <Header
        logo={<span>MyPortfolio</span>}
        navigation={[
          { id: '1', label: 'About', href: '#about' },
          { id: '2', label: 'Projects', href: '#projects' }
        ]}
      />
      <Hero
        title="John Doe"
        subtitle="Full-Stack Developer"
        variant="centered"
      />
      <ProjectCard
        project={projectData}
        variant="featured"
      />
    </div>
  );
}
```

### Theme Integration

```jsx
// Theme provider component
import { useState, useEffect } from 'react';

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

## 📚 Documentation

### Design Guidelines

- **[Design Principles](references/design_principles.md)** - Core design philosophy and standards
- **[Accessibility Guidelines](references/accessibility_guidelines.md)** - WCAG compliance and inclusive design
- **[Responsive Patterns](references/responsive_patterns.md)** - Mobile-first design patterns

### Component Documentation

All components include comprehensive Storybook documentation with:
- ✅ Interactive playgrounds
- ✅ Prop documentation
- ✅ Usage examples
- ✅ Accessibility testing
- ✅ Responsive demonstrations

### Storybook Setup

```bash
# Install Storybook dependencies
npm install @storybook/nextjs @storybook/addon-essentials @storybook/addon-a11y

# Start Storybook
npm run storybook
```

## 🚀 Deployment

### Production Setup

1. **Optimize Components**
```bash
# Validate all components
python3 scripts/accessibility_checker.py --components ./src/components --level AA

# Validate design tokens
python3 scripts/design_token_validator.py --tokens ./themes/
```

2. **Build Assets**
```bash
# Build CSS
npm run build:css

# Build components
npm run build:components

# Generate production theme
python3 scripts/theme_generator.py --personality reliable --name production-theme
```

3. **Performance Optimization**
- ✅ Lazy loading for images
- ✅ Code splitting for components
- ✅ Optimized font loading
- ✅ Minimal bundle sizes

## 🤝 Contributing

1. **Follow Design Principles** - Adhere to established design guidelines
2. **Maintain Accessibility** - Ensure WCAG 2.1 AA compliance
3. **Update Documentation** - Keep docs current with changes
4. **Test Thoroughly** - Test across devices and browsers
5. **Validate Tokens** - Run design token validation before commits

### Development Workflow

```bash
# 1. Create new component
python3 scripts/component_scaffolder.py --type YourComponent

# 2. Test accessibility
python3 scripts/accessibility_checker.py --components ./YourComponent

# 3. Validate design tokens
python3 scripts/design_token_validator.py --tokens ./themes/

# 4. Run Storybook
npm run storybook

# 5. Update documentation
# Update relevant docs in references/
```

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Resources

### External Resources
- [WebAIM](https://webaim.org/) - Web accessibility resources
- [A11y Project](https://www.a11yproject.com/) - Accessibility community
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Storybook](https://storybook.js.org/) - Component documentation

### Design Inspiration
- [Dribbble](https://dribbble.com/) - Design inspiration
- [Awwwards](https://www.awwwards.com/) - Award-winning portfolios
- [Devfolio](https://devfolio.co/) - Developer portfolio examples

---

Built with ❤️ for developers who want professional, accessible, and beautiful portfolios.