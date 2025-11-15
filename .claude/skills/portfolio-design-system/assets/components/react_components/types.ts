// Portfolio Design System - Common Types

export type ColorVariant =
  | 'primary'
  | 'secondary'
  | 'success'
  | 'warning'
  | 'error'
  | 'info'
  | 'neutral';

export type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export type SpacingSize = number | string;

export type Responsive<T> = {
  xs?: T;
  sm?: T;
  md?: T;
  lg?: T;
  xl?: T;
  '2xl'?: T;
};

export type Theme = 'light' | 'dark' | 'auto';

export type AnimationDuration = 'fast' | 'normal' | 'slow';

export type AnimationEasing =
  | 'ease-in'
  | 'ease-out'
  | 'ease-in-out'
  | 'linear';