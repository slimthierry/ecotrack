from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import BadRequestError, NotFoundError
from app.models.challenge_models import Challenge, UserChallenge
from app.models.user_models import User
from app.schemas.challenge_schemas import (
    ChallengeProgress,
    ChallengeResponse,
    LeaderboardEntry,
)


async def get_active_challenges(db: AsyncSession) -> list[ChallengeResponse]:
    """Get all currently active challenges."""
    query = select(Challenge).where(
        Challenge.is_active == True,
        Challenge.end_date >= date.today(),
    ).order_by(Challenge.start_date.desc())

    result = await db.execute(query)
    challenges = result.scalars().all()

    responses = []
    for challenge in challenges:
        # Count participants
        count_query = select(func.count(UserChallenge.id)).where(
            UserChallenge.challenge_id == challenge.id
        )
        count_result = await db.execute(count_query)
        participants_count = count_result.scalar() or 0

        response = ChallengeResponse(
            id=challenge.id,
            title=challenge.title,
            description=challenge.description,
            category=challenge.category,
            target_carbon_reduction=challenge.target_carbon_reduction,
            duration_days=challenge.duration_days,
            start_date=challenge.start_date,
            end_date=challenge.end_date,
            is_active=challenge.is_active,
            participants_count=participants_count,
            created_at=challenge.created_at,
        )
        responses.append(response)

    return responses


async def join_challenge(
    db: AsyncSession, user_id: UUID, challenge_id: UUID
) -> ChallengeProgress:
    """Join a challenge. Raises error if already joined or challenge not found."""
    # Get the challenge
    result = await db.execute(
        select(Challenge).where(Challenge.id == challenge_id, Challenge.is_active == True)
    )
    challenge = result.scalar_one_or_none()

    if challenge is None:
        raise NotFoundError(detail="Challenge not found or is no longer active")

    if challenge.end_date < date.today():
        raise BadRequestError(detail="This challenge has already ended")

    # Check if already joined
    result = await db.execute(
        select(UserChallenge).where(
            UserChallenge.user_id == user_id,
            UserChallenge.challenge_id == challenge_id,
        )
    )
    if result.scalar_one_or_none() is not None:
        raise BadRequestError(detail="You have already joined this challenge")

    # Join the challenge
    user_challenge = UserChallenge(
        user_id=user_id,
        challenge_id=challenge_id,
        joined_at=date.today(),
        progress_percent=0.0,
        completed=False,
        carbon_saved=0.0,
    )
    db.add(user_challenge)
    await db.flush()

    days_remaining = (challenge.end_date - date.today()).days

    return ChallengeProgress(
        challenge_id=challenge.id,
        challenge_title=challenge.title,
        progress_percent=0.0,
        carbon_saved=0.0,
        completed=False,
        joined_at=date.today(),
        days_remaining=max(days_remaining, 0),
    )


async def get_user_challenges(
    db: AsyncSession, user_id: UUID
) -> list[ChallengeProgress]:
    """Get all challenges a user has joined with progress."""
    query = (
        select(UserChallenge, Challenge)
        .join(Challenge, UserChallenge.challenge_id == Challenge.id)
        .where(UserChallenge.user_id == user_id)
        .order_by(UserChallenge.joined_at.desc())
    )

    result = await db.execute(query)
    rows = result.all()

    progress_list = []
    for user_challenge, challenge in rows:
        days_remaining = (challenge.end_date - date.today()).days
        progress_list.append(
            ChallengeProgress(
                challenge_id=challenge.id,
                challenge_title=challenge.title,
                progress_percent=user_challenge.progress_percent,
                carbon_saved=user_challenge.carbon_saved,
                completed=user_challenge.completed,
                joined_at=user_challenge.joined_at,
                days_remaining=max(days_remaining, 0),
            )
        )

    return progress_list


async def get_leaderboard(
    db: AsyncSession, challenge_id: UUID, limit: int = 20
) -> list[LeaderboardEntry]:
    """Get the leaderboard for a specific challenge."""
    # Verify challenge exists
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    if result.scalar_one_or_none() is None:
        raise NotFoundError(detail="Challenge not found")

    query = (
        select(User.username, UserChallenge.carbon_saved)
        .join(User, UserChallenge.user_id == User.id)
        .where(UserChallenge.challenge_id == challenge_id)
        .order_by(UserChallenge.carbon_saved.desc())
        .limit(limit)
    )

    result = await db.execute(query)
    rows = result.all()

    leaderboard = []
    for rank, (username, carbon_saved) in enumerate(rows, start=1):
        leaderboard.append(
            LeaderboardEntry(
                username=username,
                carbon_saved=round(carbon_saved, 2),
                rank=rank,
            )
        )

    return leaderboard
