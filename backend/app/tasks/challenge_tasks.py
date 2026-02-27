import asyncio
import logging
from datetime import date, timedelta

from sqlalchemy import func, select

from app.celery_app import celery_app
from app.config.database import async_session_factory
from app.models.activity_models import Activity
from app.models.challenge_models import Challenge, UserChallenge
from app.services.achievement_service import check_achievements

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Helper to run async code from synchronous Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def _update_all_challenge_progress():
    """Update progress for all active user challenges."""
    async with async_session_factory() as db:
        # Get all active, non-completed user challenges
        query = (
            select(UserChallenge, Challenge)
            .join(Challenge, UserChallenge.challenge_id == Challenge.id)
            .where(
                UserChallenge.completed == False,
                Challenge.is_active == True,
                Challenge.end_date >= date.today(),
            )
        )
        result = await db.execute(query)
        rows = result.all()

        updated = 0
        for user_challenge, challenge in rows:
            try:
                # Calculate carbon saved since joining
                carbon_result = await db.execute(
                    select(func.coalesce(func.sum(Activity.carbon_kg), 0.0)).where(
                        Activity.user_id == user_challenge.user_id,
                        Activity.category == challenge.category,
                        Activity.date >= user_challenge.joined_at,
                        Activity.date <= date.today(),
                    )
                )
                total_carbon = float(carbon_result.scalar())

                # Update progress
                user_challenge.carbon_saved = round(total_carbon, 2)
                if challenge.target_carbon_reduction > 0:
                    progress = min(
                        (total_carbon / challenge.target_carbon_reduction) * 100, 100.0
                    )
                else:
                    progress = 100.0

                user_challenge.progress_percent = round(progress, 1)
                updated += 1

            except Exception as e:
                logger.error(
                    f"Error updating challenge progress for user_challenge {user_challenge.id}: {e}"
                )

        await db.commit()
        return {"updated": updated, "total": len(rows)}


async def _check_all_completed_challenges():
    """Check and mark completed challenges, then check for new achievements."""
    async with async_session_factory() as db:
        # Find challenges that reached 100% progress
        query = select(UserChallenge).where(
            UserChallenge.completed == False,
            UserChallenge.progress_percent >= 100.0,
        )
        result = await db.execute(query)
        user_challenges = result.scalars().all()

        completed = 0
        for uc in user_challenges:
            uc.completed = True
            completed += 1

            # Check achievements for the user
            try:
                await check_achievements(db, uc.user_id)
            except Exception as e:
                logger.error(
                    f"Error checking achievements for user {uc.user_id}: {e}"
                )

        # Also mark challenges past end_date as completed
        expired_query = (
            select(UserChallenge)
            .join(Challenge, UserChallenge.challenge_id == Challenge.id)
            .where(
                UserChallenge.completed == False,
                Challenge.end_date < date.today(),
            )
        )
        expired_result = await db.execute(expired_query)
        expired = expired_result.scalars().all()
        for uc in expired:
            uc.completed = True
            completed += 1

        await db.commit()
        return {"completed": completed}


@celery_app.task(name="app.tasks.challenge_tasks.update_challenge_progress")
def update_challenge_progress():
    """Celery task: Update progress for all active user challenges."""
    logger.info("Starting challenge progress update")
    result = _run_async(_update_all_challenge_progress())
    logger.info(f"Challenge progress update complete: {result}")
    return result


@celery_app.task(name="app.tasks.challenge_tasks.check_completed_challenges")
def check_completed_challenges():
    """Celery task: Check and mark completed challenges."""
    logger.info("Starting completed challenges check")
    result = _run_async(_check_all_completed_challenges())
    logger.info(f"Completed challenges check done: {result}")
    return result
