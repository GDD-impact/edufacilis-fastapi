from enum import Enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from app.core.database import Base
from app.api.v1.teacher.models import Teacher  # Ensure the Teacher model has the correct reverse relationships

# Enum for class types
class ClassType(str, Enum):
    NURSERY = "nursery"
    PRIMARY = "primary"
    JUNIOR_SECONDARY = "junior_secondary"
    SENIOR_SECONDARY = "senior_secondary"

# Enum for learning path
class LearningPath(str, Enum):
    SCIENCE = "science"
    ART = "art"
    GENERAL_STUDIES = "general_studies"

class SubjectTeachersClass(Base):
    """
    Represents a specific subject assigned to a teacher in a particular class.
    """
    __tablename__ = "subject_teachers_classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    class_name = Column(String, nullable=False)
    class_type = Column(String, nullable=False, default=ClassType.JUNIOR_SECONDARY.value)
    academic_session = Column(String, nullable=False)
    subject_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # ✅ One-to-Many Relationship with Teacher
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)
    teacher = relationship("Teacher", back_populates="subject_teachers_classes")


    # ✅ One-to-Many Relationship with Students
    students = relationship("Student", back_populates="subject_teachers_class", cascade="all, delete-orphan")


class TeachersClass(Base):
    """
    Represents a class assigned to a teacher (not subject-specific).
    """
    __tablename__ = "teachers_classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    class_name = Column(String, nullable=False)
    class_type = Column(String, nullable=False, default=ClassType.JUNIOR_SECONDARY.value)
    academic_session = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # ✅ One-to-One Relationship with Teacher
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), unique=True, nullable=False)
    teacher = relationship("Teacher", back_populates="teachers_class", uselist=False)

    # ✅ One-to-Many Relationship with Students
    students = relationship("Student", back_populates="teachers_class", cascade="all, delete-orphan")


class Student(Base):
    """
    Represents a student assigned to a subject class.
    """
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    dob = Column(DateTime, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    learning_path = Column(String, nullable=False, default=LearningPath.GENERAL_STUDIES.value)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # ✅ Added relationship to `SubjectTeachersClass`
    subject_teachers_class_id = Column(UUID(as_uuid=True), ForeignKey("subject_teachers_classes.id"))
    subject_teachers_class = relationship("SubjectTeachersClass", back_populates="students")

    # ✅ Added relationship to `TeachersClass`
    teachers_class_id = Column(UUID(as_uuid=True), ForeignKey("teachers_classes.id"), nullable=True)
    teachers_class = relationship("TeachersClass", back_populates="students")
