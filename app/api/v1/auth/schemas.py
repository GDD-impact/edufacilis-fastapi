import uuid
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime


class Role(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    role: Role = Role.STUDENT

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
                "role": "student",
            }
        }
    }


class OauthUserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: str = Field(max_length=40)
    is_verified: bool = False
    is_oauth: bool = False
    avatar: Optional[str] = None


class UserResponseModel(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr  # Ensures email validation
    phone: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    role: Role = Role.STUDENT

    class Config:
        json_encoders = {uuid.UUID: str}



class UserModel(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr  # Ensures email validation
    phone: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    password_hash: str = Field(exclude=True)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    role: Role = Role.STUDENT
    is_verified: bool = False
    two_factor_enabled: bool = False
    is_oauth: bool = False
    created_at: datetime

    class Config:
        json_encoders = {uuid.UUID: str}
        from_attributes = True  # Enables ORM compatibility for SQLAlchemy integration


class UserUpdateModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Ensures email validation
    phone: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        from_attributes = True


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
