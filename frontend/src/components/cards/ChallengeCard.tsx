import React from "react";
import type { ChallengeResponse } from "@ecotrack/types";
import { formatCarbon, getCategoryColor } from "@ecotrack/utils";

export interface ChallengeCardProps {
  challenge: ChallengeResponse;
  onJoin?: (challengeId: string) => void;
  isJoined?: boolean;
  progressPercent?: number;
}

export function ChallengeCard({
  challenge,
  onJoin,
  isJoined = false,
  progressPercent = 0,
}: ChallengeCardProps) {
  const categoryColor = getCategoryColor(challenge.category);
  const daysLeft = Math.max(
    0,
    Math.ceil(
      (new Date(challenge.end_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
    )
  );

  return (
    <div
      style={{
        border: "1px solid #e5e5e5",
        borderRadius: "12px",
        padding: "20px",
        marginBottom: "12px",
        backgroundColor: "#ffffff",
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
        borderLeft: `4px solid ${categoryColor}`,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "12px",
        }}
      >
        <div>
          <h3
            style={{
              fontSize: "16px",
              fontWeight: 700,
              color: "#171717",
              margin: 0,
            }}
          >
            {challenge.title}
          </h3>
          <p
            style={{
              fontSize: "13px",
              color: "#525252",
              margin: "4px 0 0 0",
              lineHeight: "1.4",
            }}
          >
            {challenge.description}
          </p>
        </div>
        <span
          style={{
            fontSize: "11px",
            padding: "2px 8px",
            borderRadius: "9999px",
            backgroundColor: `${categoryColor}15`,
            color: categoryColor,
            fontWeight: 600,
            textTransform: "capitalize",
            whiteSpace: "nowrap",
          }}
        >
          {challenge.category}
        </span>
      </div>

      {/* Progress bar */}
      <div style={{ marginBottom: "12px" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "12px",
            color: "#737373",
            marginBottom: "4px",
          }}
        >
          <span>Progress</span>
          <span>{progressPercent.toFixed(1)}%</span>
        </div>
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
              width: `${Math.min(progressPercent, 100)}%`,
              height: "100%",
              backgroundColor: progressPercent >= 100 ? "#22c55e" : categoryColor,
              borderRadius: "4px",
              transition: "width 0.3s ease",
            }}
          />
        </div>
      </div>

      {/* Info row */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: "12px",
          color: "#737373",
        }}
      >
        <div style={{ display: "flex", gap: "16px" }}>
          <span>
            Target: {formatCarbon(challenge.target_carbon_reduction)}
          </span>
          <span>{challenge.participants_count} participants</span>
          <span>{daysLeft} days left</span>
        </div>

        {onJoin && !isJoined && (
          <button
            onClick={() => onJoin(challenge.id)}
            style={{
              fontSize: "13px",
              fontWeight: 600,
              color: "#ffffff",
              backgroundColor: "#22c55e",
              border: "none",
              borderRadius: "6px",
              padding: "6px 16px",
              cursor: "pointer",
            }}
          >
            Join
          </button>
        )}
        {isJoined && (
          <span
            style={{
              fontSize: "13px",
              fontWeight: 600,
              color: "#22c55e",
            }}
          >
            Joined
          </span>
        )}
      </div>
    </div>
  );
}
