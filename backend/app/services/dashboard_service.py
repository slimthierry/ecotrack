from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_models import Activity
from app.models.achievement_models import UserAchievement
from app.models.challenge_models import UserChallenge
from app.models.user_models import User
from app.schemas.dashboard_schemas import (
    CategoryBreakdown,
    DailyCarbon,
    DashboardOverview,
    EcoTip,
    WeeklyTrend,
)
from app.utils.eco_tips import get_random_tips


async def get_overview(db: AsyncSession, user_id: UUID) -> DashboardOverview:
    """Get the dashboard overview for a user."""
    # Get user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one()

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    # Carbon today
    today_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id, Activity.date == today
        )
    )
    total_carbon_today = float(today_result.scalar())

    # Carbon this week
    week_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id,
            Activity.date >= week_start,
            Activity.date <= today,
        )
    )
    total_carbon_week = float(week_result.scalar())

    # Carbon this month
    month_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id,
            Activity.date >= month_start,
            Activity.date <= today,
        )
    )
    total_carbon_month = float(month_result.scalar())

    # Active challenges count
    challenges_result = await db.execute(
        select(func.count(UserChallenge.id)).where(
            UserChallenge.user_id == user_id, UserChallenge.completed == False
        )
    )
    active_challenges = int(challenges_result.scalar() or 0)

    # Achievements unlocked count
    achievements_result = await db.execute(
        select(func.count(UserAchievement.id)).where(
            UserAchievement.user_id == user_id
        )
    )
    achievements_unlocked = int(achievements_result.scalar() or 0)

    return DashboardOverview(
        total_carbon_today=round(total_carbon_today, 2),
        total_carbon_week=round(total_carbon_week, 2),
        total_carbon_month=round(total_carbon_month, 2),
        eco_score=user.eco_score,
        streak_days=user.streak_days,
        active_challenges=active_challenges,
        achievements_unlocked=achievements_unlocked,
    )


async def get_trends(db: AsyncSession, user_id: UUID) -> WeeklyTrend:
    """Get the weekly carbon trend for the last 7 days."""
    today = date.today()
    days = []
    total_kg = 0.0

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        result = await db.execute(
            select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
                Activity.user_id == user_id, Activity.date == day
            )
        )
        carbon_kg = float(result.scalar())
        total_kg += carbon_kg
        days.append(DailyCarbon(date=day.isoformat(), carbon_kg=round(carbon_kg, 2)))

    average_daily_kg = round(total_kg / 7, 2) if total_kg > 0 else 0.0

    return WeeklyTrend(
        days=days,
        total_kg=round(total_kg, 2),
        average_daily_kg=average_daily_kg,
    )


async def get_breakdown(
    db: AsyncSession, user_id: UUID, days: int = 30
) -> CategoryBreakdown:
    """Get the carbon breakdown by category for the last N days."""
    start_date = date.today() - timedelta(days=days)

    query = select(
        Activity.category,
        func.coalesce(func.sum(Activity.carbon_kg), 0.0).label("total"),
    ).where(
        Activity.user_id == user_id,
        Activity.date >= start_date,
    ).group_by(Activity.category)

    result = await db.execute(query)
    rows = result.all()

    category_totals = {row.category.value: float(row.total) for row in rows}
    total = sum(category_totals.values())

    def pct(val: float) -> float:
        return round((val / total) * 100, 1) if total > 0 else 0.0

    transport = category_totals.get("transport", 0.0)
    food = category_totals.get("food", 0.0)
    energy = category_totals.get("energy", 0.0)
    purchase = category_totals.get("purchase", 0.0)

    return CategoryBreakdown(
        transport_percent=pct(transport),
        food_percent=pct(food),
        energy_percent=pct(energy),
        purchase_percent=pct(purchase),
        transport_kg=round(transport, 2),
        food_kg=round(food, 2),
        energy_kg=round(energy, 2),
        purchase_kg=round(purchase, 2),
    )


async def get_tips(category: str | None = None) -> list[EcoTip]:
    """Get eco tips, optionally filtered by category."""
    if category:
        from app.utils.eco_tips import get_tips_by_category

        tips_data = get_tips_by_category(category)
    else:
        tips_data = get_random_tips(5)

    return [
        EcoTip(
            title=tip["title"],
            description=tip["description"],
            category=tip["category"],
            potential_savings_kg=tip["potential_savings_kg"],
        )
        for tip in tips_data
    ]
