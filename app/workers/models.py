from sqlalchemy import Column, Integer, String
from app.core.database import Base


class PeriodicTask(Base):
    __tablename__ = "periodic_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String, nullable=False)
    task_args = Column(String, nullable=True)
    task_kwargs = Column(String, nullable=True)
    crontab = Column(String, nullable=False)
    scheduling_type = Column(String, nullable=True)