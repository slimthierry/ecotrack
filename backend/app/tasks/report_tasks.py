import asyncio
import logging

from sqlalchemy import select

from app.celery_app import celery_app
from app.config.database import async_session_factory
from app.models.user_models import User
from app.services.report_service import generate_weekly_report

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Helper to run async code from synchronous Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def _generate_all_weekly_reports():
    """Generate weekly reports for all active users."""
    async with async_session_factory() as db:
        result = await db.execute(
            select(User).where(User.is_active == True)
        )
        users = result.scalars().all()

        reports_generated = 0
        errors = 0

        for user in users:
            try:
                report = await generate_weekly_report(db, user.id)
                if "error" not in report:
                    reports_generated += 1
                    logger.info(f"Weekly report generated for user {user.username}")
                else:
                    errors += 1
                    logger.error(
                        f"Error generating report for user {user.username}: {report['error']}"
                    )
            except Exception as e:
                errors += 1
                logger.error(
                    f"Exception generating report for user {user.username}: {e}"
                )

    return {
        "reports_generated": reports_generated,
        "errors": errors,
        "total_users": len(users),
    }


@celery_app.task(name="app.tasks.report_tasks.generate_weekly_reports")
def generate_weekly_reports():
    """Celery task: Generate weekly reports for all active users."""
    logger.info("Starting weekly report generation")
    result = _run_async(_generate_all_weekly_reports())
    logger.info(f"Weekly report generation complete: {result}")
    return result
