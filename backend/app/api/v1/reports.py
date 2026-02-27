from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user_models import User
from app.services import report_service

router = APIRouter()


@router.get("/weekly")
async def get_weekly_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get the weekly carbon footprint report."""
    return await report_service.generate_weekly_report(db, current_user.id)


@router.get("/monthly")
async def get_monthly_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get the monthly carbon footprint report."""
    return await report_service.generate_monthly_report(db, current_user.id)
