from pydantic import BaseModel,UUID4, field_serializer, model_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class TeacherBase(BaseModel):
    """Base schema for Teacher model"""
    user_id: UUID4
    classes: List[str]
    subjects: List[str]
    school: str
    school_location: str
    is_form_teacher: bool = False
    my_class: str

    @model_validator(mode="before")
    @classmethod
    def coerce_json_fields(cls, values):
        """Ensure `classes` and `subjects` are lists even if provided as a string."""
        if isinstance(values.get("classes"), str):
            values["classes"] = values["classes"].split(",")  # Convert comma-separated string to list
        if isinstance(values.get("subjects"), str):
            values["subjects"] = values["subjects"].split(",")
        return values
    

class TeacherCreate(TeacherBase):
    """Schema for creating a new Teacher"""
    pass

class TeacherResponse(TeacherBase):
    """Schema for returning Teacher details"""
    id: UUID
    created_at: datetime


    # ✅ Convert UUID to String
    @field_serializer("id")
    def serialize_uuid(self, value: UUID) -> str:
        return str(value)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        """Ensure `created_at` is returned as an ISO 8601 string"""
        return value.isoformat()
    
    class Config:
        from_attributes = True
