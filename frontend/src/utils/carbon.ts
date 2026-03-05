import type { CarbonLevel } from "@ecotrack/types";

/**
 * One mature tree absorbs approximately 22 kg CO2 per year.
 */
const TREE_ANNUAL_ABSORPTION_KG = 22.0;

/**
 * Average car emits about 0.21 kg CO2 per km.
 */
const CAR_EMISSION_PER_KM = 0.21;

/**
 * Format a carbon amount with appropriate unit (g, kg, or tonnes).
 */
export function formatCarbon(carbonKg: number): string {
  if (carbonKg < 0.001) {
    return "0 g CO2";
  } else if (carbonKg < 1.0) {
    return `${(carbonKg * 1000).toFixed(0)} g CO2`;
  } else if (carbonKg < 1000.0) {
    return `${carbonKg.toFixed(2)} kg CO2`;
  } else {
    return `${(carbonKg / 1000).toFixed(2)} tonnes CO2`;
  }
}

/**
 * Convert kg of CO2 to the number of trees needed to absorb
 * that amount in one year.
 */
export function kgToTrees(carbonKg: number): number {
  if (carbonKg <= 0) return 0;
  return Math.round((carbonKg / TREE_ANNUAL_ABSORPTION_KG) * 100) / 100;
}

/**
 * Convert kg of CO2 to equivalent driving distance in km.
 */
export function kgToDrivingKm(carbonKg: number): number {
  if (carbonKg <= 0) return 0;
  return Math.round((carbonKg / CAR_EMISSION_PER_KM) * 10) / 10;
}

/**
 * Get the carbon level classification based on daily kg CO2.
 * - low: under 5 kg/day (well below global average)
 * - medium: 5-15 kg/day (around global average)
 * - high: over 15 kg/day (above global average)
 */
export function getCarbonLevel(dailyKg: number): CarbonLevel {
  if (dailyKg < 5) return "low";
  if (dailyKg < 15) return "medium";
  return "high";
}

/**
 * Get the color associated with a carbon level.
 */
export function getCarbonLevelColor(level: CarbonLevel): string {
  switch (level) {
    case "low":
      return "#22c55e"; // green-500
    case "medium":
      return "#f59e0b"; // amber-500
    case "high":
      return "#ef4444"; // red-500
  }
}

/**
 * Calculate percentage change between two values.
 */
export function percentageChange(current: number, previous: number): number {
  if (previous === 0) return 0;
  return Math.round(((current - previous) / previous) * 1000) / 10;
}
