/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './assets/components/**/*.{js,ts,jsx,tsx}',
    './templates/**/*.{js,ts,jsx,tsx,html}',
    './references/**/*.{md,html}',
    './scripts/**/*.py'
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        // Portfolio-specific color palette
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554'
        },
        secondary: {
          50: '#fdf4ff',
          100: '#fae8ff',
          200: '#f5d0fe',
          300: '#f0abfc',
          400: '#e879f9',
          500: '#d946ef',
          600: '#c026d3',
          700: '#a21caf',
          800: '#86198f',
          900: '#701a75'
        },
        neutral: {
          0: '#ffffff',
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0a0a0a'
        },
        // Technology colors for skill displays
        tech: {
          javascript: '#f7df1e',
          typescript: '#3178c6',
          react: '#61dafb',
          vue: '#4fc08d',
          angular: '#dd0031',
          nodejs: '#339933',
          python: '#3776ab',
          java: '#007396',
          docker: '#2496ed',
          kubernetes: '#326ce5',
          aws: '#ff9900',
          azure: '#0078d4',
          gcp: '#4285f4',
          html: '#e34f26',
          css: '#1572b6',
          git: '#f05032',
          github: '#181717'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Merriweather', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace']
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
        '7xl': ['4.5rem', { lineHeight: '1' }],
        '8xl': ['6rem', { lineHeight: '1' }],
        '9xl': ['8rem', { lineHeight: '1' }]
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
        '144': '36rem'
      },
      maxWidth: {
        '8xl': '88rem',
        '9xl': '96rem'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'bounce-slow': 'bounce 2s infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        }
      },
      boxShadow: {
        'portfolio': '0 4px 14px 0 rgba(0, 0, 0, 0.1)',
        'portfolio-lg': '0 10px 40px rgba(0, 0, 0, 0.15)',
        'portfolio-xl': '0 20px 60px rgba(0, 0, 0, 0.2)',
        'inner-portfolio': 'inset 0 2px 4px rgba(0, 0, 0, 0.06)'
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem'
      },
      backdropBlur: {
        xs: '2px'
      },
      screens: {
        '3xl': '1600px'
      }
    }
  },
  plugins: [
    // Plugin for aspect ratio
    require('@tailwindcss/aspect-ratio'),

    // Plugin for forms
    require('@tailwindcss/forms'),

    // Plugin for typography
    require('@tailwindcss/typography'),

    // Plugin for container queries (future)
    function({ addUtilities, theme }) {
      const newUtilities = {
        '.container-responsive': {
          width: '100%',
          marginLeft: 'auto',
          marginRight: 'auto',
          paddingLeft: theme('spacing.4'),
          paddingRight: theme('spacing.4'),
          '@screen sm': {
            paddingLeft: theme('spacing.6'),
            paddingRight: theme('spacing.6')
          },
          '@screen lg': {
            paddingLeft: theme('spacing.8'),
            paddingRight: theme('spacing.8')
          }
        }
      }
      addUtilities(newUtilities)
    },

    // Plugin for focus-visible
    function({ addUtilities }) {
      const newUtilities = {
        '.focus-visible:focus-visible': {
          outline: '2px solid transparent',
          outlineOffset: '2px',
          '--tw-ring-offset-shadow': 'var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color)',
          '--tw-ring-shadow': 'var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)',
          boxShadow: 'var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000)',
          '--tw-ring-color': 'rgb(59 130 246 / 0.5)',
          '--tw-ring-offset-color': '#fff'
        },
        '.dark .focus-visible:focus-visible': {
          '--tw-ring-offset-color': '#111827'
        }
      }
      addUtilities(newUtilities)
    }
  ]
}