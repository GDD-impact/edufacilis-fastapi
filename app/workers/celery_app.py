from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/2")

# Initialize Celery
celery_app = Celery(
    "workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.workers.tasks"],  # Ensure your tasks are in this module
)

# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    "send_daily_email": {
        "task": "send_email_task",
        "schedule": crontab(minute=0, hour=9),  # Runs daily at 9 AM
        "args": ("admin@example.com", "Daily Update", "This is your daily update."),
    },
    "generate_monthly_report": {
        "task": "generate_report_task",
        "schedule": crontab(minute=0, hour=0, day_of_month=1),  # Runs on the 1st of every month
        "args": ("Monthly Sales",),
    },
    "test_periodic_task": {
        "task": "test_periodic_task",
        "schedule": crontab(minute="*"),  # Runs every minute
        "args": ("every minute Report",),
    },
}

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()
