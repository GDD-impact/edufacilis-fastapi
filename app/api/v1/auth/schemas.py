import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }


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
    role: str = Field(default="student")  # Default role is "student"
    is_verified: bool = False
    two_factor_enabled: bool = False
    is_oauth: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True  # Enables ORM compatibility for SQLAlchemy integration


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
