from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete-orphan")
    classes = relationship("Class", back_populates="teacher", cascade="all, delete-orphan")
    school = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_form_teacher = Column(Boolean, default=False)
    my_class = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=True)