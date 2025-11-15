# Portfolio Design System - Accessibility Guidelines

## Overview

This document outlines accessibility standards and best practices for the portfolio design system, ensuring WCAG 2.1 compliance and inclusive design for all users.

## WCAG 2.1 Compliance Levels

### Level A (Essential)
- **Perceivable** - Information must be presentable in ways users can perceive
- **Operable** - Interface components must be operable
- **Understandable** - Information and operation must be understandable
- **Robust** - Content must be robust enough for various assistive technologies

### Level AA (Recommended Standard)
- All Level A requirements plus:
- **Enhanced color contrast** - 4.5:1 for normal text, 3:1 for large text
- **Resize text** - 200% zoom without breaking functionality
- **Keyboard accessibility** - Full keyboard navigation without time limits
- **Focus management** - Visible focus indicators

### Level AAA (Enhanced)
- **Higher contrast** - 7:1 for normal text, 4.5:1 for large text
- **Enhanced navigation** - Multiple ways to find content
- **Context changes** - User control over context changes

## Color & Contrast

### Contrast Requirements
- **Normal text** (18px or smaller, 14px bold): Minimum 4.5:1
- **Large text** (18px+ or 14px+ bold): Minimum 3:1:1
- **Graphical objects**: Minimum 3:1:1
- **UI components**: Visual indicators must have 3:1:1 contrast

### Color Usage Guidelines
- **Don't use color alone** - Use text labels, icons, or patterns
- **Test all combinations** - Verify contrast in both light and dark modes
- **Consider color blindness** - Test with deuteranopia, protanopia filters
- **Focus states** - Ensure focus indicators have sufficient contrast

### Implementation
```css
/* Example of accessible color implementation */
.button {
  background: #3B82F6; /* Primary color */
  color: #FFFFFF;      /* High contrast white */

  &:hover {
    background: #2563EB; /* Darker for hover state */
  }

  &:focus-visible {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
  }
}
```

## Typography & Readability

### Font Guidelines
- **Legible fonts** - Use fonts designed for screen readability
- **Sufficient size** - Minimum 16px for body text
- **Line height** - 1.5 for body text, 1.25 for headings
- **Spacing** - Adequate letter and word spacing

### Text Formatting
- **Avoid justified text** - Creates uneven spacing that's hard to read
- **Use semantic markup** - h1-h6 for headings, p for paragraphs
- **Limit line length** - 50-75 characters per line for optimal readability
- **Responsive typography** - Scale appropriately across viewports

### Implementation Example
```css
.text-content {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  line-height: 1.6;
  max-width: 65ch; /* Optimal reading length */
}
```

## Keyboard Navigation

### Requirements
- **Full keyboard access** - All interactive elements reachable via keyboard
- **Logical tab order** - Follow DOM order and visual layout
- **Visible focus** - Clear, high-contrast focus indicators
- **No keyboard traps** - Users can navigate in and out of all components

### Focus Management
- **Tab order** - Logical progression through interactive elements
- **Focus indicators** - Visible, high-contrast outlines or backgrounds
- **Skip links** - Allow users to skip navigation and go to main content
- **Modal focus** - Trap focus within modals and overlays

### Implementation
```jsx
// Example of keyboard-accessible component
const AccessibleButton = ({ onClick, children, ...props }) => (
  <button
    onClick={onClick}
    onKeyDown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onClick(e);
      }
    }}
    {...props}
  >
    {children}
  </button>
);
```

## ARIA Usage

### ARIA Roles
- **Landmark roles** - banner, navigation, main, contentinfo, complementary
- **Widget roles** - button, link, textbox, listbox, combobox
- **Document structure** - heading, list, listitem, table, row, cell
- **Live regions** - status, alert, timer, marquee

### ARIA Properties
- **aria-label** - Provides accessible name when none exists
- **aria-labelledby** - References other elements for naming
- **aria-describedby** - Provides additional description
- **aria-expanded** - Indicates expand/collapse state
- **aria-current** - Indicates current item within a set

### Best Practices
- **Don't overuse ARIA** - Use semantic HTML first
- **Use appropriate roles** - Match role to element functionality
- **Maintain state** - Keep ARIA states in sync with visual states
- **Test with screen readers** - Verify ARIA announcements

### Implementation Example
```jsx
const AccessibleNavigation = () => (
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/" aria-current="page">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
);
```

## Screen Reader Support

### Content Structure
- **Semantic HTML** - Use proper heading hierarchy (h1-h6)
- **Alternative text** - Descriptive alt text for images
- **Link context** - Descriptive link text, not just "click here"
- **Form labels** - Associated labels for all form controls

### Reading Order
- **Logical sequence** - Content reads in meaningful order
- **Hidden content** - Use appropriate techniques for content hidden from screen readers
- **Dynamic content** - Announce changes using ARIA live regions
- **Error messages** - Associate errors with form inputs

### Implementation
```jsx
const AccessibleForm = () => (
  <form>
    <div>
      <label htmlFor="email">Email address</label>
      <input
        id="email"
        type="email"
        aria-describedby="email-help email-error"
        aria-invalid={hasError}
      />
      <div id="email-help" className="sr-only">
        We'll never share your email with anyone else
      </div>
      {hasError && (
        <div id="email-error" role="alert" className="error-message">
          Please enter a valid email address
        </div>
      )}
    </div>
  </form>
);
```

## Forms & Inputs

### Label Requirements
- **Associated labels** - Every input has a corresponding label
- **Visible labels** - Labels are visible and clearly associated
- **Required fields** - Clearly mark required inputs
- **Error messaging** - Clear, accessible error messages

### Input Types
- **Appropriate types** - Use semantic input types (email, tel, url)
- **Autocomplete** - Enable browser autocomplete where appropriate
- **Validation** - Client-side and server-side validation
- **Help text** - Provide instructions when needed

### Implementation
```jsx
const AccessibleInput = ({ label, error, required, ...props }) => (
  <div>
    <label htmlFor={props.id}>
      {label}
      {required && <span aria-label="required">*</span>}
    </label>
    <input
      {...props}
      aria-invalid={!!error}
      aria-describedby={error ? `${props.id}-error` : undefined}
    />
    {error && (
      <div id={`${props.id}-error`} role="alert" className="error">
        {error}
      </div>
    )}
  </div>
);
```

## Images & Media

### Alt Text Guidelines
- **Descriptive** - Describe content and function of images
- **Decorative images** - Use empty alt attribute (alt="")
- **Complex images** - Use longdesc or provide detailed descriptions
- **Text images** - Include text content in alt text

### Image Requirements
- **High contrast** - Ensure images have sufficient contrast
- **Text alternatives** - Provide text for charts, graphs, infographics
- **Captions** - Provide captions for video content
- **Transcripts** - Provide transcripts for audio content

### Implementation
```jsx
const AccessibleImage = ({ src, alt, decorative = false, ...props }) => (
  <img
    src={src}
    alt={decorative ? "" : alt}
    role={decorative ? "presentation" : undefined}
    {...props}
  />
);
```

## Tables & Data

### Table Accessibility
- **Captions** - Provide table captions or summaries
- **Headers** - Use th elements with scope attributes
- **Associations** - Associate headers with data cells
- **Linear reading** - Ensure tables make sense when read linearly

### Implementation
```jsx
const AccessibleTable = ({ caption, headers, data }) => (
  <table>
    <caption>{caption}</caption>
    <thead>
      <tr>
        {headers.map((header, index) => (
          <th key={index} scope="col">
            {header}
          </th>
        ))}
      </tr>
    </thead>
    <tbody>
      {data.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {row.map((cell, cellIndex) => (
            <td key={cellIndex} headers={`${headers[cellIndex]}`}>
              {cell}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
);
```

## Motion & Animation

### Motion Preferences
- **Respect preferences** - Honor `prefers-reduced-motion` setting
- **Essential motion only** - Keep motion to essential animations
- **Controls** - Provide controls for auto-playing content
- **Alternatives** - Provide static alternatives for animated content

### Implementation
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Testing Guidelines

### Automated Testing
- **axe-core** - Integrate accessibility testing in CI/CD
- **lighthouse** - Regular accessibility audits
- **color contrast analyzers** - Automated contrast checking
- **HTML validation** - Ensure valid, semantic HTML

### Manual Testing
- **Keyboard navigation** - Test all functionality via keyboard
- **Screen readers** - Test with NVDA, JAWS, VoiceOver
- **Zoom testing** - Test at 200% and 400% zoom
- **Color blindness** - Test with color blindness simulators

### Testing Checklist
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible and clear
- [ ] Color contrast meets WCAG AA standards
- [ ] All images have appropriate alt text
- [ ] Form inputs have associated labels
- [ ] Content reads in logical order with screen reader
- [ ] Links have descriptive text
- [ ] Tables have proper headers and captions
- [ ] Modal dialogs trap focus appropriately
- [ ] Error messages are accessible and informative

## Documentation Requirements

### Component Documentation
- **Accessibility features** - Document all accessibility features
- **Keyboard shortcuts** - List all keyboard interactions
- **ARIA usage** - Document ARIA attributes and their purpose
- **Testing notes** - Include accessibility testing notes

### Design Documentation
- **Accessibility standards** - Reference WCAG guidelines
- **Color contrast ratios** - Document contrast values
- **Typography requirements** - Specify accessible font choices
- **Interaction patterns** - Document accessible interaction patterns

## Ongoing Maintenance

### Regular Audits
- **Monthly accessibility audits** - Check for new issues
- **User testing** - Include users with disabilities
- **Tool updates** - Keep accessibility tools updated
- **Training** - Regular team accessibility training

### Monitoring
- **Error tracking** - Monitor accessibility-related errors
- **User feedback** - Collect and act on accessibility feedback
- **Performance impact** - Monitor impact of accessibility features
- **Compliance tracking** - Track WCAG compliance status

## Resources & Tools

### Testing Tools
- **axe DevTools** - Browser extension for accessibility testing
- **WAVE** - Web accessibility evaluation tool
- **Colour Contrast Analyser** - TPGi's contrast checking tool
- **Accessibility Insights** - Microsoft's accessibility testing suite

### Learning Resources
- **WebAIM** - Web Accessibility in Mind
- **A11y Project** - Accessibility community resource
- **MDN Web Accessibility** - Developer documentation
- **WCAG 2.1 Guidelines** - Official W3C documentation

This guide should be regularly updated to reflect evolving accessibility standards and best practices. All team members should be familiar with these guidelines and apply them consistently across the design system.