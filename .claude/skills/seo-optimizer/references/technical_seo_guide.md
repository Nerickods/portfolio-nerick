# Technical SEO Guide for Developer Portfolios

## Table of Contents
1. [HTML & Semantic Structure](#html--semantic-structure)
2. [Meta Tags Implementation](#meta-tags-implementation)
3. [URL Structure Optimization](#url-structure-optimization)
4. [Image SEO Best Practices](#image-seo-best-practices)
5. [JavaScript SEO for React/Next.js](#javascript-seo-for-reactnextjs)
6. [Performance Optimization](#performance-optimization)
7. [Mobile SEO Implementation](#mobile-seo-implementation)
8. [Schema Markup Technical Guide](#schema-markup-technical-guide)
9. [Crawling & Indexing](#crawling--indexing)
10. [Technical SEO Auditing](#technical-seo-auditing)

## HTML & Semantic Structure

### Document Structure Best Practices
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Essential head elements -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <!-- SEO critical meta tags -->
    <title>John Doe | React Developer in San Francisco</title>
    <meta name="description" content="Senior React Developer with 8+ years building scalable web applications. Specializing in React, Node.js, and TypeScript.">

    <!-- Canonical URL -->
    <link rel="canonical" href="https://johndoe.dev">

    <!-- Preconnect to external domains -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- DNS prefetch for external resources -->
    <link rel="dns-prefetch" href="//github.com">
    <link rel="dns-prefetch" href="//linkedin.com">
</head>
<body>
    <!-- Skip navigation for accessibility -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- Header with navigation -->
    <header>
        <nav role="navigation" aria-label="Main navigation">
            <!-- Navigation structure -->
        </nav>
    </header>

    <!-- Main content area -->
    <main id="main-content">
        <!-- Content sections with proper heading hierarchy -->
    </main>

    <!-- Footer -->
    <footer>
        <!-- Footer content -->
    </footer>
</body>
</html>
```

### Semantic HTML5 Structure
```html
<main>
    <!-- About Section -->
    <section id="about" aria-labelledby="about-heading">
        <h1 id="about-heading">John Doe - Senior React Developer</h1>

        <article class="about-content">
            <h2>About Me</h2>
            <p>San Francisco-based senior React developer with 8+ years of experience...</p>

            <!-- Skills list -->
            <section aria-labelledby="skills-heading">
                <h3 id="skills-heading">Technical Skills</h3>
                <ul>
                    <li><span class="skill-category">Frontend:</span> React, TypeScript, Next.js</li>
                    <li><span class="skill-category">Backend:</span> Node.js, Express, Python</li>
                </ul>
            </section>
        </article>
    </section>

    <!-- Projects Section -->
    <section id="projects" aria-labelledby="projects-heading">
        <h2 id="projects-heading">Projects</h2>

        <article class="project" itemscope itemtype="https://schema.org/Project">
            <h3 itemprop="name">E-commerce Platform</h3>
            <p itemprop="description">Full-stack e-commerce solution...</p>

            <div class="tech-stack">
                <h4>Technologies Used:</h4>
                <ul>
                    <li itemprop="programmingLanguage">React</li>
                    <li itemprop="programmingLanguage">Node.js</li>
                    <li itemprop="programmingLanguage">MongoDB</li>
                </ul>
            </div>

            <div class="project-links">
                <a href="https://github.com/johndoe/ecommerce"
                   itemprop="codeRepository"
                   target="_blank"
                   rel="noopener noreferrer">
                    View Source Code
                </a>
                <a href="https://ecommerce-demo.com"
                   itemprop="url"
                   target="_blank"
                   rel="noopener noreferrer">
                    Live Demo
                </a>
            </div>
        </article>
    </section>

    <!-- Contact Section -->
    <section id="contact" aria-labelledby="contact-heading">
        <h2 id="contact-heading">Get In Touch</h2>

        <address>
            <p>Email: <a href="mailto:john@johndoe.dev">john@johndoe.dev</a></p>
            <p>Location: San Francisco, CA</p>
        </address>
    </section>
</main>
```

### Heading Hierarchy Optimization
```html
<!-- ✅ Correct heading structure -->
<h1>John Doe - Senior React Developer</h1>
  <h2>About Me</h2>
    <h3>Technical Skills</h3>
      <h4>Frontend Technologies</h4>
      <h4>Backend Technologies</h4>
    <h3>Experience</h3>
      <h4>Tech Company Inc</h4>
  <h2>Projects</h2>
    <h3>E-commerce Platform</h3>
      <h4>Technical Implementation</h4>
      <h4>Results & Impact</h4>
    <h2>Contact</h2>

<!-- ❌ Incorrect heading structure -->
<h3>About Me</h3>  <!-- Should be h1 or h2 -->
  <h5>Skills</h5>  <!-- Skips h4 -->
<h1>Projects</h1>  <!-- Multiple h1s -->
  <h2>Details</h2>
```

## Meta Tags Implementation

### Complete Meta Tag Setup
```html
<head>
    <!-- Basic Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <!-- SEO Essentials -->
    <title>John Doe | React Developer in San Francisco | Full Stack Engineer</title>
    <meta name="description" content="Senior React Developer with 8+ years building scalable web applications. Specializing in React, Node.js, and TypeScript. Available for opportunities in San Francisco.">
    <meta name="keywords" content="react developer, node.js developer, full stack developer, san francisco, typescript, javascript developer, senior developer">

    <!-- Author & Copyright -->
    <meta name="author" content="John Doe">
    <meta name="copyright" content="John Doe">
    <meta name="generator" content="Custom built with Next.js">

    <!-- Robots & Indexing -->
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <meta name="bingbot" content="index, follow">

    <!-- Canonical URL -->
    <link rel="canonical" href="https://johndoe.dev">

    <!-- Alternative Language Versions -->
    <link rel="alternate" hreflang="en" href="https://johndoe.dev">
    <link rel="alternate" hreflang="x-default" href="https://johndoe.dev">

    <!-- Open Graph (Facebook/LinkedIn) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="John Doe | React Developer in San Francisco">
    <meta property="og:description" content="Senior React Developer with 8+ years building scalable web applications. Specializing in React, Node.js, and TypeScript.">
    <meta property="og:url" content="https://johndoe.dev">
    <meta property="og:site_name" content="John Doe - Portfolio">
    <meta property="og:image" content="https://johndoe.dev/images/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="John Doe - Senior React Developer">
    <meta property="og:locale" content="en_US">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@johndoe">
    <meta name="twitter:creator" content="@johndoe">
    <meta name="twitter:title" content="John Doe | React Developer in San Francisco">
    <meta name="twitter:description" content="Senior React Developer with 8+ years building scalable web applications. Specializing in React, Node.js, and TypeScript.">
    <meta name="twitter:image" content="https://johndoe.dev/images/og-image.jpg">

    <!-- Additional Meta Tags -->
    <meta name="theme-color" content="#317EFB">
    <meta name="msapplication-TileColor" content="#317EFB">
    <meta name="application-name" content="John Doe Portfolio">
    <meta name="apple-mobile-web-app-title" content="John Doe">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">

    <!-- Favicon -->
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
</head>
```

### Dynamic Meta Tag Generation (Next.js Example)
```javascript
// pages/_app.js or layout component
import Head from 'next/head';

function SEOHead({ pageData }) {
  const { title, description, image, url, type = 'website' } = pageData;

  return (
    <Head>
      {/* Basic SEO */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={url} />

      {/* Open Graph */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={url} />
      <meta property="og:image" content={image} />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
    </Head>
  );
}
```

## URL Structure Optimization

### SEO-Friendly URL Patterns
```javascript
// ✅ Good URL structure
const routes = {
  homepage: '/',
  about: '/about',
  projects: '/projects',
  projectDetail: '/projects/[slug]', // /projects/ecommerce-platform
  contact: '/contact',
  skills: '/skills',
  blog: '/blog',
  blogPost: '/blog/[slug]' // /blog/react-performance-tips
};

// ❌ Bad URL structure
const badRoutes = {
  homepage: '/index.html',
  about: '/page.php?id=2',
  projects: '/portfolio.php',
  projectDetail: '/project-details.php?project=123'
};
```

### Dynamic Route Parameters
```javascript
// pages/projects/[slug].js
export async function getStaticPaths() {
  const projects = await getProjects();
  const paths = projects.map(project => ({
    params: { slug: project.slug }
  }));

  return {
    paths,
    fallback: 'blocking' // Generate new pages on-demand
  };
}

export async function getStaticProps({ params }) {
  const project = await getProject(params.slug);

  return {
    props: {
      project,
      // Additional SEO data
      seo: {
        title: `${project.name} - Project by John Doe`,
        description: project.description,
        image: project.image,
        url: `https://johndoe.dev/projects/${params.slug}`
      }
    },
    revalidate: 60 // Revalidate every minute
  };
}
```

### URL Best Practices Checklist
```markdown
- [ ] Use lowercase letters in URLs
- [ ] Use hyphens (-) instead of underscores (_)
- [ ] Keep URLs under 60 characters
- [ ] Include target keywords naturally
- [ ] Avoid special characters except hyphens
- [ ] Use meaningful, descriptive URLs
- [ ] Implement trailing slashes consistently
- [ ] Remove stop words (and, the, of) from URLs
- [ ] Use HTTPS protocol
- [ ] Implement proper redirects for URL changes
```

## Image SEO Best Practices

### Optimized Image Implementation
```html
<!-- Optimized image with SEO attributes -->
<img
  src="/images/react-project-screenshot.jpg"
  alt="E-commerce platform built with React and Node.js - showing product listing page"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
  importance="low"
  sizes="(max-width: 768px) 100vw, 50vw"
  srcset="
    /images/react-project-screenshot-400w.jpg 400w,
    /images/react-project-screenshot-800w.jpg 800w,
    /images/react-project-screenshot-1200w.jpg 1200w
  "
>
```

### Next.js Image Component
```javascript
import Image from 'next/image';

function ProjectImage({ src, alt, priority = false }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      priority={priority} // Priority for above-the-fold images
      placeholder="blur" // or "empty"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..." // Small blur data URL
      sizes="(max-width: 768px) 100vw, 50vw"
      quality={85} // 0-100, default 75
    />
  );
}
```

### Image SEO Checklist
```markdown
### Alt Text Guidelines
- [ ] Descriptive alt text for all images
- [ ] Alt text under 125 characters
- [ ] Include relevant keywords naturally
- [ ] Decorative images use empty alt=""
- [ ] Test alt text with screen readers

### File Optimization
- [ ] Compress images before upload
- [ ] Use WebP format when supported
- [ ] Implement responsive images
- [ ] Use lazy loading for below-the-fold images
- [ ] Serve appropriate image sizes

### File Naming
- [ ] Use descriptive file names
- [ ] Separate words with hyphens
- [ ] Include target keywords
- [ ] Keep names concise
- [ ] Example: "react-ecommerce-platform.jpg"
```

### SVG Optimization
```html
<!-- Optimized SVG with SEO attributes -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 100 100"
  aria-label="React Logo"
  role="img"
>
  <title>React Framework Logo</title>
  <desc>Official React JavaScript framework logo</desc>
  <!-- SVG content -->
</svg>
```

## JavaScript SEO for React/Next.js

### Server-Side Rendering (SSR) Implementation
```javascript
// pages/index.js - SSR implementation
export async function getServerSideProps(context) {
  const { req, res } = context;

  // Fetch data on server
  const projects = await getFeaturedProjects();
  const profile = await getProfileData();

  return {
    props: {
      projects,
      profile,
      // Pre-rendered SEO data
      seo: {
        title: `${profile.name} | ${profile.title} in ${profile.location}`,
        description: profile.description,
        structuredData: generateStructuredData(profile, projects)
      }
    }
  };
}
```

### Static Site Generation (SSG)
```javascript
// pages/projects/[slug].js - SSG with ISR
export async function getStaticProps({ params }) {
  const project = await getProject(params.slug);

  return {
    props: {
      project,
      seo: {
        title: `${project.name} - Project by ${project.author}`,
        description: project.description,
        openGraph: {
          'og:image': project.image,
          'og:type': 'article'
        }
      }
    },
    revalidate: 3600 // Revalidate every hour
  };
}
```

### Client-Side SEO Considerations
```javascript
// Dynamic content loading with SEO
import { useState, useEffect } from 'react';
import Head from 'next/head';

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [seoData, setSeoData] = useState({});

  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await fetchProjects();
        setProjects(data.projects);

        // Update SEO dynamically
        setSeoData({
          title: `Featured Projects | ${data.total} React Applications`,
          description: `Explore ${data.total} React projects including ${data.projects.slice(0, 3).map(p => p.name).join(', ')}`
        });

        // Update document title
        document.title = seoData.title;

        // Update meta description
        updateMetaDescription(seoData.description);

      } catch (error) {
        console.error('Failed to load projects:', error);
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  return (
    <>
      <Head>
        <title>{seoData.title || 'Projects - Portfolio'}</title>
        <meta name="description" content={seoData.description || 'Browse my portfolio of development projects.'} />
      </Head>

      <section>
        <h1>My Projects</h1>
        {loading ? (
          <div>Loading projects...</div>
        ) : (
          <div>{/* Project content */}</div>
        )}
      </section>
    </>
  );
}

function updateMetaDescription(description) {
  let metaDesc = document.querySelector('meta[name="description"]');
  if (!metaDesc) {
    metaDesc = document.createElement('meta');
    metaDesc.name = 'description';
    document.head.appendChild(metaDesc);
  }
  metaDesc.content = description;
}
```

### SEO-Friendly Routing
```javascript
// components/SEOHead.js
import Head from 'next/head';

export default function SEOHead({ seo }) {
  return (
    <Head>
      <title>{seo.title}</title>
      <meta name="description" content={seo.description} />

      {seo.keywords && <meta name="keywords" content={seo.keywords} />}

      {/* Open Graph */}
      <meta property="og:title" content={seo.title} />
      <meta property="og:description" content={seo.description} />
      <meta property="og:url" content={seo.url} />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={seo.title} />
      <meta name="twitter:description" content={seo.description} />

      {/* Canonical URL */}
      <link rel="canonical" href={seo.url} />

      {/* Structured Data */}
      {seo.structuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(seo.structuredData)
          }}
        />
      )}
    </Head>
  );
}
```

## Performance Optimization

### Critical CSS Optimization
```javascript
// pages/_document.js
import Document, { Html, Head, Main, NextScript } from 'next/document';

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  render() {
    return (
      <Html lang="en">
        <Head>
          {/* Critical CSS inline */}
          <style dangerouslySetInnerHTML={{
            __html: `
              /* Critical above-the-fold styles */
              body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
              .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
              .hero { min-height: 60vh; display: flex; align-items: center; }
            `
          }} />

          {/* Preload critical resources */}
          <link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossOrigin="" />
          <link rel="preload" href="/images/hero-bg.jpg" as="image" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
```

### Bundle Optimization
```javascript
// next.config.js
module.exports = {
  // Production optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Bundle analysis
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      };
    }
    return config;
  },

  // Image optimization
  images: {
    domains: ['example.com'],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60 * 60 * 24 * 365, // 1 year
  },

  // Compression
  compress: true,

  // Experimental features
  experimental: {
    optimizeCss: true,
  },
};
```

### Core Web Vitals Optimization
```javascript
// utils/performance.js
export function reportWebVitals(metric) {
  // Send metrics to analytics service
  if (window.gtag) {
    window.gtag('event', metric.name, {
      event_category: 'Web Vitals',
      event_label: metric.id,
      value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
      non_interaction: true,
    });
  }

  // Console logging for development
  if (process.env.NODE_ENV === 'development') {
    console.log(`[Web Vitals] ${metric.name}:`, metric.value);
  }
}

// components/LazyImage.js
import { useState, useRef, useEffect } from 'react';

export default function LazyImage({ src, alt, className, ...props }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef} className={`relative ${className}`}>
      {isInView && (
        <img
          src={src}
          alt={alt}
          loading="lazy"
          onLoad={() => setIsLoaded(true)}
          className={`transition-opacity duration-300 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
          {...props}
        />
      )}
      {!isLoaded && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
    </div>
  );
}
```

## Mobile SEO Implementation

### Responsive Meta Tags
```html
<head>
  <!-- Viewport optimization -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">

  <!-- Mobile-specific optimizations -->
  <meta name="format-detection" content="telephone=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="theme-color" content="#317EFB">

  <!-- Apple touch icons -->
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
  <link rel="apple-touch-icon" sizes="167x167" href="/apple-touch-icon-167x167.png">
  <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
  <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">

  <!-- Android manifest -->
  <link rel="manifest" href="/site.webmanifest">
</head>
```

### Mobile-First CSS
```css
/* Mobile-first responsive design */
.container {
  width: 100%;
  padding: 0 1rem;
  margin: 0 auto;
}

/* Navigation - Mobile first */
.nav {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.nav-toggle {
  display: block;
  background: none;
  border: none;
  font-size: 1.5rem;
}

.nav-menu {
  display: none;
  flex-direction: column;
  gap: 1rem;
}

.nav-menu.active {
  display: flex;
}

/* Tablets */
@media (min-width: 768px) {
  .container {
    max-width: 768px;
    padding: 0 2rem;
  }

  .nav {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .nav-toggle {
    display: none;
  }

  .nav-menu {
    display: flex;
    flex-direction: row;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: 0 4rem;
  }
}

/* Touch targets for mobile */
.btn, .nav-link {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* Readability on mobile */
body {
  font-size: 16px;
  line-height: 1.6;
}

@media (min-width: 768px) {
  body {
    font-size: 18px;
  }
}
```

## Schema Markup Technical Guide

### JSON-LD Implementation
```javascript
// utils/structuredData.js
export function generatePersonSchema(profile) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: profile.name,
    jobTitle: profile.title,
    description: profile.description,
    url: profile.url,
    email: profile.email,
    telephone: profile.phone,
    address: {
      '@type': 'PostalAddress',
      addressLocality: profile.location
    },
    sameAs: [
      `https://github.com/${profile.github}`,
      `https://linkedin.com/in/${profile.linkedin}`,
      `https://twitter.com/${profile.twitter}`
    ],
    knowsAbout: profile.skills.slice(0, 10),
    alumniOf: profile.education.map(edu => ({
      '@type': 'EducationalOrganization',
      name: edu.institution
    })),
    seeks: profile.availableForHire ? {
      '@type': 'JobPosting',
      title: profile.title,
      description: `${profile.name} is looking for new opportunities`,
      employmentType: ['FULL_TIME', 'CONTRACTOR']
    } : undefined
  };
}

export function generateProjectSchema(project, author) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Project',
    name: project.name,
    description: project.description,
    url: project.url,
    codeRepository: project.repositoryUrl,
    programmingLanguage: project.technologies,
    dateCreated: project.startDate,
    dateModified: project.updatedAt,
    author: {
      '@type': 'Person',
      name: author.name,
      url: author.url
    },
    keywords: project.tags.join(', '),
    screenshot: project.images[0],
    potentialAction: {
      '@type': 'ViewAction',
      target: project.url,
      name: 'View Live Demo'
    }
  };
}
```

### Dynamic Schema Generation
```javascript
// pages/projects/[slug].js
import Head from 'next/head';
import { generateProjectSchema, generatePersonSchema } from '../../utils/structuredData';

function ProjectPage({ project, author }) {
  const structuredData = [
    generateProjectSchema(project, author),
    generatePersonSchema(author)
  ];

  return (
    <>
      <Head>
        <title>{project.name} - Project by {author.name}</title>
        <meta name="description" content={project.description} />

        {/* Structured Data */}
        {structuredData.map((schema, index) => (
          <script
            key={index}
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify(schema)
            }}
          />
        ))}
      </Head>

      <main>
        {/* Project content */}
      </main>
    </>
  );
}
```

## Crawling & Indexing

### robots.txt Configuration
```txt
# robots.txt for developer portfolio
User-agent: *
Allow: /

# Block crawling of sensitive directories
Disallow: /api/
Disallow: /admin/
Disallow: /_next/static/
Disallow: /.well-known/

# Allow crawling of important resources
Allow: /images/
Allow: /css/
Allow: /js/

# Sitemap location
Sitemap: https://johndoe.dev/sitemap.xml
Sitemap: https://johndoe.dev/sitemap-projects.xml

# Crawl delay (optional)
Crawl-delay: 1
```

### XML Sitemap Generation
```javascript
// pages/sitemap.xml.js
import { getServerSideProps } from 'next/server';

export default function Sitemap() {
  // This component is never actually rendered
  return null;
}

export async function getServerSideProps({ res }) {
  const baseUrl = 'https://johndoe.dev';

  // Static pages
  const staticPages = [
    { url: '', changefreq: 'weekly', priority: 1.0 },
    { url: '/about', changefreq: 'monthly', priority: 0.8 },
    { url: '/projects', changefreq: 'weekly', priority: 0.9 },
    { url: '/contact', changefreq: 'monthly', priority: 0.7 },
    { url: '/skills', changefreq: 'monthly', priority: 0.8 }
  ];

  // Dynamic pages (projects, blog posts)
  const projects = await getProjects();
  const projectPages = projects.map(project => ({
    url: `/projects/${project.slug}`,
    changefreq: 'monthly',
    priority: 0.8,
    lastmod: project.updatedAt
  }));

  // Build sitemap XML
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      ${[...staticPages, ...projectPages].map(page => `
        <url>
          <loc>${baseUrl}${page.url}</loc>
          <lastmod>${page.lastmod || new Date().toISOString()}</lastmod>
          <changefreq>${page.changefreq}</changefreq>
          <priority>${page.priority}</priority>
        </url>
      `).join('')}
    </urlset>`;

  res.setHeader('Content-Type', 'text/xml');
  res.write(sitemap);
  res.end();

  return {
    props: {},
  };
}
```

### HTTP Headers for SEO
```javascript
// pages/_middleware.js (Next.js middleware)
import { NextResponse } from 'next/server';

export function middleware(request) {
  const response = NextResponse.next();

  // Add security and SEO headers
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');

  // Cache static assets
  if (request.nextUrl.pathname.startsWith('/images/') ||
      request.nextUrl.pathname.startsWith('/static/')) {
    response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
  }

  return response;
}
```

## Technical SEO Auditing

### Lighthouse Configuration
```javascript
// next.config.js - Lighthouse configuration
module.exports = {
  experimental: {
    lighthouse: {
      // Enable Lighthouse auditing
      enabled: true,

      // Configure Lighthouse settings
      settings: {
        extends: 'lighthouse:default',
        settings: {
          onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
          throttling: {
            rttMs: 40,
            throughputKbps: 10240,
            cpuSlowdownMultiplier: 1,
            requestLatencyMs: 0,
            downloadThroughputKbps: 0,
            uploadThroughputKbps: 0
          }
        }
      }
    }
  }
};
```

### SEO Audit Automation
```javascript
// scripts/seo-audit.js
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runSEOAudit(url) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  const options = {
    logLevel: 'info',
    output: 'json',
    onlyCategories: ['seo', 'performance'],
    port: chrome.port
  };

  const runnerResult = await lighthouse(url, options);
  await chrome.kill();

  const { lhr } = runnerResult;

  // Extract SEO metrics
  const seoScore = lhr.categories.seo.score * 100;
  const performanceScore = lhr.categories.performance.score * 100;

  // Check specific SEO elements
  const audits = lhr.audits;

  const auditResults = {
    overallScore: Math.round((seoScore + performanceScore) / 2),
    seo: {
      score: Math.round(seoScore),
      title: audits['seo-title'].score,
      description: audits['meta-description'].score,
      headingStructure: audits['heading-order'].score,
      imageAlt: audits['image-alt'].score,
      crawlable: audits['is-crawlable'].score,
      robotsTxt: audits['robots-txt'].score,
      sitemap: audits['sitemap'].score
    },
    performance: {
      score: Math.round(performanceScore),
      lcp: audits['largest-contentful-paint'].displayValue,
      fid: audits['max-potential-fid'].displayValue,
      cls: audits['cumulative-layout-shift'].displayValue
    },
    recommendations: generateRecommendations(audits)
  };

  return auditResults;
}

function generateRecommendations(audits) {
  const recommendations = [];

  if (audits['seo-title'].score < 1) {
    recommendations.push('Optimize your title tag (50-60 characters)');
  }

  if (audits['meta-description'].score < 1) {
    recommendations.push('Add a compelling meta description (120-160 characters)');
  }

  if (audits['image-alt'].score < 1) {
    recommendations.push('Add descriptive alt text to all images');
  }

  if (audits['is-crawlable'].score < 1) {
    recommendations.push('Fix crawling issues in your robots.txt');
  }

  return recommendations;
}

// Usage
runSEOAudit('https://johndoe.dev')
  .then(results => console.log(JSON.stringify(results, null, 2)))
  .catch(error => console.error('Audit failed:', error));
```

### Technical SEO Checklist
```markdown
### HTML Structure
- [ ] Valid HTML5 markup
- [ ] Semantic HTML elements
- [ ] Proper heading hierarchy (one H1 per page)
- [ ] Language declaration (lang="en")
- [ ] DOCTYPE declaration

### Meta Tags
- [ ] Unique title tags (50-60 chars)
- [ ] Meta descriptions (120-160 chars)
- [ ] Meta keywords (optional, 15-20 max)
- [ ] Canonical URL for each page
- [ ] Charset declaration (UTF-8)
- [ ] Viewport meta tag

### URL Structure
- [ ] Clean, descriptive URLs
- [ ] Hyphens instead of underscores
- [ ] Lowercase letters
- [ ] No special characters
- [ ] HTTPS protocol
- [ ] Consistent trailing slashes

### Images
- [ ] Alt text for all images
- [ ] Optimized file sizes
- [ ] Responsive images
- [ ] Lazy loading
- [ ] Descriptive file names

### Performance
- [ ] Page load time < 3 seconds
- [ ] Core Web Vitals passing
- [ ] Gzip compression enabled
- [ ] Browser caching
- [ ] Minified CSS/JS
- [ ] Optimized images

### Mobile SEO
- [ ] Responsive design
- [ ] Mobile-friendly navigation
- [ ] Touch-friendly buttons (44px min)
- [ ] Readable font sizes (16px min)
- [ ] No horizontal scrolling

### Technical Elements
- [ ] XML sitemap
- [ ] robots.txt configured
- [ ] Structured data implemented
- [ ] No broken links
- [ ] Proper redirects (301)
- [ ] HTTPS certificate

### Monitoring
- [ ] Google Search Console setup
- [ ] Google Analytics tracking
- [ ] Core Web Vitals monitoring
- [ ] Regular SEO audits
- [ ] Error tracking
```

This comprehensive technical SEO guide provides the essential implementation details for optimizing developer portfolios at the technical level, covering everything from basic HTML structure to advanced performance optimization and automation.