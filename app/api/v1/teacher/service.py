# ✅ teacher_service.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .models import Teacher
from .schemas import TeacherCreate, TeacherResponse
from fastapi import HTTPException, status


class TeacherService:
    @staticmethod
    async def create_teacher(teacher_data: TeacherCreate, db: AsyncSession) -> Teacher:
        new_teacher = Teacher(**teacher_data.model_dump())
        db.add(new_teacher)
        await db.commit()
        await db.refresh(new_teacher)
        return new_teacher

    @staticmethod
    async def get_all_teachers(
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = None
    ) -> list[Teacher]:
        result = await db.execute(select(Teacher).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def get_teacher_by_user_id(user_id: UUID, db: AsyncSession) -> Teacher:
        result = await db.execute(select(Teacher).where(Teacher.user_id == user_id))
        teacher = result.scalar_one_or_none()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        return teacher

    @staticmethod
    async def update_teacher(user_id: UUID, teacher_data: TeacherCreate, db: AsyncSession) -> Teacher:
        teacher = await TeacherService.get_teacher_by_user_id(user_id, db)
        for key, value in teacher_data.model_dump().items():
            setattr(teacher, key, value)
        await db.commit()
        await db.refresh(teacher)
        return teacher

    @staticmethod
    async def delete_teacher(user_id: UUID, db: AsyncSession):
        teacher = await TeacherService.get_teacher_by_user_id(user_id, db)
        await db.delete(teacher)
        await db.commit()
        return {"message": "Teacher deleted successfully"}
