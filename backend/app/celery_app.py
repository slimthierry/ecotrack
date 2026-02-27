from celery import Celery
from celery.schedules import crontab

from app.config.settings import settings

celery_app = Celery(
    "ecotrack",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.report_tasks",
        "app.tasks.challenge_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Beat schedule: periodic tasks
celery_app.conf.beat_schedule = {
    "generate-weekly-reports": {
        "task": "app.tasks.report_tasks.generate_weekly_reports",
        "schedule": crontab(hour=8, minute=0, day_of_week="sunday"),
        "args": (),
    },
    "update-challenge-progress": {
        "task": "app.tasks.challenge_tasks.update_challenge_progress",
        "schedule": crontab(hour=0, minute=30),  # Daily at 00:30 UTC
        "args": (),
    },
    "check-completed-challenges": {
        "task": "app.tasks.challenge_tasks.check_completed_challenges",
        "schedule": crontab(hour=1, minute=0),  # Daily at 01:00 UTC
        "args": (),
    },
}
