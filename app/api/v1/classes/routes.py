from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.schemas.schemas import UserModel
from app.core.database import async_get_db
from typing import List, Optional
from uuid import UUID
from .schemas import (
    CreateTeacherMainClassModel,
    CreateTeacherSubjectClassModel,
    SubjectTeachersClassModel,
    TeachersClassModel,
    StudentModel,
    CreateStudentModel,
    UpdateStudentModel
)

from app.api.v1.auth.dependencies import (
    RoleChecker,
    get_current_user,
)

from .services.class_services import (
    MainClassService,
    SubjectClassService,
)
from .services.students_service import ClassStudentsService


class_router = APIRouter()

main_class_service = MainClassService()
subject_class_service = SubjectClassService()
class_students_service = ClassStudentsService()
role_checker = RoleChecker(["admin", "teacher"])

# --------------------------------------------------------------
# Main Classes router
# --------------------------------------------------------------


@class_router.get("/main-classes", response_model=List[TeachersClassModel])
async def get_all_main_classes(
        skip: int = 0,
        limit: int = 100,
        _: UserModel = Depends(role_checker),
        db: AsyncSession = Depends(async_get_db)):
    """
    Get all main classes created by a teacher.
    """
    return await main_class_service.get_all_main_classes(skip, limit, db)


@class_router.get("/teacher/{teacher_id}/main-classes", response_model=List[TeachersClassModel])
async def get_teacher_main_classes(teacher_id: UUID, _: UserModel = Depends(role_checker), db: AsyncSession = Depends(async_get_db)):
    """
    Get main classes created by a teacher.
    """
    return await main_class_service.get_teacher_main_class(teacher_id, db)


@class_router.get("/main-classes/{class_id}", response_model=Optional[TeachersClassModel])
async def get_teacher_main_class_by_id(class_id: UUID, _: UserModel = Depends(role_checker), db: AsyncSession = Depends(async_get_db)):
    """
    Get a specific main class by ID.
    """
    return await main_class_service.get_teacher_main_class_by_id(class_id, db)


@class_router.post("/main-classes", response_model=TeachersClassModel)
async def create_teacher_main_class(
    details: CreateTeacherMainClassModel,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Create a new main class for a teacher.
    """
    return await main_class_service.create_teacher_main_class(details, db)


@class_router.put("/main-classes/{class_id}", response_model=TeachersClassModel)
async def update_teacher_main_class(
    class_id: UUID,
    details: CreateTeacherMainClassModel,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Update a specific main class.
    """
    return await main_class_service.update_teacher_main_class(class_id, details, db)


@class_router.get("/check-main-class-exists", response_model=bool)
async def check_main_class_exists(
    class_type: str,
    class_name: str,
    academic_session: str,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Check if a main class exists based on class_type, class_name, and academic_session.
    """
    return await main_class_service.check_main_class_exists(class_type, class_name, academic_session, db)


# --------------------------------------------------------------
# Subject Classes router
# --------------------------------------------------------------

@class_router.get("/subject-classes", response_model=List[SubjectTeachersClassModel])
async def get_all_subject_classes(skip: int = 0, limit: int = 100, _: UserModel = Depends(role_checker), db: AsyncSession = Depends(async_get_db)):
    """
    Get all subject classes created by a teacher.
    """
    return await subject_class_service.get_all_subject_classes(skip, limit, db)


@class_router.get("/teacher/{teacher_id}/subject-classes", response_model=List[SubjectTeachersClassModel])
async def get_teacher_subject_classes(
    teacher_id: UUID, skip: int = 0, limit: int = 100, _: UserModel = Depends(role_checker), db: AsyncSession = Depends(async_get_db)
):
    """
    Get all subject classes created by a teacher.
    """
    return await subject_class_service.get_all_teachers_sub_classes(teacher_id, skip, limit, db)


@class_router.get("/subject-classes/{class_id}", response_model=Optional[SubjectTeachersClassModel])
async def get_teacher_subject_class_by_id(class_id: UUID, _: UserModel = Depends(role_checker), db: AsyncSession = Depends(async_get_db)):
    """
    Get a specific subject class by ID.
    """
    return await subject_class_service.get_teacher_sub_class_by_id(class_id, db)


@class_router.post("/subject-classes", response_model=SubjectTeachersClassModel)
async def create_teacher_subject_class(
    details: CreateTeacherSubjectClassModel,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Create a new subject class for a teacher.
    """
    return await subject_class_service.create_teacher_sub_class(details, db)


@class_router.put("/subject-classes/{class_id}", response_model=SubjectTeachersClassModel)
async def update_teacher_subject_class(
    class_id: UUID,
    details: CreateTeacherSubjectClassModel,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Update a specific subject class.
    """
    return await subject_class_service.update_teacher_sub_class(class_id, details, db)


@class_router.get("/check-sub-class-exists", response_model=bool)
async def check_subject_class_exists(
    class_type: str,
    class_name: str,
    academic_session: str,
    subject_name: str,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Check if a subject class exists based on class_type, class_name, subject_name, and academic_session.
    """
    return await subject_class_service.check_sub_class_exists(
        class_type, class_name, academic_session, subject_name, db
    )

# --------------------------------------------------------------
# Students router
# --------------------------------------------------------------


@class_router.post("/students", response_model=StudentModel)
async def create_student(
    student: CreateStudentModel,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Create a new student and add them to a class.
    """
    return await class_students_service.create_student(student, db)


@class_router.put("/students/{student_id}", response_model=StudentModel)
async def update_student(
    student_id: UUID,
    updated_data: UpdateStudentModel,  # Model containing optional fields for update
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Update an existing student's details including their class.
    """
    return await class_students_service.update_student(student_id, updated_data, db)


@class_router.delete("/students/{student_id}", status_code=204)
async def delete_student(
    student_id: UUID,
    _: UserModel = Depends(role_checker),
    db: AsyncSession = Depends(async_get_db)
):
    """
    Delete a student and automatically remove them from any class.
    """
    await class_students_service.delete_student(student_id, db)
    return {"detail": "Student deleted successfully."}
