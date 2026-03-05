from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import BadRequestError, NotFoundError
from app.models.activity_models import Activity, ActivityCategory
from app.schemas.activity_schemas import (
    ActivityCreate,
    ActivityResponse,
    ActivitySummary,
    CarbonBreakdown,
)
from app.services.carbon_calculator import calculate_carbon


async def create_activity(
    db: AsyncSession, user_id: UUID, data: ActivityCreate
) -> ActivityResponse:
    """Create a new activity with calculated carbon emissions."""
    # Validate category
    try:
        ActivityCategory(data.category)
    except ValueError:
        raise BadRequestError(
            detail=f"Invalid category '{data.category}'. Must be one of: transport, food, energy, purchase"
        )

    # Calculate carbon emissions
    try:
        carbon_kg = calculate_carbon(
            category=data.category,
            sub_category=data.sub_category,
            quantity=data.quantity,
            unit=data.unit,
        )
    except ValueError as e:
        raise BadRequestError(detail=str(e))

    activity = Activity(
        user_id=user_id,
        category=ActivityCategory(data.category),
        sub_category=data.sub_category,
        quantity=data.quantity,
        unit=data.unit,
        carbon_kg=carbon_kg,
        date=data.date,
        notes=data.notes,
    )
    db.add(activity)
    await db.flush()
    await db.refresh(activity)

    return ActivityResponse.model_validate(activity)


async def get_activities(
    db: AsyncSession,
    user_id: UUID,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ActivityResponse]:
    """Get activities for a user with optional filters and pagination."""
    query = select(Activity).where(Activity.user_id == user_id)

    if category:
        try:
            cat_enum = ActivityCategory(category)
            query = query.where(Activity.category == cat_enum)
        except ValueError:
            raise BadRequestError(detail=f"Invalid category: {category}")

    if start_date:
        query = query.where(Activity.date >= start_date)

    if end_date:
        query = query.where(Activity.date <= end_date)

    query = query.order_by(Activity.date.desc(), Activity.created_at.desc())
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    activities = result.scalars().all()

    return [ActivityResponse.model_validate(a) for a in activities]


async def get_summary(
    db: AsyncSession,
    user_id: UUID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> ActivitySummary:
    """Get aggregated activity summary for a date range."""
    if start_date is None:
        start_date = date.today() - timedelta(days=30)
    if end_date is None:
        end_date = date.today()

    query = select(
        func.coalesce(func.sum(Activity.carbon_kg), 0.0).label("total_carbon"),
        func.count(Activity.id).label("activity_count"),
    ).where(
        Activity.user_id == user_id,
        Activity.date >= start_date,
        Activity.date <= end_date,
    )

    result = await db.execute(query)
    row = result.one()

    return ActivitySummary(
        total_carbon=float(row.total_carbon),
        activity_count=int(row.activity_count),
        date_range_start=start_date,
        date_range_end=end_date,
    )


async def get_carbon_breakdown(
    db: AsyncSession,
    user_id: UUID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> CarbonBreakdown:
    """Get carbon breakdown by category for a date range."""
    if start_date is None:
        start_date = date.today() - timedelta(days=30)
    if end_date is None:
        end_date = date.today()

    query = select(
        Activity.category,
        func.coalesce(func.sum(Activity.carbon_kg), 0.0).label("total"),
    ).where(
        Activity.user_id == user_id,
        Activity.date >= start_date,
        Activity.date <= end_date,
    ).group_by(Activity.category)

    result = await db.execute(query)
    rows = result.all()

    category_totals = {row.category.value: float(row.total) for row in rows}
    total = sum(category_totals.values())

    def pct(val: float) -> float:
        return round((val / total) * 100, 1) if total > 0 else 0.0

    transport_kg = category_totals.get("transport", 0.0)
    food_kg = category_totals.get("food", 0.0)
    energy_kg = category_totals.get("energy", 0.0)
    purchase_kg = category_totals.get("purchase", 0.0)

    return CarbonBreakdown(
        transport_percent=pct(transport_kg),
        food_percent=pct(food_kg),
        energy_percent=pct(energy_kg),
        purchase_percent=pct(purchase_kg),
        transport_kg=round(transport_kg, 2),
        food_kg=round(food_kg, 2),
        energy_kg=round(energy_kg, 2),
        purchase_kg=round(purchase_kg, 2),
        total_kg=round(total, 2),
    )


async def delete_activity(
    db: AsyncSession, user_id: UUID, activity_id: UUID
) -> None:
    """Delete an activity belonging to a user."""
    result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id, Activity.user_id == user_id
        )
    )
    activity = result.scalar_one_or_none()

    if activity is None:
        raise NotFoundError(detail="Activity not found")

    await db.execute(
        delete(Activity).where(Activity.id == activity_id)
    )
    await db.flush()
