from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user_models import User
from app.schemas.challenge_schemas import (
    ChallengeJoin,
    ChallengeProgress,
    ChallengeResponse,
    LeaderboardEntry,
)
from app.services import challenge_service

router = APIRouter()


@router.get("/", response_model=list[ChallengeResponse])
async def get_active_challenges(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ChallengeResponse]:
    """Get all currently active challenges."""
    return await challenge_service.get_active_challenges(db)


@router.post("/join", response_model=ChallengeProgress, status_code=201)
async def join_challenge(
    data: ChallengeJoin,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChallengeProgress:
    """Join a challenge."""
    return await challenge_service.join_challenge(db, current_user.id, data.challenge_id)


@router.get("/leaderboard/{challenge_id}", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    challenge_id: UUID,
    limit: int = Query(20, ge=1, le=100, description="Max entries"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[LeaderboardEntry]:
    """Get the leaderboard for a specific challenge."""
    return await challenge_service.get_leaderboard(db, challenge_id, limit)


@router.get("/my-challenges", response_model=list[ChallengeProgress])
async def get_my_challenges(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ChallengeProgress]:
    """Get all challenges the current user has joined."""
    return await challenge_service.get_user_challenges(db, current_user.id)
