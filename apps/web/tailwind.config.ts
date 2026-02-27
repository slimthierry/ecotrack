import type { Config } from 'tailwindcss';

export default {
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
    '../../packages/ui/src/**/*.{ts,tsx}',
    '../../packages/theme/src/**/*.{ts,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#F0FDF4',
          100: '#DCFCE7',
          200: '#BBF7D0',
          300: '#86EFAC',
          400: '#4ADE80',
          500: '#22C55E',
          600: '#16A34A',
          700: '#15803D',
          800: '#166534',
          900: '#14532D',
        },
        surface: {
          primary: 'rgb(var(--theme-bg-primary) / <alpha-value>)',
          secondary: 'rgb(var(--theme-bg-secondary) / <alpha-value>)',
          tertiary: 'rgb(var(--theme-bg-tertiary) / <alpha-value>)',
        },
        content: {
          primary: 'rgb(var(--theme-text-primary) / <alpha-value>)',
          secondary: 'rgb(var(--theme-text-secondary) / <alpha-value>)',
          tertiary: 'rgb(var(--theme-text-tertiary) / <alpha-value>)',
          inverted: 'rgb(var(--theme-text-inverted) / <alpha-value>)',
        },
        edge: {
          primary: 'rgb(var(--theme-border-primary) / <alpha-value>)',
          secondary: 'rgb(var(--theme-border-secondary) / <alpha-value>)',
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
