import React from "react";
import type { CategoryBreakdown as CategoryBreakdownType } from "@ecotrack/types";
import { formatCarbon, getCategoryColor } from "@ecotrack/utils";

export interface CategoryBreakdownProps {
  breakdown: CategoryBreakdownType;
  title?: string;
}

interface CategoryRow {
  name: string;
  key: string;
  percent: number;
  kg: number;
}

/**
 * Shows percentage breakdown by category with colored bars.
 */
export function CategoryBreakdown({
  breakdown,
  title = "Category Breakdown",
}: CategoryBreakdownProps) {
  const categories: CategoryRow[] = [
    {
      name: "Transport",
      key: "transport",
      percent: breakdown.transport_percent,
      kg: breakdown.transport_kg,
    },
    {
      name: "Food",
      key: "food",
      percent: breakdown.food_percent,
      kg: breakdown.food_kg,
    },
    {
      name: "Energy",
      key: "energy",
      percent: breakdown.energy_percent,
      kg: breakdown.energy_kg,
    },
    {
      name: "Purchase",
      key: "purchase",
      percent: breakdown.purchase_percent,
      kg: breakdown.purchase_kg,
    },
  ];

  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        borderRadius: "12px",
        padding: "20px",
        border: "1px solid #e5e5e5",
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
      }}
    >
      <h3
        style={{
          fontSize: "16px",
          fontWeight: 700,
          color: "#171717",
          margin: "0 0 16px 0",
        }}
      >
        {title}
      </h3>

      <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
        {categories.map((cat) => {
          const color = getCategoryColor(cat.key);
          return (
            <div key={cat.key}>
              {/* Label row */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "4px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <div
                    style={{
                      width: "10px",
                      height: "10px",
                      borderRadius: "50%",
                      backgroundColor: color,
                    }}
                  />
                  <span
                    style={{
                      fontSize: "13px",
                      fontWeight: 600,
                      color: "#404040",
                    }}
                  >
                    {cat.name}
                  </span>
                </div>
                <div style={{ display: "flex", gap: "12px", alignItems: "baseline" }}>
                  <span style={{ fontSize: "13px", color: "#737373" }}>
                    {formatCarbon(cat.kg)}
                  </span>
                  <span
                    style={{
                      fontSize: "14px",
                      fontWeight: 700,
                      color: "#171717",
                      minWidth: "48px",
                      textAlign: "right",
                    }}
                  >
                    {cat.percent.toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Bar */}
              <div
                style={{
                  width: "100%",
                  height: "8px",
                  backgroundColor: "#f5f5f5",
                  borderRadius: "4px",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${Math.min(cat.percent, 100)}%`,
                    height: "100%",
                    backgroundColor: color,
                    borderRadius: "4px",
                    transition: "width 0.3s ease",
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
