import React from 'react';

export interface HeroProps {
  title: string;
  subtitle?: string;
  cta?: React.ReactNode;
  background?: 'gradient' | 'image' | 'pattern' | 'color';
  backgroundImage?: string;
  variant?: 'centered' | 'left-aligned' | 'split';
  size?: 'compact' | 'default' | 'large';
  className?: string;
  'data-testid'?: string;
}

/**
 * Hero section component for landing pages with multiple layout variants
 * @component
 */
export const Hero: React.FC<HeroProps> = ({
  title,
  subtitle,
  cta,
  background = 'gradient',
  backgroundImage,
  variant = 'centered',
  size = 'default',
  className = '',
  'data-testid': testId
}) => {
  const heroClass = HeroClassNames({ variant, size, background, className });
  const hasBackgroundImage = background === 'image' && backgroundImage;

  return (
    <section
      className={heroClass}
      data-testid={testId || 'hero'}
      aria-labelledby="hero-title"
    >
      {/* Background overlay for images */}
      {hasBackgroundImage && (
        <div
          className="hero-background-image"
          style={{ backgroundImage: `url(${backgroundImage})` }}
          aria-hidden="true"
        />
      )}

      {/* Content wrapper */}
      <div className="hero-container">
        <div className={HeroContentClassNames({ variant, hasCta: !!cta })}>
          <div className="hero-text-content">
            <h1
              id="hero-title"
              className="hero-title"
            >
              {title}
            </h1>

            {subtitle && (
              <p className="hero-subtitle">
                {subtitle}
              </p>
            )}

            {cta && (
              <div className="hero-cta">
                {cta}
              </div>
            )}
          </div>

          {/* Split layout - right side content */}
          {variant === 'split' && (
            <div className="hero-visual-content">
              {/* Visual content placeholder for split layout */}
              <div className="hero-visual-placeholder">
                <span aria-hidden="true">💻🚀</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Scroll indicator */}
      {size !== 'compact' && (
        <div className="hero-scroll-indicator" aria-hidden="true">
          <span className="hero-scroll-line"></span>
          <span className="hero-scroll-arrow">↓</span>
        </div>
      )}
    </section>
  );
};

// Helper function for CSS classes
const HeroClassNames = ({
  variant,
  size,
  background,
  className
}: {
  variant: string;
  size: string;
  background: string;
  className: string;
}) => {
  const baseClasses = [
    'hero-component',
    'relative',
    'overflow-hidden',
    'transition-all',
    'duration-500'
  ];

  // Size classes
  const sizeClasses = {
    compact: ['min-h-[60vh]', 'py-16'],
    default: ['min-h-[80vh]', 'py-20'],
    large: ['min-h-screen', 'py-24']
  };

  // Background classes
  const backgroundClasses = {
    gradient: [
      'bg-gradient-to-br',
      'from-primary-50',
      'via-white',
      'to-secondary-50',
      'dark:from-neutral-900',
      'dark:via-neutral-800',
      'dark:to-primary-900'
    ],
    image: ['bg-neutral-900'],
    pattern: [
      'bg-white',
      'dark:bg-neutral-900',
      'bg-pattern'
    ],
    color: [
      'bg-primary-600',
      'dark:bg-primary-800'
    ]
  };

  // Variant-specific classes
  const variantClasses = {
    centered: ['flex', 'items-center', 'justify-center'],
    'left-aligned': ['flex', 'items-start', 'justify-start'],
    split: ['flex', 'items-center']
  };

  return [
    ...baseClasses,
    ...sizeClasses[size],
    ...backgroundClasses[background],
    ...variantClasses[variant],
    className
  ].filter(Boolean).join(' ');
};

const HeroContentClassNames = ({
  variant,
  hasCta
}: {
  variant: string;
  hasCta: boolean;
}) => {
  const baseClasses = [
    'hero-content',
    'relative',
    'z-10',
    'text-center',
    'sm:text-left'
  ];

  const variantClasses = {
    centered: [
      'max-w-4xl',
      'mx-auto',
      'text-center',
      'sm:text-center'
    ],
    'left-aligned': [
      'max-w-4xl',
      'text-left'
    ],
    split: [
      'max-w-7xl',
      'mx-auto',
      'grid',
      'grid-cols-1',
      'lg:grid-cols-2',
      'gap-12',
      'items-center'
    ]
  };

  const spacingClasses = hasCta ? ['space-y-8'] : ['space-y-6'];

  return [
    ...baseClasses,
    ...variantClasses[variant],
    ...spacingClasses
  ].filter(Boolean).join(' ');
};