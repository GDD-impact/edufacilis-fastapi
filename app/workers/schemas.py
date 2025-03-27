from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class PeriodicTaskCreate(BaseModel):
    task_name: str
    task_args: List[str] = []
    task_kwargs: Dict[str, Any] = {}
    scheduling_type: str
    start_datetime: datetime
    end_datetime: datetime