# Portfolio Design System - Responsive Design Patterns

## Overview

This document outlines responsive design patterns and best practices for creating adaptable layouts that work seamlessly across all devices and screen sizes.

## Mobile-First Approach

### Philosophy
- **Start with mobile** - Design for smallest screens first, then enhance
- **Progressive enhancement** - Add features and complexity for larger screens
- **Performance priority** - Optimize for mobile constraints (bandwidth, performance)
- **Touch-first design** - Design for touch interfaces, enhance for mouse input

### Implementation Strategy
1. **Base styles** - Mobile-first CSS without media queries
2. **Tablet enhancements** - Add complexity for 768px+ screens
3. **Desktop enhancements** - Full functionality for 1024px+ screens
4. **Large screen optimizations** - Enhanced layouts for 1280px+ screens

## Breakpoint System

### Standard Breakpoints
```css
/* Mobile */
@media (min-width: 320px) { /* Base styles */ }

/* Small mobile */
@media (min-width: 375px) { /* Enhanced mobile */ }

/* Large mobile */
@media (min-width: 414px) { /* Large mobile */ }

/* Tablet */
@media (min-width: 768px) { /* Tablet layouts */ }

/* Desktop */
@media (min-width: 1024px) { /* Desktop layouts */ }

/* Large desktop */
@media (min-width: 1280px) { /* Enhanced desktop */ }

/* Extra large */
@media (min-width: 1536px) { /* Maximum layouts */ }
```

### Custom Breakpoints
- **Container queries** - Component-based responsive design
- **Feature queries** - Responsive based on capabilities, not screen size
- **Orientation queries** - Different layouts for portrait vs landscape
- **Resolution queries** - High-density display optimizations

## Layout Patterns

### Single Column Layout
**Use Cases:** Articles, blog posts, mobile views
```css
.single-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  padding: var(--spacing-4);
  max-width: 65ch; /* Optimal reading width */
  margin: 0 auto;
}

@media (min-width: 768px) {
  .single-column {
    padding: var(--spacing-8);
    gap: var(--spacing-6);
  }
}
```

### Two-Column Layout
**Use Cases:** Content with sidebar, project listings
```css
.two-column {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-6);
}

@media (min-width: 768px) {
  .two-column {
    grid-template-columns: 2fr 1fr;
    gap: var(--spacing-8);
  }
}
```

### Three-Column Layout
**Use Cases:** Complex dashboards, documentation sites
```css
.three-column {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-4);
}

@media (min-width: 768px) {
  .three-column {
    grid-template-columns: 1fr 2fr;
  }
}

@media (min-width: 1024px) {
  .three-column {
    grid-template-columns: 1fr 2fr 1fr;
  }
}
```

### Card Grid Layout
**Use Cases:** Project galleries, product listings
```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-4);
}

@media (min-width: 640px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## Component Patterns

### Responsive Navigation
```css
.nav {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-4);
}

.nav-toggle {
  display: block;
}

.nav-menu {
  display: none;
}

.nav-menu.active {
  display: block;
}

@media (min-width: 768px) {
  .nav {
    flex-direction: row;
    padding: var(--spacing-2);
  }

  .nav-toggle {
    display: none;
  }

  .nav-menu {
    display: flex;
    flex-direction: row;
    gap: var(--spacing-4);
  }
}
```

### Responsive Hero Section
```css
.hero {
  min-height: 60vh;
  padding: var(--spacing-8) var(--spacing-4);
  text-align: center;
}

.hero-title {
  font-size: clamp(2rem, 8vw, 4rem);
  line-height: 1.1;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
  align-items: center;
}

@media (min-width: 768px) {
  .hero {
    min-height: 80vh;
    padding: var(--spacing-12) var(--spacing-6);
  }

  .hero-actions {
    flex-direction: row;
    justify-content: center;
  }
}
```

### Responsive Form
```css
.form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  max-width: 100%;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

@media (min-width: 768px) {
  .form-row {
    flex-direction: row;
  }

  .form-row > * {
    flex: 1;
  }
}
```

## Typography Patterns

### Fluid Typography
```css
/* Using clamp() for fluid scaling */
.heading-1 {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.1;
}

.heading-2 {
  font-size: clamp(1.5rem, 4vw, 3rem);
  line-height: 1.2;
}

.body-text {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  line-height: 1.6;
}

/* Using CSS custom properties for responsive typography */
:root {
  --font-size-fluid: clamp(1rem, 2.5vw, 1.25rem);
  --line-height-fluid: 1.5;
}

@media (min-width: 768px) {
  :root {
    --font-size-fluid: clamp(1.125rem, 2vw, 1.5rem);
    --line-height-fluid: 1.6;
  }
}
```

### Responsive Line Height
```css
.text-responsive {
  font-size: 1rem;
  line-height: 1.5;
}

@media (min-width: 768px) {
  .text-responsive {
    font-size: 1.125rem;
    line-height: 1.6;
  }
}

@media (min-width: 1024px) {
  .text-responsive {
    font-size: 1.25rem;
    line-height: 1.7;
  }
}
```

## Image & Media Patterns

### Responsive Images
```css
.responsive-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

/* Aspect ratio containers */
.image-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Art direction with picture element */
<picture>
  <source media="(min-width: 1024px)" srcset="large-image.jpg">
  <source media="(min-width: 768px)" srcset="medium-image.jpg">
  <img src="small-image.jpg" alt="Description">
</picture>
```

### Responsive Video
```css
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-container iframe,
.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

## Spacing Patterns

### Responsive Spacing
```css
/* Container spacing */
.container {
  padding: var(--spacing-4);
}

@media (min-width: 768px) {
  .container {
    padding: var(--spacing-6);
  }
}

@media (min-width: 1024px) {
  .container {
    padding: var(--spacing-8);
  }
}

/* Gap spacing */
.grid {
  gap: var(--spacing-3);
}

@media (min-width: 768px) {
  .grid {
    gap: var(--spacing-4);
  }
}

@media (min-width: 1024px) {
  .grid {
    gap: var(--spacing-6);
  }
}
```

### Component Spacing
```css
.card {
  padding: var(--spacing-4);
}

@media (min-width: 768px) {
  .card {
    padding: var(--spacing-6);
  }
}

.section {
  padding: var(--spacing-8) var(--spacing-4);
}

@media (min-width: 768px) {
  .section {
    padding: var(--spacing-12) var(--spacing-6);
  }
}
```

## Navigation Patterns

### Mobile Navigation
```css
/* Hamburger menu pattern */
.mobile-nav {
  position: fixed;
  top: 0;
  right: -100%;
  width: 80%;
  max-width: 320px;
  height: 100vh;
  background: white;
  transition: right 0.3s ease;
  z-index: 1000;
}

.mobile-nav.active {
  right: 0;
}

.mobile-nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 999;
}

.mobile-nav-overlay.active {
  opacity: 1;
  pointer-events: auto;
}
```

### Responsive Tabs
```css
.tabs {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

@media (min-width: 768px) {
  .tabs {
    flex-direction: row;
    border-bottom: 1px solid var(--color-border);
  }
}

.tab {
  padding: var(--spacing-3) var(--spacing-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

@media (min-width: 768px) {
  .tab {
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
  }

  .tab.active {
    border-bottom-color: var(--color-primary);
  }
}
```

## Performance Patterns

### Lazy Loading
```css
/* Intersection Observer for lazy loading */
.lazy-load {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.lazy-load.loaded {
  opacity: 1;
}
```

```javascript
// Lazy loading implementation
const lazyImages = document.querySelectorAll('.lazy-load');

const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.add('loaded');
      imageObserver.unobserve(img);
    }
  });
});

lazyImages.forEach(img => imageObserver.observe(img));
```

### Critical CSS
```css
/* Critical CSS for above-the-fold content */
.critical-path {
  /* Above-the-fold styles */
}

/* Non-critical CSS loaded asynchronously */
.non-critical {
  /* Below-the-fold styles */
}
```

## Touch Patterns

### Touch Targets
```css
/* Minimum touch target size: 44px x 44px */
.touch-target {
  min-height: 44px;
  min-width: 44px;
  padding: var(--spacing-2);
}

/* Spacing between touch targets */
.touch-target + .touch-target {
  margin-top: var(--spacing-2);
}
```

### Gesture Support
```css
.swipe-container {
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.swipe-item {
  scroll-snap-align: start;
  flex-shrink: 0;
}
```

## Testing Strategies

### Responsive Testing Checklist
- [ ] Test all breakpoints
- [ ] Verify touch targets on mobile
- [ ] Test horizontal scrolling
- [ ] Verify font scaling
- [ ] Test with high DPI displays
- [ ] Test in different browsers
- [ ] Verify performance on slow connections
- [ ] Test accessibility at different sizes

### Tools & Techniques
- **Browser DevTools** - Device simulation and responsive testing
- **BrowserStack** - Cross-device testing
- **Viewport resizers** - Quick responsive testing
- **Network throttling** - Performance testing
- **Real device testing** - Actual device verification

## Advanced Patterns

### Container Queries
```css
/* Container query support (when available) */
@container (min-width: 400px) {
  .component {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

### Feature Queries
```css
/* Feature detection for modern CSS */
@supports (display: grid) {
  .layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}

@supports not (display: grid) {
  .layout {
    display: flex;
    flex-wrap: wrap;
  }
}
```

### Variable Fonts
```css
/* Responsive typography with variable fonts */
@supports (font-variation-settings: normal) {
  .heading {
    font-family: 'Inter Variable';
    font-variation-settings: 'wght' 400, 'opsz' 32;
    font-size: clamp(1.5rem, 4vw, 3rem);
  }

  @media (min-width: 768px) {
    .heading {
      font-variation-settings: 'wght' 600, 'opsz' 48;
    }
  }
}
```

## Best Practices

### Performance
- **Mobile-first CSS** - Minimize media queries
- **Optimize images** - Responsive images with srcset
- **Minimize HTTP requests** - Combine resources when possible
- **Use CSS Grid/Flexbox** - More efficient than older layout methods

### User Experience
- **Consistent patterns** - Similar behavior across devices
- **Predictable navigation** - Easy to find and use
- **Fast loading** - Optimize for mobile performance
- **Accessible** - Maintain accessibility at all screen sizes

### Development
- **Component-based** - Design reusable responsive components
- **Documentation** - Document responsive behavior
- **Testing** - Test across devices and browsers
- **Maintenance** - Regular updates and optimizations

These patterns should be used as guidelines and adapted to specific project requirements. Always test responsive designs across actual devices and consider the target audience's device usage patterns.