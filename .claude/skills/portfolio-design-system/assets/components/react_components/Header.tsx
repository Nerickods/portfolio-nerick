import React, { useState } from 'react';

export interface NavigationItem {
  id: string;
  label: string;
  href: string;
  active?: boolean;
  external?: boolean;
}

export interface HeaderProps {
  logo?: React.ReactNode;
  navigation: NavigationItem[];
  mobileMenuOpen?: boolean;
  onMobileMenuToggle?: (open: boolean) => void;
  showThemeToggle?: boolean;
  className?: string;
  'data-testid'?: string;
}

/**
 * Navigation header component with responsive menu and accessibility features
 * @component
 */
export const Header: React.FC<HeaderProps> = ({
  logo,
  navigation,
  mobileMenuOpen = false,
  onMobileMenuToggle,
  showThemeToggle = false,
  className = '',
  'data-testid': testId
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(mobileMenuOpen);

  const handleMenuToggle = () => {
    const newState = !isMenuOpen;
    setIsMenuOpen(newState);
    onMobileMenuToggle?.(newState);
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Escape' && isMenuOpen) {
      setIsMenuOpen(false);
      onMobileMenuToggle?.(false);
    }
  };

  return (
    <header
      className={HeaderClassNames({ className })}
      data-testid={testId || 'header'}
      onKeyDown={handleKeyDown}
    >
      <nav
        className="header-nav"
        role="navigation"
        aria-label="Main navigation"
      >
        <div className="header-container">
          {/* Logo */}
          {logo && (
            <div className="header-logo">
              <a
                href="/"
                className="header-logo-link"
                aria-label="Home"
              >
                {logo}
              </a>
            </div>
          )}

          {/* Desktop Navigation */}
          <ul className="header-navigation header-navigation--desktop">
            {navigation.map((item) => (
              <li key={item.id} className="header-nav-item">
                <a
                  href={item.href}
                  className={`header-nav-link ${item.active ? 'header-nav-link--active' : ''}`}
                  aria-current={item.active ? 'page' : undefined}
                  target={item.external ? '_blank' : undefined}
                  rel={item.external ? 'noopener noreferrer' : undefined}
                >
                  {item.label}
                  {item.external && (
                    <span className="header-nav-external-icon" aria-hidden="true">
                      ↗
                    </span>
                  )}
                </a>
              </li>
            ))}
          </ul>

          {/* Right side actions */}
          <div className="header-actions">
            {showThemeToggle && (
              <button
                className="header-theme-toggle"
                aria-label="Toggle theme"
                data-testid="theme-toggle"
              >
                <span className="header-theme-icon header-theme-icon--light">
                  ☀️
                </span>
                <span className="header-theme-icon header-theme-icon--dark">
                  🌙
                </span>
              </button>
            )}

            {/* Mobile menu button */}
            <button
              className="header-menu-button"
              onClick={handleMenuToggle}
              aria-expanded={isMenuOpen}
              aria-controls="mobile-menu"
              aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
              data-testid="mobile-menu-button"
            >
              <span className="header-menu-icon">
                <span className="header-menu-line"></span>
                <span className="header-menu-line"></span>
                <span className="header-menu-line"></span>
              </span>
              <span className="sr-only">Toggle navigation menu</span>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div
          id="mobile-menu"
          className={`header-mobile-menu ${isMenuOpen ? 'header-mobile-menu--open' : ''}`}
          aria-hidden={!isMenuOpen}
        >
          <ul className="header-navigation header-navigation--mobile">
            {navigation.map((item) => (
              <li key={item.id} className="header-nav-item">
                <a
                  href={item.href}
                  className={`header-nav-link ${item.active ? 'header-nav-link--active' : ''}`}
                  aria-current={item.active ? 'page' : undefined}
                  target={item.external ? '_blank' : undefined}
                  rel={item.external ? 'noopener noreferrer' : undefined}
                  onClick={() => {
                    setIsMenuOpen(false);
                    onMobileMenuToggle?.(false);
                  }}
                >
                  {item.label}
                  {item.external && (
                    <span className="header-nav-external-icon" aria-hidden="true">
                      ↗
                    </span>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    </header>
  );
};

// Helper function for CSS classes
const HeaderClassNames = ({ className }: { className: string }) => {
  const baseClasses = [
    'header-component',
    'bg-white',
    'dark:bg-neutral-900',
    'border-b',
    'border-neutral-200',
    'dark:border-neutral-700',
    'sticky',
    'top-0',
    'z-50',
    'transition-all',
    'duration-300'
  ];

  return [...baseClasses, className].filter(Boolean).join(' ');
};