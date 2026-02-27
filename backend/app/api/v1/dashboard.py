from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user_models import User
from app.schemas.dashboard_schemas import (
    CategoryBreakdown,
    DashboardOverview,
    EcoTip,
    WeeklyTrend,
)
from app.services import dashboard_service

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardOverview:
    """Get the dashboard overview with carbon totals, score, and streaks."""
    return await dashboard_service.get_overview(db, current_user.id)


@router.get("/trends", response_model=WeeklyTrend)
async def get_trends(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WeeklyTrend:
    """Get weekly carbon trends (last 7 days)."""
    return await dashboard_service.get_trends(db, current_user.id)


@router.get("/breakdown", response_model=CategoryBreakdown)
async def get_breakdown(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CategoryBreakdown:
    """Get carbon breakdown by category."""
    return await dashboard_service.get_breakdown(db, current_user.id, days)


@router.get("/tips", response_model=list[EcoTip])
async def get_tips(
    category: str | None = Query(None, description="Filter tips by category"),
    current_user: User = Depends(get_current_user),
) -> list[EcoTip]:
    """Get eco-friendly tips, optionally filtered by category."""
    return await dashboard_service.get_tips(category)
