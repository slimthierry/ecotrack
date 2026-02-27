from pydantic import BaseModel


class DashboardOverview(BaseModel):
    total_carbon_today: float = 0.0
    total_carbon_week: float = 0.0
    total_carbon_month: float = 0.0
    eco_score: int = 0
    streak_days: int = 0
    active_challenges: int = 0
    achievements_unlocked: int = 0


class DailyCarbon(BaseModel):
    date: str
    carbon_kg: float


class WeeklyTrend(BaseModel):
    days: list[DailyCarbon] = []
    total_kg: float = 0.0
    average_daily_kg: float = 0.0


class CategoryBreakdown(BaseModel):
    transport_percent: float = 0.0
    food_percent: float = 0.0
    energy_percent: float = 0.0
    purchase_percent: float = 0.0
    transport_kg: float = 0.0
    food_kg: float = 0.0
    energy_kg: float = 0.0
    purchase_kg: float = 0.0


class EcoTip(BaseModel):
    title: str
    description: str
    category: str
    potential_savings_kg: float
