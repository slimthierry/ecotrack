from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_db
from app.models.user_models import User
from app.schemas.activity_schemas import (
    ActivityCreate,
    ActivityResponse,
    ActivitySummary,
)
from app.services import activity_service
from app.services.achievement_service import check_achievements

router = APIRouter()


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ActivityResponse:
    """Create a new carbon activity. Carbon emissions are calculated automatically."""
    activity = await activity_service.create_activity(db, current_user.id, data)

    # Check if any new achievements were unlocked
    await check_achievements(db, current_user.id)

    return activity


@router.get("/", response_model=list[ActivityResponse])
async def list_activities(
    category: str | None = Query(None, description="Filter by category"),
    start_date: date | None = Query(None, description="Filter from date"),
    end_date: date | None = Query(None, description="Filter to date"),
    limit: int = Query(50, ge=1, le=200, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ActivityResponse]:
    """List activities with optional filters and pagination."""
    return await activity_service.get_activities(
        db, current_user.id, category, start_date, end_date, limit, offset
    )


@router.get("/summary", response_model=ActivitySummary)
async def get_summary(
    start_date: date | None = Query(None, description="Start of date range"),
    end_date: date | None = Query(None, description="End of date range"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ActivitySummary:
    """Get aggregated activity summary for a date range."""
    return await activity_service.get_summary(db, current_user.id, start_date, end_date)


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete an activity by ID."""
    await activity_service.delete_activity(db, current_user.id, activity_id)
