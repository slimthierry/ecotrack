from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user_models import User
from app.schemas.achievement_schemas import AchievementResponse, UserAchievementResponse
from app.services import achievement_service

router = APIRouter()


@router.get("/", response_model=list[AchievementResponse])
async def get_all_achievements(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AchievementResponse]:
    """Get all available achievements."""
    return await achievement_service.get_all_achievements(db)


@router.get("/my-achievements", response_model=list[UserAchievementResponse])
async def get_my_achievements(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[UserAchievementResponse]:
    """Get all achievements unlocked by the current user."""
    return await achievement_service.get_user_achievements(db, current_user.id)
