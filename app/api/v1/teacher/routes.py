# ✅ teacher_routes.py
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.schemas.schemas import UserModel
from .schemas import TeacherCreate, TeacherResponse
from app.core.database import async_get_db
from .service import TeacherService
from uuid import UUID
from app.api.v1.auth.dependencies import (
    RoleChecker,
    get_current_user,
)

teachers_router = APIRouter()
role_checker = RoleChecker(["admin", "teacher"])


@teachers_router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: TeacherCreate, db: AsyncSession = Depends(async_get_db)):
    return await TeacherService.create_teacher(teacher, db)


@teachers_router.get("/", response_model=list[TeacherResponse])
async def get_all_teachers(
    skip: int = 0,
    limit: int = 100,
    _: RoleChecker = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    return await TeacherService.get_all_teachers(skip=skip, limit=limit, db=db)
    


@teachers_router.get("/me", response_model=TeacherResponse)
async def get_teacher_me(
        user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)):
    user_id = user.id
    if not user.role == "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not a teacher")
    return await TeacherService.get_teacher_by_user_id(user_id, db)


@teachers_router.get("/{user_id}", response_model=TeacherResponse)
async def get_teacher_by_user_id(
        user_id: UUID,
        _: RoleChecker = Depends(role_checker),
        db: AsyncSession = Depends(async_get_db)):
    return await TeacherService.get_teacher_by_user_id(user_id, db)


@teachers_router.put("/{user_id}", response_model=TeacherResponse)
async def update_teacher(
        user_id: UUID, teacher: TeacherCreate,
        _: RoleChecker = Depends(role_checker),
        db: AsyncSession = Depends(async_get_db)):
    return await TeacherService.update_teacher(user_id, teacher, db)


@teachers_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_teacher(
        user_id: UUID,
        _: RoleChecker = Depends(role_checker),
        db: AsyncSession = Depends(async_get_db)):
    return await TeacherService.delete_teacher(user_id, db)
