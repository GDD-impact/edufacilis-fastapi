from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_get_db


student_router = APIRouter()

@student_router.get("/")
def get_students(session: AsyncSession = Depends(async_get_db)):
    return {"Hello": "Students", "status": "database connection successful"}