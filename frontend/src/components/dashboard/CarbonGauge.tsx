import React from "react";

export interface CarbonGaugeProps {
  /** Eco score value between 0 and 100 */
  score: number;
  /** Diameter of the gauge in pixels */
  size?: number;
  /** Label shown below the score */
  label?: string;
}

/**
 * Circular gauge component showing an eco score from 0-100.
 * Uses SVG for the circular progress arc.
 */
export function CarbonGauge({
  score,
  size = 180,
  label = "Eco Score",
}: CarbonGaugeProps) {
  const clampedScore = Math.max(0, Math.min(100, score));
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (clampedScore / 100) * circumference;

  // Color based on score: red -> yellow -> green
  const getColor = (s: number): string => {
    if (s < 30) return "#ef4444";
    if (s < 60) return "#f59e0b";
    return "#22c55e";
  };

  const color = getColor(clampedScore);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "8px",
      }}
    >
      <div style={{ position: "relative", width: size, height: size }}>
        <svg
          width={size}
          height={size}
          style={{ transform: "rotate(-90deg)" }}
        >
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="#f5f5f5"
            strokeWidth={strokeWidth}
          />
          {/* Progress arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{
              transition: "stroke-dashoffset 0.6s ease, stroke 0.3s ease",
            }}
          />
        </svg>
        {/* Center text */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontSize: `${size * 0.22}px`,
              fontWeight: 800,
              color: color,
              lineHeight: 1,
            }}
          >
            {clampedScore}
          </div>
          <div
            style={{
              fontSize: `${size * 0.08}px`,
              color: "#737373",
              marginTop: "4px",
            }}
          >
            / 100
          </div>
        </div>
      </div>
      <div
        style={{
          fontSize: "14px",
          fontWeight: 600,
          color: "#404040",
        }}
      >
        {label}
      </div>
    </div>
  );
}
