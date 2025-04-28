from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy import Date
from app.api.v1.classes.services.class_services import MainClassService
from ..models import AttendanceStatus, ClassAttendance

main_class_service = MainClassService()

# --------------------------------------------------------------
# ClassAttendance Service
# --------------------------------------------------------------


class ClassAttendanceService:
    def __init__(self):
        pass

    async def create_class_attendance(self, db: AsyncSession, class_id: UUID, date: datetime) -> List[ClassAttendance]:
        """
        Create attendance records for all students in a class for today.
        """
        # Fetch the class object properly
        class_object = await main_class_service.get_teacher_main_class_by_id(class_id, db)
        if not class_object:
            raise HTTPException(status_code=404, detail="Class not found")

        students = class_object.students
        if not students:
            raise HTTPException(
                status_code=404, detail="No students found in this class")

        attendance_records = []
        for student in students:
            attendance_record = ClassAttendance(
                date=date,
                status=AttendanceStatus.NOT_TAKEN,
                student_id=student.id,
                teachers_class_id=class_id
            )
            db.add(attendance_record)
            attendance_records.append(attendance_record)

        await db.commit()
        return attendance_records  # Return the list of created records

    async def get_attendance_by_student(self, db: AsyncSession, student_id: UUID, class_id: UUID) -> List[ClassAttendance]:
        """
        Get all attendance records for a specific student in a specific class.
        """
        result = await db.execute(
            select(ClassAttendance).where(
                ClassAttendance.student_id == student_id,
                ClassAttendance.teachers_class_id == class_id
            ).order_by(desc(ClassAttendance.date))
        )
        return result.scalars().all()

    async def get_attendance_by_date_and_class(self, db: AsyncSession, date: datetime, class_id: UUID) -> List[ClassAttendance]:
        """
        Get all attendance records for a specific date in a specific class.
        """
        result = await db.execute(
            select(ClassAttendance).where(
                ClassAttendance.teachers_class_id == class_id,
                ClassAttendance.date.cast(
                    Date) == date.date()  # Correct comparison
            ).order_by(desc(ClassAttendance.date))
        )
        return result.scalars().all()

    async def update_attendance(self, db: AsyncSession, attendance_id: UUID, attendance_status: str) -> ClassAttendance:
        """
        Update an existing attendance record.
        """
        result = await db.execute(
            select(ClassAttendance).where(ClassAttendance.id == attendance_id)
        )
        attendance_record = result.scalar_one_or_none()

        if not attendance_record:
            raise HTTPException(
                status_code=404, detail="Attendance record not found")

        attendance_record.status = attendance_status
        await db.commit()
        await db.refresh(attendance_record)
        return attendance_record

    async def delete_attendance(self, db: AsyncSession, attendance_id: UUID) -> ClassAttendance:
        result = await db.execute(
            select(ClassAttendance).where(ClassAttendance.id == attendance_id)
        )
        attendance_record = result.scalar_one_or_none()

        if not attendance_record:
            raise HTTPException(status_code=404, detail="Attendance record not found")

        await db.delete(attendance_record)
        await db.commit()
        return attendance_record

