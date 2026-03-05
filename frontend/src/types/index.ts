// ===== User Types =====

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserResponse {
  id: string;
  email: string;
  username: string;
  eco_score: number;
  total_carbon_saved: number;
  streak_days: number;
  created_at: string;
}

export interface UserProfile extends UserResponse {
  total_activities: number;
  active_challenges: number;
  achievements_unlocked: number;
  carbon_saved_this_week: number;
  carbon_saved_this_month: number;
}

// ===== Auth Types =====

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// ===== Activity Types =====

export type ActivityCategory = "transport" | "food" | "energy" | "purchase";

export interface ActivityCreate {
  category: ActivityCategory;
  sub_category: string;
  quantity: number;
  unit: string;
  date: string;
  notes?: string;
}

export interface ActivityResponse {
  id: string;
  user_id: string;
  category: ActivityCategory;
  sub_category: string;
  quantity: number;
  unit: string;
  carbon_kg: number;
  date: string;
  notes: string | null;
  created_at: string;
}

export interface ActivitySummary {
  total_carbon: number;
  activity_count: number;
  date_range_start: string;
  date_range_end: string;
}

export interface CarbonBreakdown {
  transport_percent: number;
  food_percent: number;
  energy_percent: number;
  purchase_percent: number;
  transport_kg: number;
  food_kg: number;
  energy_kg: number;
  purchase_kg: number;
  total_kg: number;
}

// ===== Challenge Types =====

export interface ChallengeResponse {
  id: string;
  title: string;
  description: string;
  category: string;
  target_carbon_reduction: number;
  duration_days: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
  participants_count: number;
  created_at: string;
}

export interface ChallengeJoin {
  challenge_id: string;
}

export interface ChallengeProgress {
  challenge_id: string;
  challenge_title: string;
  progress_percent: number;
  carbon_saved: number;
  completed: boolean;
  joined_at: string;
  days_remaining: number;
}

export interface LeaderboardEntry {
  username: string;
  carbon_saved: number;
  rank: number;
}

// ===== Achievement Types =====

export interface AchievementResponse {
  id: string;
  name: string;
  description: string;
  icon: string;
  criteria_type: string;
  criteria_value: number;
  created_at: string;
}

export interface UserAchievementResponse {
  id: string;
  achievement: AchievementResponse;
  unlocked_at: string;
}

// ===== Dashboard Types =====

export interface DashboardOverview {
  total_carbon_today: number;
  total_carbon_week: number;
  total_carbon_month: number;
  eco_score: number;
  streak_days: number;
  active_challenges: number;
  achievements_unlocked: number;
}

export interface DailyCarbon {
  date: string;
  carbon_kg: number;
}

export interface WeeklyTrend {
  days: DailyCarbon[];
  total_kg: number;
  average_daily_kg: number;
}

export interface CategoryBreakdown {
  transport_percent: number;
  food_percent: number;
  energy_percent: number;
  purchase_percent: number;
  transport_kg: number;
  food_kg: number;
  energy_kg: number;
  purchase_kg: number;
}

export interface EcoTip {
  title: string;
  description: string;
  category: string;
  potential_savings_kg: number;
}

// ===== Report Types =====

export interface WeeklyReport {
  user: {
    username: string;
    eco_score: number;
    streak_days: number;
  };
  period: {
    start: string;
    end: string;
  };
  summary: {
    total_carbon_kg: number;
    total_carbon_formatted: string;
    activity_count: number;
    daily_average_kg: number;
    trees_equivalent: number;
    driving_km_equivalent: number;
  };
  comparison: {
    previous_week_kg: number;
    change_percent: number;
    vs_average: {
      daily_carbon_kg: number;
      average_daily_kg: number;
      percentage_of_average: number;
      level: string;
      message: string;
    };
  };
  category_breakdown: Record<string, number>;
  daily_breakdown: DailyCarbon[];
}

export interface MonthlyReport {
  user: {
    username: string;
    eco_score: number;
    total_carbon_saved: number;
  };
  period: {
    start: string;
    end: string;
  };
  summary: {
    total_carbon_kg: number;
    total_carbon_formatted: string;
    activity_count: number;
    daily_average_kg: number;
    trees_equivalent: number;
    driving_km_equivalent: number;
  };
  comparison: {
    vs_average: {
      daily_carbon_kg: number;
      average_daily_kg: number;
      percentage_of_average: number;
      level: string;
      message: string;
    };
  };
  category_breakdown: Record<string, number>;
  weekly_breakdown: {
    week_start: string;
    week_end: string;
    carbon_kg: number;
  }[];
}

// ===== Utility Types =====

export type CarbonLevel = "low" | "medium" | "high";

export interface ApiError {
  detail: string;
}
