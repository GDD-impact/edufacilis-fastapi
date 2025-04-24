from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from ..schemas import *
from typing import Optional
from sqlalchemy import desc
from ..models import SubjectTeachersClass, TeachersClass

# ---------------------------------------------------------
# Main Class Service
# ---------------------------------------------------------


class MainClassService:
    async def get_all_main_classes(
            self,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = None
    ) -> List[TeachersClass]:
        """
        Get all main classes created by a teacher.
        """
        query = select(TeachersClass).order_by(
            desc(TeachersClass.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_teacher_main_class(
            self,
            teacher_id: UUID,
            db: AsyncSession = None
    ) -> List[TeachersClass]:
        """
        Get Main classes created by a teacher.
        """
        query = select(TeachersClass).options(
            joinedload(TeachersClass.students)  # Eagerly load students
        ).filter(TeachersClass.teacher_id == teacher_id)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_teacher_main_class_by_id(
            self,
            class_id: UUID,
            db: AsyncSession = None
    ) -> Optional[TeachersClass]:
        """
        Get a specific main class by ID.
        """
        query = select(TeachersClass).options(
            joinedload(TeachersClass.students)  # Eagerly load students
        ).filter(
            TeachersClass.id == class_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def check_main_class_exists(
        self,
        class_type: str,
        class_name: str,
        academic_session: str,
        db: AsyncSession
    ) -> bool:
        """
        Check if a main class exists based on class_type, class_name, and academic_session.
        """
        query = select(TeachersClass).filter(
            TeachersClass.class_type == class_type,
            TeachersClass.class_name == class_name,
            TeachersClass.academic_session == academic_session
        )

        result = await db.execute(query)
        return result.scalar_one_or_none() is not None

    async def create_teacher_main_class(
            self,
            details: CreateTeacherMainClassModel,
            db: AsyncSession = None
    ) -> TeachersClass:
        """
        Create a new main class for a teacher.
        """
        # check if the class already exists with the same exact credentials
        same_class_credentials = await self.check_main_class_exists(
            class_type=details.class_type,
            class_name=details.class_name,
            academic_session=details.academic_session,
            db=db
        )

        if same_class_credentials:
            raise HTTPException(
                status_code=400, detail="Class already exists with the same credentials")

        new_class = TeachersClass(
            class_name=details.class_name,
            class_type=details.class_type,
            academic_session=details.academic_session,
            teacher_id=details.teacher_id
        )
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        return new_class

    async def update_teacher_main_class(
            self,
            class_id: UUID,
            details: CreateTeacherMainClassModel,
            db: AsyncSession = None
    ) -> TeachersClass:
        """
        Update a specific main class.
        """
        existing_class = await self.get_teacher_main_class_by_id(
            class_id=class_id, db=db)

        if not existing_class:
            raise HTTPException(status_code=404, detail="Class not found")

        # check if the class already exists with the same exact credentials
        same_class_credentials = await self.check_main_class_exists(
            class_type=details.class_type,
            class_name=details.class_name,
            academic_session=details.academic_session,
            db=db
        )

        if same_class_credentials:
            raise HTTPException(
                status_code=400, detail="Class already exists with the same credentials")

        existing_class.class_name = details.class_name
        existing_class.class_type = details.class_type
        existing_class.academic_session = details.academic_session

        await db.commit()
        await db.refresh(existing_class)
        return existing_class


# ---------------------------------------------------------
# Subject Class Service
# ---------------------------------------------------------

class SubjectClassService:
    async def get_all_subject_classes(
            self,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = None
    ) -> List[SubjectTeachersClass]:
        """
        Get all subject classes created by a teacher.
        """
        query = select(SubjectTeachersClass).order_by(
            desc(SubjectTeachersClass.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_all_teachers_sub_classes(
            self,
            teacher_id: UUID,
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = None
    ) -> List[SubjectTeachersClass]:
        """
        Get all subject classes created by a teacher.
        """
        query = select(SubjectTeachersClass).filter(
            SubjectTeachersClass.teacher_id == teacher_id).order_by(desc(SubjectTeachersClass.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_teacher_sub_class_by_id(
        self,
        class_id: UUID,
        db: AsyncSession = None
    ) -> Optional[SubjectTeachersClass]:
        """
        Get a specific subject class by ID.
        """
        query = select(SubjectTeachersClass).options(
            joinedload(SubjectTeachersClass.students)  # Eagerly load students
        ).filter(
            SubjectTeachersClass.id == class_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def check_sub_class_exists(
        self,
        class_type: str,
        class_name: str,
        academic_session: str,
        subject_name: str,
        db: AsyncSession
    ) -> bool:
        """
        Check if a class exists based on class_type, class_name, and academic_session.
        """
        query = select(SubjectTeachersClass).filter(
            SubjectTeachersClass.class_type == class_type,
            SubjectTeachersClass.class_name == class_name,
            SubjectTeachersClass.subject_name == subject_name,
            SubjectTeachersClass.academic_session == academic_session
        )

        result = await db.execute(query)
        return result.scalar_one_or_none() is not None

    async def create_teacher_sub_class(
            self,
            details: CreateTeacherSubjectClassModel,
            db: AsyncSession = None
    ) -> SubjectTeachersClass:
        """
        Create a new subject class for a teacher.
        """
        # check if the class already exists with the same exact credentials
        same_class_credentials = await self.check_sub_class_exists(
            class_type=details.class_type,
            class_name=details.class_name,
            academic_session=details.academic_session,
            subject_name=details.subject_name,
            db=db
        )

        if same_class_credentials:
            raise HTTPException(
                status_code=400, detail="Class already exists with the same credentials")

        new_class = SubjectTeachersClass(
            class_name=details.class_name,
            class_type=details.class_type,
            academic_session=details.academic_session,
            subject_name=details.subject_name,
            teacher_id=details.teacher_id
        )
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        return new_class

    async def update_teacher_sub_class(
            self,
            class_id: UUID,
            details: CreateTeacherSubjectClassModel,
            db: AsyncSession = None
    ) -> SubjectTeachersClass:
        """
        Update a specific subject class.
        """
        query = select(SubjectTeachersClass).filter(
            SubjectTeachersClass.id == class_id)
        result = await db.execute(query)
        existing_class = result.scalar_one_or_none()

        if not existing_class:
            raise HTTPException(status_code=404, detail="Class not found")

        # check if the class already exists with the same exact credentials
        same_class_credentials = await self.check_sub_class_exists(
            class_type=details.class_type,
            class_name=details.class_name,
            academic_session=details.academic_session,
            db=db
        )

        if same_class_credentials:
            raise HTTPException(
                status_code=400, detail="Class already exists with the same credentials")

        existing_class.class_name = details.class_name
        existing_class.class_type = details.class_type
        existing_class.academic_session = details.academic_session
        existing_class.subject_name = details.subject_name

        await db.commit()
        await db.refresh(existing_class)
        return existing_class
