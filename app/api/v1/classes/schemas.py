from pydantic import BaseModel, Field, field_serializer, UUID4
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.api.v1.classes.models import AttendanceStatus, ClassType, LearningPath


# --------------------------------------------------------
# ✅ Student Pydantic Model
# --------------------------------------------------------
class StudentModel(BaseModel):
    id: UUID
    firstname: str
    lastname: str
    gender: str
    phone_number: Optional[str] = None
    dob: Optional[datetime] = None
    email: Optional[str] = None
    address: Optional[str] = None
    learning_path: str
    created_at: datetime
    subject_teachers_class_id: Optional[UUID] = None
    teachers_class_id: Optional[UUID] = None

    @field_serializer("id", "subject_teachers_class_id", "teachers_class_id")
    def serialize_uuid(self, value: Optional[UUID]) -> Optional[str]:
        return str(value) if value else None

    @field_serializer("created_at", "dob")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


class CreateStudentModel(BaseModel):
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    gender: str
    parent_phone_number: Optional[str] = None
    dob: Optional[datetime] = None
    parent_email: Optional[str] = None
    address: Optional[str] = None
    learning_path: LearningPath = Field(..., example="general_studies")
    subject_teachers_class_id: Optional[UUID] = Field(
        ..., example="123e4567-e89b-12d3-a456-426614174000")
    teachers_class_id: Optional[UUID] = Field(
        ..., example="123e4567-e89b-12d3-a456-426614174000")


class UpdateStudentModel(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    gender: Optional[str]
    parent_phone_number: Optional[str]
    dob: Optional[datetime]
    parent_email: Optional[str]
    address: Optional[str]
    learning_path: Optional[str]
    subject_teachers_class_id: Optional[UUID]
    teachers_class_id: Optional[UUID]


# --------------------------------------------------------
# 🔁 Shared fields for any teacher class
# --------------------------------------------------------
class BaseTeacherClassModel(BaseModel):
    id: UUID
    class_name: str
    class_type: str
    academic_session: str
    created_at: datetime
    teacher_id: UUID

    @field_serializer("id", "teacher_id")
    def serialize_uuid(self, value: UUID) -> str:
        return str(value)

    @field_serializer("created_at")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    class Config:
        from_attributes = True


# --------------------------------------------------------
# Specific to SubjectTeachersClass
# --------------------------------------------------------
class SubjectTeachersClassModel(BaseTeacherClassModel):
    subject_name: str


class SubjectTeachersClassWithStudentsModel(BaseTeacherClassModel):
    subject_name: str
    students: List[StudentModel] = []

# General Teachers Class (no subject_name field)


class TeachersClassModel(BaseTeacherClassModel):
    pass


class TeachersClassWithStudentsModel(BaseTeacherClassModel):
    students: List[StudentModel] = []


# Creation Model for SubjectTeachersClass
class CreateTeacherSubjectClassModel(BaseModel):
    class_name: str = Field(..., example="Mathematics 101")
    class_type: ClassType = Field(..., example="junior_secondary")
    academic_session: str = Field(..., example="2023/2024")
    subject_name: str = Field(..., example="Mathematics")
    teacher_id: UUID = Field(...,
                             example="123e4567-e89b-12d3-a456-426614174000")


# Creation Model for TeachersClass
class CreateTeacherMainClassModel(BaseModel):
    class_name: str = Field(..., example="Mathematics 101")
    class_type: ClassType = Field(..., example="junior_secondary")
    academic_session: str = Field(..., example="2023/2024")
    teacher_id: UUID = Field(...,
                             example="123e4567-e89b-12d3-a456-426614174000")


# --------------------------------------------------------
# ClassAttendance Pydantic Model
# --------------------------------------------------------

# Base fields for ClassAttendance
class ClassAttendanceBase(BaseModel):
    date: datetime
    status: str
    student_id: UUID4
    teachers_class_id: UUID4

# Schema for creating new ClassAttendance record


class ClassAttendanceCreate(ClassAttendanceBase):
    pass

# Schema for updating ClassAttendance record


class ClassAttendanceUpdate(BaseModel):
    status: AttendanceStatus = Field(..., example="present")

# Schema for responding with ClassAttendance details


class ClassAttendanceResponse(ClassAttendanceBase):
    id: UUID4

    @field_serializer("id", "student_id", "teachers_class_id")
    def serialize_uuid(self, value: UUID) -> str:
        return str(value)

    @field_serializer("date")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()

    class Config:
        from_attributes = True


class BulkUpdateAttendanceStatus(BaseModel):
    attendance_id: List[ClassAttendanceResponse]
    status: AttendanceStatus = Field(..., example="present")
