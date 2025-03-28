import ast
import asyncio
from celery import Celery
from celery.schedules import crontab
from .service import get_periodic_tasks
from app.workers.tasks import user_initialized_task
from .celery_app import celery_app

def fetch_periodic_tasks():
    """Helper function to fetch tasks synchronously."""
    print("Fetching periodic tasks...")
    return asyncio.run(get_periodic_tasks())

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    """Set up periodic tasks from both hardcoded and database schedules."""

    # 📌 **Dynamically Loaded Tasks from DB**
    periodic_tasks = fetch_periodic_tasks()
    for task in periodic_tasks:
        crondict = ast.literal_eval(task["crontab"])
        sender.add_periodic_task(
            crontab(
                minute=crondict["minute"],
                hour=crondict["hour"],
                day_of_week=crondict["day_of_week"],
                day_of_month=crondict["day_of_month"],
                month_of_year=crondict["month_of_year"],
            ),
            user_initialized_task.s(task["task_name"]),
            name=task["task_name"],
        )

    return f"Periodic tasks set up successfully: {sender}"