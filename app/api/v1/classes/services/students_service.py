from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..schemas import *
from typing import Optional
from sqlalchemy import desc
from ..models import TeachersStudent

class ClassStudentsService:
    # create a student and add to the a class
    async def create_student(
        self,
        student: CreateStudentModel,
        db: AsyncSession = None
    ) -> TeachersStudent:
        """
        Create a new student and add them to a class.
        """
        new_student = TeachersStudent(
            firstname=student.firstname,
            lastname=student.lastname,
            gender = student.gender,
            parent_phone_number=student.parent_phone_number,
            dob=student.dob,
            parent_email=student.parent_email,
            address=student.address,
            learning_path=student.learning_path,
            subject_teachers_class_id=student.subject_teachers_class_id,
            teachers_class_id=student.teachers_class_id,
        )
        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)

        return new_student
    
    async def update_student(
        self,
        student_id: UUID,
        updated_data: UpdateStudentModel,  # a model with optional fields
        db: AsyncSession
    ) -> TeachersStudent:
        """
        Update an existing student's details including their class.
        """
        result = await db.execute(select(TeachersStudent).where(TeachersStudent.id == student_id))
        student = result.scalar_one_or_none()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Update all provided fields
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(student, field, value)

        await db.commit()
        await db.refresh(student)

        return student
    
    async def delete_student(
        self,
        student_id: UUID,
        db: AsyncSession
    ) -> None:
        """
        Delete a student and automatically remove them from any class (handled by cascade).
        """
        result = await db.execute(select(TeachersStudent).where(TeachersStudent.id == student_id))
        student = result.scalar_one_or_none()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        await db.delete(student)
        await db.commit()

