from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievement_models import Achievement, UserAchievement
from app.models.activity_models import Activity
from app.models.user_models import User
from app.schemas.achievement_schemas import AchievementResponse, UserAchievementResponse

# Achievement criteria definitions
ACHIEVEMENT_DEFINITIONS = [
    {
        "name": "First Step",
        "description": "Log your first carbon activity",
        "icon": "leaf",
        "criteria_type": "first_activity",
        "criteria_value": 1.0,
    },
    {
        "name": "Carbon Saver",
        "description": "Save 10 kg of CO2 through eco-friendly choices",
        "icon": "star",
        "criteria_type": "carbon_saved",
        "criteria_value": 10.0,
    },
    {
        "name": "Carbon Champion",
        "description": "Save 100 kg of CO2 through eco-friendly choices",
        "icon": "trophy",
        "criteria_type": "carbon_saved",
        "criteria_value": 100.0,
    },
    {
        "name": "Carbon Hero",
        "description": "Save 500 kg of CO2 through eco-friendly choices",
        "icon": "medal",
        "criteria_type": "carbon_saved",
        "criteria_value": 500.0,
    },
    {
        "name": "Week Warrior",
        "description": "Maintain a 7-day activity streak",
        "icon": "fire",
        "criteria_type": "streak_days",
        "criteria_value": 7.0,
    },
    {
        "name": "Month Master",
        "description": "Maintain a 30-day activity streak",
        "icon": "crown",
        "criteria_type": "streak_days",
        "criteria_value": 30.0,
    },
    {
        "name": "Activity Tracker",
        "description": "Log 50 carbon activities",
        "icon": "clipboard",
        "criteria_type": "activity_count",
        "criteria_value": 50.0,
    },
    {
        "name": "Eco Enthusiast",
        "description": "Log 200 carbon activities",
        "icon": "globe",
        "criteria_type": "activity_count",
        "criteria_value": 200.0,
    },
    {
        "name": "Challenge Accepted",
        "description": "Complete your first challenge",
        "icon": "flag",
        "criteria_type": "challenges_completed",
        "criteria_value": 1.0,
    },
    {
        "name": "Challenge Master",
        "description": "Complete 10 challenges",
        "icon": "shield",
        "criteria_type": "challenges_completed",
        "criteria_value": 10.0,
    },
]


async def seed_achievements(db: AsyncSession) -> None:
    """Seed the achievements table with predefined achievements if empty."""
    result = await db.execute(select(func.count(Achievement.id)))
    count = result.scalar()

    if count == 0:
        for definition in ACHIEVEMENT_DEFINITIONS:
            achievement = Achievement(**definition)
            db.add(achievement)
        await db.flush()


async def get_all_achievements(db: AsyncSession) -> list[AchievementResponse]:
    """Get all available achievements."""
    result = await db.execute(select(Achievement).order_by(Achievement.criteria_value))
    achievements = result.scalars().all()
    return [AchievementResponse.model_validate(a) for a in achievements]


async def get_user_achievements(
    db: AsyncSession, user_id: UUID
) -> list[UserAchievementResponse]:
    """Get all achievements unlocked by a user."""
    query = (
        select(UserAchievement)
        .where(UserAchievement.user_id == user_id)
        .order_by(UserAchievement.unlocked_at.desc())
    )

    result = await db.execute(query)
    user_achievements = result.scalars().all()

    responses = []
    for ua in user_achievements:
        # Load the related achievement
        ach_result = await db.execute(
            select(Achievement).where(Achievement.id == ua.achievement_id)
        )
        achievement = ach_result.scalar_one_or_none()
        if achievement:
            responses.append(
                UserAchievementResponse(
                    id=ua.id,
                    achievement=AchievementResponse.model_validate(achievement),
                    unlocked_at=ua.unlocked_at,
                )
            )

    return responses


async def check_achievements(db: AsyncSession, user_id: UUID) -> list[str]:
    """
    Check all achievement criteria for a user and unlock any newly earned ones.
    Returns a list of newly unlocked achievement names.
    """
    # Get user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        return []

    # Get already unlocked achievement IDs
    unlocked_result = await db.execute(
        select(UserAchievement.achievement_id).where(
            UserAchievement.user_id == user_id
        )
    )
    unlocked_ids = {row[0] for row in unlocked_result.all()}

    # Get all achievements
    all_achievements_result = await db.execute(select(Achievement))
    all_achievements = all_achievements_result.scalars().all()

    # Get user stats
    activity_count_result = await db.execute(
        select(func.count(Activity.id)).where(Activity.user_id == user_id)
    )
    activity_count = activity_count_result.scalar() or 0

    from app.models.challenge_models import UserChallenge

    challenges_completed_result = await db.execute(
        select(func.count(UserChallenge.id)).where(
            UserChallenge.user_id == user_id, UserChallenge.completed == True
        )
    )
    challenges_completed = challenges_completed_result.scalar() or 0

    newly_unlocked = []

    for achievement in all_achievements:
        if achievement.id in unlocked_ids:
            continue

        earned = False

        if achievement.criteria_type == "first_activity":
            earned = activity_count >= achievement.criteria_value

        elif achievement.criteria_type == "carbon_saved":
            earned = user.total_carbon_saved >= achievement.criteria_value

        elif achievement.criteria_type == "streak_days":
            earned = user.streak_days >= achievement.criteria_value

        elif achievement.criteria_type == "activity_count":
            earned = activity_count >= achievement.criteria_value

        elif achievement.criteria_type == "challenges_completed":
            earned = challenges_completed >= achievement.criteria_value

        if earned:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id,
            )
            db.add(user_achievement)
            newly_unlocked.append(achievement.name)

    if newly_unlocked:
        await db.flush()

    return newly_unlocked
