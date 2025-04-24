from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.schemas.schemas import UserModel
from app.core.database import async_get_db
from typing import List, Optional
from uuid import UUID
from ..schemas import (
    CreateTeacherMainClassModel,
    CreateTeacherSubjectClassModel,
    SubjectTeachersClassModel,
    TeachersClassModel,
    StudentModel,
    CreateStudentModel,
    UpdateStudentModel
)

from app.api.v1.auth.dependencies import (
    RoleChecker,
)