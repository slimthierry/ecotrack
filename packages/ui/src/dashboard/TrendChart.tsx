import React from "react";
import type { DailyCarbon } from "@ecotrack/types";
import { formatCarbon } from "@ecotrack/utils";

export interface TrendChartProps {
  /** Array of daily carbon data */
  days: DailyCarbon[];
  /** Height of the chart in pixels */
  height?: number;
  /** Color of the bars */
  barColor?: string;
  /** Title displayed above the chart */
  title?: string;
}

/**
 * Simple bar chart showing weekly carbon trend.
 * Renders using plain HTML/CSS for zero dependencies.
 */
export function TrendChart({
  days,
  height = 200,
  barColor = "#22c55e",
  title = "Weekly Carbon Trend",
}: TrendChartProps) {
  const maxCarbon = Math.max(...days.map((d) => d.carbon_kg), 0.1);

  const dayLabels = days.map((d) => {
    const date = new Date(d.date);
    return date.toLocaleDateString("en-US", { weekday: "short" });
  });

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

      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-between",
          height: `${height}px`,
          gap: "8px",
          padding: "0 4px",
        }}
      >
        {days.map((day, index) => {
          const barHeight =
            maxCarbon > 0
              ? Math.max((day.carbon_kg / maxCarbon) * (height - 40), 4)
              : 4;

          return (
            <div
              key={day.date}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                flex: 1,
                gap: "6px",
              }}
            >
              {/* Carbon value label */}
              <div
                style={{
                  fontSize: "10px",
                  color: "#737373",
                  whiteSpace: "nowrap",
                }}
              >
                {day.carbon_kg > 0 ? formatCarbon(day.carbon_kg) : "-"}
              </div>

              {/* Bar */}
              <div
                style={{
                  width: "100%",
                  maxWidth: "40px",
                  height: `${barHeight}px`,
                  backgroundColor: barColor,
                  borderRadius: "4px 4px 0 0",
                  transition: "height 0.3s ease",
                  opacity: day.carbon_kg > 0 ? 1 : 0.3,
                }}
              />

              {/* Day label */}
              <div
                style={{
                  fontSize: "11px",
                  color: "#525252",
                  fontWeight: 500,
                }}
              >
                {dayLabels[index]}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
