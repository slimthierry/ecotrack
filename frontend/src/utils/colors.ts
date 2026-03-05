/**
 * EcoTrack green eco theme color palette.
 */

export const colors = {
  primary: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16",
  },
  secondary: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22",
  },
  accent: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49",
  },
  status: {
    success: "#22c55e",
    warning: "#f59e0b",
    error: "#ef4444",
    info: "#3b82f6",
  },
  category: {
    transport: "#3b82f6",  // blue-500
    food: "#f97316",       // orange-500
    energy: "#eab308",     // yellow-500
    purchase: "#8b5cf6",   // violet-500
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a",
  },
} as const;

export type CategoryColor = keyof typeof colors.category;

/**
 * Get the color for an activity category.
 */
export function getCategoryColor(category: string): string {
  return (
    colors.category[category as CategoryColor] ?? colors.neutral[500]
  );
}

/**
 * Get the color for a carbon level.
 */
export function getLevelColor(level: "low" | "medium" | "high"): string {
  switch (level) {
    case "low":
      return colors.status.success;
    case "medium":
      return colors.status.warning;
    case "high":
      return colors.status.error;
  }
}
