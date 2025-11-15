import React from 'react';

export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: (event: React.MouseEvent) => void;
  type?: 'button' | 'submit' | 'reset';
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
  className?: string;
  'data-testid'?: string;
}

/**
 * Interactive button component with multiple variants and sizes
 * @component
 */
export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
  loading = false,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  'data-testid': testId,
  ...rest
}) => {
  const buttonClass = ButtonClassNames({
    variant,
    size,
    disabled,
    loading,
    fullWidth,
    className
  });

  return (
    <button
      type={type}
      className={buttonClass}
      onClick={onClick}
      disabled={disabled || loading}
      data-testid={testId || 'button'}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      {...rest}
    >
      {loading && (
        <span className="button-spinner" aria-hidden="true">
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </span>
      )}

      {icon && iconPosition === 'left' && (
        <span className="button-icon-left" aria-hidden="true">
          {icon}
        </span>
      )}

      <span className="button-text">{children}</span>

      {icon && iconPosition === 'right' && (
        <span className="button-icon-right" aria-hidden="true">
          {icon}
        </span>
      )}
    </button>
  );
};

// Helper function for CSS classes
const ButtonClassNames = ({
  variant,
  size,
  disabled,
  loading,
  fullWidth,
  className
}: Omit<ButtonProps, 'children' | 'onClick' | 'type' | 'icon' | 'iconPosition'> & { className: string }) => {
  const baseClasses = [
    'button-component',
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'rounded-lg',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2'
  ];

  // Variant classes
  const variantClasses = {
    primary: [
      'bg-primary-600',
      'text-white',
      'border',
      'border-transparent',
      'hover:bg-primary-700',
      'focus:ring-primary-500',
      'active:bg-primary-800'
    ],
    secondary: [
      'bg-secondary-600',
      'text-white',
      'border',
      'border-transparent',
      'hover:bg-secondary-700',
      'focus:ring-secondary-500',
      'active:bg-secondary-800'
    ],
    outline: [
      'bg-transparent',
      'text-primary-600',
      'border-2',
      'border-primary-600',
      'hover:bg-primary-50',
      'focus:ring-primary-500',
      'active:bg-primary-100'
    ],
    ghost: [
      'bg-transparent',
      'text-primary-600',
      'border',
      'border-transparent',
      'hover:bg-primary-50',
      'focus:ring-primary-500',
      'active:bg-primary-100'
    ]
  };

  // Size classes
  const sizeClasses = {
    sm: ['px-3', 'py-1.5', 'text-sm', 'min-h-[32px]'],
    md: ['px-4', 'py-2', 'text-base', 'min-h-[40px]'],
    lg: ['px-6', 'py-3', 'text-lg', 'min-h-[48px]']
  };

  // State classes
  const stateClasses = [];
  if (disabled) {
    stateClasses.push('opacity-50', 'cursor-not-allowed');
  }
  if (loading) {
    stateClasses.push('opacity-75', 'cursor-wait');
  }
  if (fullWidth) {
    stateClasses.push('w-full');
  }

  return [
    ...baseClasses,
    ...variantClasses[variant],
    ...sizeClasses[size],
    ...stateClasses,
    className
  ].filter(Boolean).join(' ');
};