from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_models import Activity
from app.models.user_models import User
from app.utils.carbon_calculations import (
    compare_to_average,
    format_carbon,
    kg_to_driving_km,
    kg_to_trees_equivalent,
)


async def generate_weekly_report(db: AsyncSession, user_id: UUID) -> dict:
    """
    Generate a weekly carbon summary report for a user.
    Covers the last 7 days from today.
    """
    today = date.today()
    week_start = today - timedelta(days=6)

    # Get user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        return {"error": "User not found"}

    # Total carbon this week
    total_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id,
            Activity.date >= week_start,
            Activity.date <= today,
        )
    )
    total_carbon = float(total_result.scalar())

    # Activity count this week
    count_result = await db.execute(
        select(func.count(Activity.id)).where(
            Activity.user_id == user_id,
            Activity.date >= week_start,
            Activity.date <= today,
        )
    )
    activity_count = int(count_result.scalar() or 0)

    # Category breakdown
    breakdown_result = await db.execute(
        select(
            Activity.category,
            func.coalesce(func.sum(Activity.carbon_kg), 0.0).label("total"),
        )
        .where(
            Activity.user_id == user_id,
            Activity.date >= week_start,
            Activity.date <= today,
        )
        .group_by(Activity.category)
    )
    breakdown_rows = breakdown_result.all()
    category_breakdown = {
        row.category.value: round(float(row.total), 2) for row in breakdown_rows
    }

    # Daily breakdown
    daily_breakdown = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_result = await db.execute(
            select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
                Activity.user_id == user_id, Activity.date == day
            )
        )
        day_carbon = float(day_result.scalar())
        daily_breakdown.append({
            "date": day.isoformat(),
            "carbon_kg": round(day_carbon, 2),
        })

    # Previous week for comparison
    prev_week_start = week_start - timedelta(days=7)
    prev_week_end = week_start - timedelta(days=1)
    prev_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id,
            Activity.date >= prev_week_start,
            Activity.date <= prev_week_end,
        )
    )
    prev_total = float(prev_result.scalar())

    # Calculate week-over-week change
    if prev_total > 0:
        change_percent = round(((total_carbon - prev_total) / prev_total) * 100, 1)
    else:
        change_percent = 0.0

    daily_average = total_carbon / 7 if total_carbon > 0 else 0.0
    comparison = compare_to_average(daily_average)

    return {
        "user": {
            "username": user.username,
            "eco_score": user.eco_score,
            "streak_days": user.streak_days,
        },
        "period": {
            "start": week_start.isoformat(),
            "end": today.isoformat(),
        },
        "summary": {
            "total_carbon_kg": round(total_carbon, 2),
            "total_carbon_formatted": format_carbon(total_carbon),
            "activity_count": activity_count,
            "daily_average_kg": round(daily_average, 2),
            "trees_equivalent": kg_to_trees_equivalent(total_carbon),
            "driving_km_equivalent": kg_to_driving_km(total_carbon),
        },
        "comparison": {
            "previous_week_kg": round(prev_total, 2),
            "change_percent": change_percent,
            "vs_average": comparison,
        },
        "category_breakdown": category_breakdown,
        "daily_breakdown": daily_breakdown,
    }


async def generate_monthly_report(db: AsyncSession, user_id: UUID) -> dict:
    """
    Generate a monthly carbon summary report for a user.
    Covers the last 30 days from today.
    """
    today = date.today()
    month_start = today - timedelta(days=29)

    # Get user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        return {"error": "User not found"}

    # Total carbon this month
    total_result = await db.execute(
        select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
            Activity.user_id == user_id,
            Activity.date >= month_start,
            Activity.date <= today,
        )
    )
    total_carbon = float(total_result.scalar())

    # Activity count
    count_result = await db.execute(
        select(func.count(Activity.id)).where(
            Activity.user_id == user_id,
            Activity.date >= month_start,
            Activity.date <= today,
        )
    )
    activity_count = int(count_result.scalar() or 0)

    # Category breakdown
    breakdown_result = await db.execute(
        select(
            Activity.category,
            func.coalesce(func.sum(Activity.carbon_kg), 0.0).label("total"),
        )
        .where(
            Activity.user_id == user_id,
            Activity.date >= month_start,
            Activity.date <= today,
        )
        .group_by(Activity.category)
    )
    breakdown_rows = breakdown_result.all()
    category_breakdown = {
        row.category.value: round(float(row.total), 2) for row in breakdown_rows
    }

    # Weekly breakdown (4 weeks)
    weekly_breakdown = []
    for week in range(4):
        ws = month_start + timedelta(weeks=week)
        we = min(ws + timedelta(days=6), today)
        week_result = await db.execute(
            select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
                Activity.user_id == user_id,
                Activity.date >= ws,
                Activity.date <= we,
            )
        )
        week_carbon = float(week_result.scalar())
        weekly_breakdown.append({
            "week_start": ws.isoformat(),
            "week_end": we.isoformat(),
            "carbon_kg": round(week_carbon, 2),
        })

    daily_average = total_carbon / 30 if total_carbon > 0 else 0.0
    comparison = compare_to_average(daily_average)

    return {
        "user": {
            "username": user.username,
            "eco_score": user.eco_score,
            "total_carbon_saved": user.total_carbon_saved,
        },
        "period": {
            "start": month_start.isoformat(),
            "end": today.isoformat(),
        },
        "summary": {
            "total_carbon_kg": round(total_carbon, 2),
            "total_carbon_formatted": format_carbon(total_carbon),
            "activity_count": activity_count,
            "daily_average_kg": round(daily_average, 2),
            "trees_equivalent": kg_to_trees_equivalent(total_carbon),
            "driving_km_equivalent": kg_to_driving_km(total_carbon),
        },
        "comparison": {
            "vs_average": comparison,
        },
        "category_breakdown": category_breakdown,
        "weekly_breakdown": weekly_breakdown,
    }
