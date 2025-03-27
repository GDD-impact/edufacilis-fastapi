from fastapi import APIRouter,Depends,status,HTTPException
from app.api.v1.auth.oauth2 import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_get_db


student_router = APIRouter()

@student_router.get("/")
def get_students(db: AsyncSession = Depends(async_get_db)):
    return {"Hello": "Students", "status": "database connection successful"}