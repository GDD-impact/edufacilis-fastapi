from celery.schedules import crontab
from sqlalchemy.future import select
from app.core.database import async_get_db
from app.workers.models import PeriodicTask

async def get_periodic_tasks():
    """
    Asynchronously fetch all periodic tasks from the database.
    Returns:
        List[dict]: A list of dictionaries containing task details.
    """
    async with async_get_db() as session:
        result = await session.execute(select(PeriodicTask))  # Async DB query
        tasks = result.scalars().all()  # Fetch results
    
    return [
        {
            "task_name": task.task_name,
            "task_args": task.task_args,
            "task_kwargs": task.task_kwargs,
            "crontab": task.crontab,
            "scheduling_type": task.scheduling_type,
        }
        for task in tasks
    ]



def create_cron_schedule(scheduling_type, start_datetime, end_datetime):
    """Generates crontab schedules dynamically based on user input."""
    start_time = start_datetime.time()
    
    if scheduling_type == "daily":
        cron_value = crontab(hour=start_time.hour, minute=start_time.minute)
    elif scheduling_type == "weekly":
        cron_value = crontab(day_of_week=start_datetime.weekday(), hour=start_time.hour, minute=start_time.minute)
    elif scheduling_type == "weekdays":
        cron_value = crontab(day_of_week="mon-fri", hour=start_time.hour, minute=start_time.minute)
    elif scheduling_type == "monthly":
        cron_value = crontab(day_of_month=start_datetime.day, hour=start_time.hour, minute=start_time.minute)
    elif scheduling_type == "yearly":
        cron_value = crontab(day_of_year=start_datetime.timetuple().tm_yday, hour=start_time.hour, minute=start_time.minute)
    elif scheduling_type == "once":
        cron_value = crontab(day_of_year=start_datetime.timetuple().tm_yday, hour=start_time.hour, minute=start_time.minute)
    else:
        raise ValueError("Invalid scheduling type")

    return cron_value
