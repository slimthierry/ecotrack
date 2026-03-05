import React from "react";
import type { ActivityResponse } from "@ecotrack/types";
import { formatCarbon, getCategoryColor } from "@ecotrack/utils";

export interface ActivityCardProps {
  activity: ActivityResponse;
  onDelete?: (id: string) => void;
}

const categoryIcons: Record<string, string> = {
  transport: "🚗",
  food: "🍽️",
  energy: "⚡",
  purchase: "🛒",
};

export function ActivityCard({ activity, onDelete }: ActivityCardProps) {
  const icon = categoryIcons[activity.category] ?? "📊";
  const categoryColor = getCategoryColor(activity.category);

  return (
    <div
      style={{
        border: "1px solid #e5e5e5",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "12px",
        backgroundColor: "#ffffff",
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            style={{
              fontSize: "24px",
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: `${categoryColor}15`,
            }}
          >
            {icon}
          </div>
          <div>
            <div
              style={{
                fontSize: "14px",
                fontWeight: 600,
                color: "#171717",
                textTransform: "capitalize",
              }}
            >
              {activity.sub_category.replace(/_/g, " ")}
            </div>
            <div
              style={{
                fontSize: "12px",
                color: "#737373",
                marginTop: "2px",
              }}
            >
              {activity.quantity} {activity.unit} &middot;{" "}
              <span style={{ color: categoryColor, textTransform: "capitalize" }}>
                {activity.category}
              </span>
            </div>
          </div>
        </div>

        <div style={{ textAlign: "right" }}>
          <div
            style={{
              fontSize: "16px",
              fontWeight: 700,
              color: "#166534",
            }}
          >
            {formatCarbon(activity.carbon_kg)}
          </div>
          <div style={{ fontSize: "11px", color: "#a3a3a3", marginTop: "2px" }}>
            {new Date(activity.date).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
            })}
          </div>
        </div>
      </div>

      {activity.notes && (
        <div
          style={{
            marginTop: "10px",
            fontSize: "13px",
            color: "#525252",
            fontStyle: "italic",
            paddingLeft: "60px",
          }}
        >
          {activity.notes}
        </div>
      )}

      {onDelete && (
        <div style={{ marginTop: "10px", textAlign: "right" }}>
          <button
            onClick={() => onDelete(activity.id)}
            style={{
              fontSize: "12px",
              color: "#ef4444",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "4px 8px",
            }}
          >
            Delete
          </button>
        </div>
      )}
    </div>
  );
}
