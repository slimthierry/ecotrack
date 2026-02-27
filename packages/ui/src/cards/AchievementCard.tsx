import React from "react";
import type { AchievementResponse } from "@ecotrack/types";

export interface AchievementCardProps {
  achievement: AchievementResponse;
  unlocked: boolean;
  unlockedAt?: string;
}

const iconMap: Record<string, string> = {
  leaf: "🌿",
  star: "⭐",
  trophy: "🏆",
  medal: "🏅",
  fire: "🔥",
  crown: "👑",
  clipboard: "📋",
  globe: "🌍",
  flag: "🚩",
  shield: "🛡️",
};

export function AchievementCard({
  achievement,
  unlocked,
  unlockedAt,
}: AchievementCardProps) {
  const icon = iconMap[achievement.icon] ?? "🎯";

  return (
    <div
      style={{
        border: "1px solid #e5e5e5",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "12px",
        backgroundColor: unlocked ? "#ffffff" : "#fafafa",
        boxShadow: unlocked ? "0 1px 3px rgba(0, 0, 0, 0.1)" : "none",
        opacity: unlocked ? 1 : 0.6,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Unlocked shimmer effect */}
      {unlocked && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: "3px",
            background: "linear-gradient(90deg, #22c55e, #10b981, #059669)",
          }}
        />
      )}

      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        <div
          style={{
            fontSize: "32px",
            width: "56px",
            height: "56px",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: unlocked ? "#f0fdf4" : "#f5f5f5",
            border: unlocked ? "2px solid #22c55e" : "2px solid #d4d4d4",
            filter: unlocked ? "none" : "grayscale(100%)",
          }}
        >
          {icon}
        </div>

        <div style={{ flex: 1 }}>
          <div
            style={{
              fontSize: "15px",
              fontWeight: 700,
              color: unlocked ? "#171717" : "#a3a3a3",
            }}
          >
            {achievement.name}
          </div>
          <div
            style={{
              fontSize: "13px",
              color: unlocked ? "#525252" : "#a3a3a3",
              marginTop: "2px",
              lineHeight: "1.4",
            }}
          >
            {achievement.description}
          </div>
          {unlocked && unlockedAt && (
            <div
              style={{
                fontSize: "11px",
                color: "#22c55e",
                marginTop: "4px",
                fontWeight: 600,
              }}
            >
              Unlocked{" "}
              {new Date(unlockedAt).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                year: "numeric",
              })}
            </div>
          )}
          {!unlocked && (
            <div
              style={{
                fontSize: "11px",
                color: "#a3a3a3",
                marginTop: "4px",
              }}
            >
              Locked
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
