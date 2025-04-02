from sqlalchemy import Column, Boolean, ForeignKey, DateTime, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from app.core.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # ✅ One-to-One Relationship with User (User can be either a Teacher or Student)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="teacher", uselist=False)

    # ✅ Store `classes` and `subjects` as JSON lists (Array-like storage)
    classes = Column(JSON, nullable=False, default=[])
    subjects = Column(JSON, nullable=False, default=[])

    school = Column(String, nullable=False)
    school_location = Column(String, nullable=False)
    
    is_form_teacher = Column(Boolean, default=False)
    my_class = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # ✅ Reverse Relationships
    subject_teachers_classes = relationship("SubjectTeachersClass", back_populates="teacher")
    teachers_class = relationship("TeachersClass", back_populates="teacher", uselist=False)
