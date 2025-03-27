from celery import Celery
from celery.beat import PersistentScheduler
import os
from dotenv import load_dotenv


load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery
celery_app = Celery(
    "workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.workers.tasks"],
)

# Optional Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_scheduler=PersistentScheduler,
    beat_schedule={},
)


if __name__ == "__main__":
    celery_app.start()
