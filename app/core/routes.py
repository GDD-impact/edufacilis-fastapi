from fastapi import APIRouter
from app.api.v1.teacher.routes import teachers_router
from app.api.v1.student.routes import student_router
from app.workers.routes import schedule_router
from app.api.v1.auth.routes.oauth_routes import oauth_router
from app.api.v1.auth.routes.routes import auth_router
from app.api.v1.auth.routes.user_routes import user_router
from app.api.v1.auth.routes.two_factor_routes import twoFA_router
from app.core.templates import email_preview_router
from app.api.v1.media.routes import file_router
from app.api.v1.classes.routes.routes import class_router

router = APIRouter()

# Include other routers
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(twoFA_router, prefix="/auth", tags=["authentication (2FA)"])
router.include_router(oauth_router, prefix="/auth", tags=["authentication (oauth)"])

# user router and profile router
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(teachers_router, prefix="/teacher", tags=["Teacher"])
router.include_router(student_router, prefix="/student", tags=["Student"])

# class router
router.include_router(class_router, prefix="/class", tags=["Class"])

# email preview router
router.include_router(email_preview_router, prefix="/preview/email", tags=["email preview"])

# file upload router
router.include_router(file_router, prefix="/file", tags=["file handler"])

# periodic task router
router.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])