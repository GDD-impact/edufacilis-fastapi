from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# Enum for user roles
class Role(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    role = Column(String, nullable=False, default=Role.STUDENT.value)
    email_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    is_oauth = Column(Boolean, default=False)

    # Relationship with verification tokens
    verification_tokens = relationship("VerificationToken", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")

class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, nullable=False)
    expires_at = Column(String, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    

    user_rel = relationship("User", back_populates="verification_tokens", foreign_keys=[user])

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, nullable=False)
    expires_at = Column(String, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    

    user_rel = relationship("User", back_populates="password_reset_tokens", foreign_keys=[user])

class ActivityType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    activity_type = Column(String, nullable=False, default=ActivityType.CREATE.value)
    created_at = Column(String, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


    user_rel = relationship("User", back_populates="activities", foreign_keys=[user])







