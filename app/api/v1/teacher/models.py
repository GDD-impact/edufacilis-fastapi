from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    Firstname = Column(String, nullable=False)
    Surname = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete-orphan")
    classes = relationship("Class", back_populates="teacher", cascade="all, delete-orphan")
    school = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_form_teacher = Column(Boolean, default=False)
    my_class = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=True)