import type { BrandPalette, ThemeConfig } from './types';

export const brandPalette: BrandPalette = {
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
  950: '#052E16',
};

export const defaultConfig: ThemeConfig = {
  storageKey: 'ecotrack-theme',
  defaultMode: 'system',
  brand: brandPalette,
};
