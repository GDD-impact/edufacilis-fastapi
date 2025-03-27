from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_get_db
from .models import PeriodicTask
from .schemas import PeriodicTaskCreate
from .service import create_cron_schedule

schedule_router = APIRouter()

@schedule_router.post("/add_periodic_task")
async def add_periodic_task(task_data: PeriodicTaskCreate, db: AsyncSession = Depends(async_get_db)):
    """
    API to add a new periodic task dynamically.
    """
    cron_value = create_cron_schedule(
        task_data.scheduling_type,
        task_data.start_datetime,
        task_data.end_datetime,
    )

    new_task = PeriodicTask(
        task_name=task_data.task_name,
        task_args=task_data.task_args,
        task_kwargs=task_data.task_kwargs,
        crontab=str(cron_value.__dict__),
        scheduling_type=task_data.scheduling_type,
    )
    db.add(new_task)
    await db.commit()
    return {"message": "Task scheduled successfully"}
