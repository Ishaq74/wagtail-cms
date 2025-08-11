/**
 * EXTRAORDINARY Design System Tailwind Configuration
 * 
 * This configuration implements a comprehensive design system with:
 * - Design tokens for consistency
 * - Component-based architecture
 * - Responsive design patterns
 * - Theme variations
 * - Accessibility features
 */

const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
    content: [
        // Template files
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        
        // Python files for classes in code
        '../../**/*.py',
        
        // JavaScript files
        '../../**/static/**/*.js',
    ],
    
    darkMode: 'class', // Enable dark mode with class strategy
    
    theme: {
        extend: {
            // Design System Color Tokens
            colors: {
                // Primary brand colors
                primary: {
                    50: 'rgb(var(--color-primary-50) / <alpha-value>)',
                    100: 'rgb(var(--color-primary-100) / <alpha-value>)',
                    200: 'rgb(var(--color-primary-200) / <alpha-value>)',
                    300: 'rgb(var(--color-primary-300) / <alpha-value>)',
                    400: 'rgb(var(--color-primary-400) / <alpha-value>)',
                    500: 'rgb(var(--color-primary-500) / <alpha-value>)',
                    600: 'rgb(var(--color-primary-600) / <alpha-value>)',
                    700: 'rgb(var(--color-primary-700) / <alpha-value>)',
                    800: 'rgb(var(--color-primary-800) / <alpha-value>)',
                    900: 'rgb(var(--color-primary-900) / <alpha-value>)',
                    950: 'rgb(var(--color-primary-950) / <alpha-value>)',
                    DEFAULT: 'rgb(var(--color-primary-600) / <alpha-value>)',
                },
                
                // Secondary brand colors
                secondary: {
                    50: 'rgb(var(--color-secondary-50) / <alpha-value>)',
                    100: 'rgb(var(--color-secondary-100) / <alpha-value>)',
                    200: 'rgb(var(--color-secondary-200) / <alpha-value>)',
                    300: 'rgb(var(--color-secondary-300) / <alpha-value>)',
                    400: 'rgb(var(--color-secondary-400) / <alpha-value>)',
                    500: 'rgb(var(--color-secondary-500) / <alpha-value>)',
                    600: 'rgb(var(--color-secondary-600) / <alpha-value>)',
                    700: 'rgb(var(--color-secondary-700) / <alpha-value>)',
                    800: 'rgb(var(--color-secondary-800) / <alpha-value>)',
                    900: 'rgb(var(--color-secondary-900) / <alpha-value>)',
                    950: 'rgb(var(--color-secondary-950) / <alpha-value>)',
                    DEFAULT: 'rgb(var(--color-secondary-600) / <alpha-value>)',
                },
                
                // Accent colors
                accent: {
                    50: 'rgb(var(--color-accent-50) / <alpha-value>)',
                    100: 'rgb(var(--color-accent-100) / <alpha-value>)',
                    200: 'rgb(var(--color-accent-200) / <alpha-value>)',
                    300: 'rgb(var(--color-accent-300) / <alpha-value>)',
                    400: 'rgb(var(--color-accent-400) / <alpha-value>)',
                    500: 'rgb(var(--color-accent-500) / <alpha-value>)',
                    600: 'rgb(var(--color-accent-600) / <alpha-value>)',
                    700: 'rgb(var(--color-accent-700) / <alpha-value>)',
                    800: 'rgb(var(--color-accent-800) / <alpha-value>)',
                    900: 'rgb(var(--color-accent-900) / <alpha-value>)',
                    950: 'rgb(var(--color-accent-950) / <alpha-value>)',
                    DEFAULT: 'rgb(var(--color-accent-500) / <alpha-value>)',
                },
                
                // Neutral colors
                neutral: {
                    50: 'rgb(var(--color-neutral-50) / <alpha-value>)',
                    100: 'rgb(var(--color-neutral-100) / <alpha-value>)',
                    200: 'rgb(var(--color-neutral-200) / <alpha-value>)',
                    300: 'rgb(var(--color-neutral-300) / <alpha-value>)',
                    400: 'rgb(var(--color-neutral-400) / <alpha-value>)',
                    500: 'rgb(var(--color-neutral-500) / <alpha-value>)',
                    600: 'rgb(var(--color-neutral-600) / <alpha-value>)',
                    700: 'rgb(var(--color-neutral-700) / <alpha-value>)',
                    800: 'rgb(var(--color-neutral-800) / <alpha-value>)',
                    900: 'rgb(var(--color-neutral-900) / <alpha-value>)',
                    950: 'rgb(var(--color-neutral-950) / <alpha-value>)',
                    DEFAULT: 'rgb(var(--color-neutral-700) / <alpha-value>)',
                },
                
                // Base colors for text and backgrounds
                base: {
                    50: 'rgb(var(--color-base-50) / <alpha-value>)',
                    100: 'rgb(var(--color-base-100) / <alpha-value>)',
                    200: 'rgb(var(--color-base-200) / <alpha-value>)',
                    300: 'rgb(var(--color-base-300) / <alpha-value>)',
                    400: 'rgb(var(--color-base-400) / <alpha-value>)',
                    500: 'rgb(var(--color-base-500) / <alpha-value>)',
                    600: 'rgb(var(--color-base-600) / <alpha-value>)',
                    700: 'rgb(var(--color-base-700) / <alpha-value>)',
                    800: 'rgb(var(--color-base-800) / <alpha-value>)',
                    900: 'rgb(var(--color-base-900) / <alpha-value>)',
                    950: 'rgb(var(--color-base-950) / <alpha-value>)',
                    DEFAULT: 'rgb(var(--color-base-800) / <alpha-value>)',
                },
                
                // Semantic colors
                success: {
                    50: 'rgb(240 253 244 / <alpha-value>)',
                    100: 'rgb(220 252 231 / <alpha-value>)',
                    500: 'rgb(34 197 94 / <alpha-value>)',
                    600: 'rgb(22 163 74 / <alpha-value>)',
                    DEFAULT: 'rgb(22 163 74 / <alpha-value>)',
                },
                warning: {
                    50: 'rgb(255 251 235 / <alpha-value>)',
                    100: 'rgb(254 243 199 / <alpha-value>)',
                    500: 'rgb(245 158 11 / <alpha-value>)',
                    600: 'rgb(217 119 6 / <alpha-value>)',
                    DEFAULT: 'rgb(217 119 6 / <alpha-value>)',
                },
                error: {
                    50: 'rgb(254 242 242 / <alpha-value>)',
                    100: 'rgb(254 226 226 / <alpha-value>)',
                    500: 'rgb(239 68 68 / <alpha-value>)',
                    600: 'rgb(220 38 38 / <alpha-value>)',
                    DEFAULT: 'rgb(220 38 38 / <alpha-value>)',
                },
                info: {
                    50: 'rgb(239 246 255 / <alpha-value>)',
                    100: 'rgb(219 234 254 / <alpha-value>)',
                    500: 'rgb(59 130 246 / <alpha-value>)',
                    600: 'rgb(37 99 235 / <alpha-value>)',
                    DEFAULT: 'rgb(37 99 235 / <alpha-value>)',
                },
            },
            
            // Typography Scale
            fontFamily: {
                sans: ['var(--font-family-sans)', ...defaultTheme.fontFamily.sans],
                serif: ['var(--font-family-serif)', ...defaultTheme.fontFamily.serif],
                mono: ['var(--font-family-mono)', ...defaultTheme.fontFamily.mono],
            },
            
            fontSize: {
                'xs': ['0.75rem', { lineHeight: '1rem' }],
                'sm': ['0.875rem', { lineHeight: '1.25rem' }],
                'base': ['1rem', { lineHeight: '1.5rem' }],
                'lg': ['1.125rem', { lineHeight: '1.75rem' }],
                'xl': ['1.25rem', { lineHeight: '1.75rem' }],
                '2xl': ['1.5rem', { lineHeight: '2rem' }],
                '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
                '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
                '5xl': ['3rem', { lineHeight: '1.2' }],
                '6xl': ['3.75rem', { lineHeight: '1.1' }],
                '7xl': ['4.5rem', { lineHeight: '1.1' }],
                '8xl': ['6rem', { lineHeight: '1' }],
                '9xl': ['8rem', { lineHeight: '1' }],
            },
            
            // Spacing Scale
            spacing: {
                '18': '4.5rem',
                '88': '22rem',
                '128': '32rem',
                '144': '36rem',
            },
            
            // Border Radius
            borderRadius: {
                'xs': '0.125rem',
                'sm': '0.25rem',
                'md': '0.375rem',
                'lg': '0.5rem',
                'xl': '0.75rem',
                '2xl': '1rem',
                '3xl': '1.5rem',
            },
            
            // Shadows
            boxShadow: {
                'xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
                'sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
                'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
                'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
                'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
                '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
                'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
                'glow': '0 0 20px rgb(var(--color-primary-500) / 0.5)',
                'glow-lg': '0 0 40px rgb(var(--color-primary-500) / 0.3)',
            },
            
            // Animation and Transitions
            animation: {
                'fade-in': 'fadeIn 0.5s ease-in-out',
                'fade-in-up': 'fadeInUp 0.6s ease-out',
                'fade-in-down': 'fadeInDown 0.6s ease-out',
                'slide-in-left': 'slideInLeft 0.5s ease-out',
                'slide-in-right': 'slideInRight 0.5s ease-out',
                'zoom-in': 'zoomIn 0.5s ease-out',
                'bounce-in': 'bounceIn 0.8s ease-out',
                'pulse-slow': 'pulse 3s ease-in-out infinite',
            },
            
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(30px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                fadeInDown: {
                    '0%': { opacity: '0', transform: 'translateY(-30px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideInLeft: {
                    '0%': { opacity: '0', transform: 'translateX(-30px)' },
                    '100%': { opacity: '1', transform: 'translateX(0)' },
                },
                slideInRight: {
                    '0%': { opacity: '0', transform: 'translateX(30px)' },
                    '100%': { opacity: '1', transform: 'translateX(0)' },
                },
                zoomIn: {
                    '0%': { opacity: '0', transform: 'scale(0.95)' },
                    '100%': { opacity: '1', transform: 'scale(1)' },
                },
                bounceIn: {
                    '0%': { opacity: '0', transform: 'scale(0.3)' },
                    '50%': { opacity: '1', transform: 'scale(1.05)' },
                    '70%': { transform: 'scale(0.9)' },
                    '100%': { opacity: '1', transform: 'scale(1)' },
                },
            },
            
            // Grid and Layout
            gridTemplateColumns: {
                '16': 'repeat(16, minmax(0, 1fr))',
                '20': 'repeat(20, minmax(0, 1fr))',
            },
            
            // Aspect Ratios
            aspectRatio: {
                'square': '1 / 1',
                'landscape': '4 / 3',
                'portrait': '3 / 4',
                'wide': '16 / 9',
                'ultra-wide': '21 / 9',
                'golden': '1.618 / 1',
            },
            
            // Container Sizes
            maxWidth: {
                'xs': '20rem',      // 320px
                'sm': '24rem',      // 384px
                'md': '28rem',      // 448px
                'lg': '32rem',      // 512px
                'xl': '36rem',      // 576px
                '2xl': '42rem',     // 672px
                '3xl': '48rem',     // 768px
                '4xl': '56rem',     // 896px
                '5xl': '64rem',     // 1024px
                '6xl': '72rem',     // 1152px
                '7xl': '80rem',     // 1280px
                'screen-sm': '640px',
                'screen-md': '768px',
                'screen-lg': '1024px',
                'screen-xl': '1280px',
                'screen-2xl': '1536px',
            },
            
            // Z-index scale
            zIndex: {
                'dropdown': '1000',
                'sticky': '1020',
                'fixed': '1030',
                'modal-backdrop': '1040',
                'modal': '1050',
                'popover': '1060',
                'tooltip': '1070',
            },
        },
    },
    
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        
        // Custom plugin for component classes
        function({ addComponents, addUtilities, theme }) {
            addComponents({
                // Button Components
                '.btn': {
                    '@apply inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium rounded-md border border-transparent transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2': {},
                },
                '.btn-xs': { '@apply px-2 py-1 text-xs': {} },
                '.btn-sm': { '@apply px-3 py-1.5 text-sm': {} },
                '.btn-md': { '@apply px-4 py-2 text-sm': {} },
                '.btn-lg': { '@apply px-6 py-3 text-base': {} },
                '.btn-xl': { '@apply px-8 py-4 text-lg': {} },
                
                '.btn-primary': {
                    '@apply bg-primary text-white hover:bg-primary-700 focus:ring-primary/50': {},
                },
                '.btn-secondary': {
                    '@apply bg-secondary text-white hover:bg-secondary-700 focus:ring-secondary/50': {},
                },
                '.btn-accent': {
                    '@apply bg-accent text-white hover:bg-accent-600 focus:ring-accent/50': {},
                },
                '.btn-outline': {
                    '@apply border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary/50': {},
                },
                '.btn-ghost': {
                    '@apply text-primary hover:bg-primary/10 focus:ring-primary/50': {},
                },
                '.btn-link': {
                    '@apply text-primary underline hover:text-primary-700 focus:ring-primary/50': {},
                },
                '.btn-full': {
                    '@apply w-full': {},
                },
                
                // Card Components
                '.card': {
                    '@apply bg-white dark:bg-neutral-800 rounded-lg shadow-md border border-neutral-200 dark:border-neutral-700': {},
                },
                '.card-body': {
                    '@apply p-6': {},
                },
                '.card-header': {
                    '@apply px-6 py-4 border-b border-neutral-200 dark:border-neutral-700': {},
                },
                '.card-footer': {
                    '@apply px-6 py-4 border-t border-neutral-200 dark:border-neutral-700': {},
                },
                
                // Typography Components
                '.heading-xs': { '@apply text-sm font-semibold': {} },
                '.heading-sm': { '@apply text-base font-semibold': {} },
                '.heading-base': { '@apply text-lg font-semibold': {} },
                '.heading-lg': { '@apply text-xl font-bold': {} },
                '.heading-xl': { '@apply text-2xl font-bold': {} },
                '.heading-2xl': { '@apply text-3xl font-bold': {} },
                '.heading-3xl': { '@apply text-4xl font-bold': {} },
                '.heading-4xl': { '@apply text-5xl font-bold': {} },
                '.heading-5xl': { '@apply text-6xl font-bold': {} },
                '.heading-6xl': { '@apply text-7xl font-bold': {} },
                
                '.lead': {
                    '@apply text-lg text-neutral-600 dark:text-neutral-300': {},
                },
                
                // Layout Components
                '.container-xs': { '@apply max-w-xs mx-auto px-4': {} },
                '.container-sm': { '@apply max-w-sm mx-auto px-4': {} },
                '.container-md': { '@apply max-w-md mx-auto px-4': {} },
                '.container-lg': { '@apply max-w-lg mx-auto px-4': {} },
                '.container-xl': { '@apply max-w-xl mx-auto px-4': {} },
                '.container-2xl': { '@apply max-w-2xl mx-auto px-4': {} },
                '.container-3xl': { '@apply max-w-3xl mx-auto px-4': {} },
                '.container-4xl': { '@apply max-w-4xl mx-auto px-4': {} },
                '.container-5xl': { '@apply max-w-5xl mx-auto px-4': {} },
                '.container-6xl': { '@apply max-w-6xl mx-auto px-4': {} },
                '.container-7xl': { '@apply max-w-7xl mx-auto px-4': {} },
                '.container-full': { '@apply w-full px-4': {} },
                
                // Grid Components
                '.grid-cols-auto': {
                    'grid-template-columns': 'repeat(auto-fit, minmax(280px, 1fr))',
                },
                '.grid-cols-auto-sm': {
                    'grid-template-columns': 'repeat(auto-fit, minmax(200px, 1fr))',
                },
                '.grid-cols-auto-lg': {
                    'grid-template-columns': 'repeat(auto-fit, minmax(320px, 1fr))',
                },
            });
            
            addUtilities({
                // Animation Utilities
                '.animate-delay-100': { 'animation-delay': '100ms' },
                '.animate-delay-200': { 'animation-delay': '200ms' },
                '.animate-delay-300': { 'animation-delay': '300ms' },
                '.animate-delay-500': { 'animation-delay': '500ms' },
                '.animate-delay-750': { 'animation-delay': '750ms' },
                '.animate-delay-1000': { 'animation-delay': '1000ms' },
                
                // Spacing Utilities
                '.spacing-none': { '@apply mb-0': {} },
                '.spacing-xs': { '@apply mb-2': {} },
                '.spacing-sm': { '@apply mb-4': {} },
                '.spacing-md': { '@apply mb-6': {} },
                '.spacing-lg': { '@apply mb-8': {} },
                '.spacing-xl': { '@apply mb-12': {} },
                '.spacing-2xl': { '@apply mb-16': {} },
                
                // Aspect Ratio Utilities
                '.aspect-square': { 'aspect-ratio': '1 / 1' },
                '.aspect-landscape': { 'aspect-ratio': '4 / 3' },
                '.aspect-portrait': { 'aspect-ratio': '3 / 4' },
                '.aspect-wide': { 'aspect-ratio': '16 / 9' },
                '.aspect-ultra-wide': { 'aspect-ratio': '21 / 9' },
            });
        }
    ],
}