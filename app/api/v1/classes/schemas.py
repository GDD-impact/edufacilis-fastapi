from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from uuid import UUID

# ✅ SubjectTeachersClass Pydantic Model
class SubjectTeachersClassModel(BaseModel):
    id: UUID
    class_name: str
    class_type: str
    academic_session: str
    subject_name: str
    created_at: datetime
    teacher_id: UUID

    # ✅ Convert UUID to String
    @field_serializer("id", "teacher_id")
    def serialize_uuid(self, value: UUID) -> str:
        return str(value)

    # ✅ Convert Datetime to ISO 8601 String
    @field_serializer("created_at")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    class Config:
        from_attributes = True


# ✅ TeachersClass Pydantic Model
class TeachersClassModel(BaseModel):
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


# ✅ Student Pydantic Model
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
