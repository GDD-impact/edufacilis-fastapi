from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.schemas.schemas import UserModel
from app.api.v1.classes.services.attendance_service import ClassAttendanceService
from app.core.database import async_get_db
from typing import List, Optional
from uuid import UUID
from ..schemas import BulkUpdateAttendanceStatus, ClassAttendanceUpdate, ClassAttendanceResponse

from app.api.v1.auth.dependencies import (
    RoleChecker,
)


attendance_router = APIRouter()
attendance_service = ClassAttendanceService()
role_checker = RoleChecker(["admin", "teacher"])

# --------------------------------------------------------------
# Class Attendance router
# --------------------------------------------------------------


@attendance_router.get("/student/{student_id}/{class_id}", response_model=List[ClassAttendanceResponse])
async def get_attendance_for_student(
    student_id: UUID,
    class_id: UUID,
    db: AsyncSession = Depends(async_get_db),
    _: UserModel = Depends(role_checker)
):
    """
    Fetch all attendance records for a specific student in a class.
    """
    return await attendance_service.get_attendance_by_student(db, student_id, class_id)


@attendance_router.get("/class/{class_id}/date/{date}", response_model=List[ClassAttendanceResponse])
async def get_attendance_by_date_and_class(
    class_id: UUID,
    date: datetime,
    db: AsyncSession = Depends(async_get_db),
    _: UserModel = Depends(role_checker)
):
    """
    Fetch attendance records for a specific date and class or create a new attendance record if it doesn't exist.
    """
    attendance_record = await attendance_service.get_attendance_by_date_and_class(db, date, class_id)
    if not attendance_record:
        new_attendance_record = await attendance_service.create_class_attendance(db, class_id, date)
        return new_attendance_record
    return attendance_record


@attendance_router.patch("/update/{attendance_id}", response_model=ClassAttendanceResponse)
async def update_attendance_status(
    attendance_id: UUID,
    payload: ClassAttendanceUpdate,
    db: AsyncSession = Depends(async_get_db),
    _: UserModel = Depends(role_checker)
):
    """
    Update the status (e.g., present, absent) for an attendance record.
    """
    return await attendance_service.update_attendance(db, attendance_id, payload.status)


@attendance_router.patch("/bulk-update", response_model=List[ClassAttendanceResponse])
async def bulk_update_attendance_status(
    payload: BulkUpdateAttendanceStatus,
    db: AsyncSession = Depends(async_get_db),
    _: UserModel = Depends(role_checker)
):
    """
    Bulk update the status (e.g., present, absent) for multiple attendance records.
    """
    updated_records = []
    for attendance in payload.attendance_id:
        updated_record = await attendance_service.update_attendance(db, attendance.id, attendance.status)
        updated_records.append(updated_record)
    return updated_records


@attendance_router.delete("/delete/{attendance_id}", response_model=ClassAttendanceResponse)
async def delete_attendance_record(
    attendance_id: UUID,
    db: AsyncSession = Depends(async_get_db),
    _: UserModel = Depends(role_checker)
):
    """
    Delete a specific attendance record.
    """
    return await attendance_service.delete_attendance(db, attendance_id)
