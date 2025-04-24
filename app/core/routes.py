from fastapi import APIRouter
from app.api.v1.teacher.routes import teacher_router
from app.api.v1.student.routes import student_router
from app.workers.routes import schedule_router
from app.api.v1.auth.routes.oauth_routes import oauth_router
from app.api.v1.auth.routes.routes import auth_router
from app.api.v1.auth.routes.user_routes import user_router
from app.api.v1.auth.routes.two_factor_routes import twoFA_router
from app.core.templates import email_preview_router

router = APIRouter()

# Include other routers
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(twoFA_router, prefix="/auth", tags=["authentication (2FA)"])
router.include_router(oauth_router, prefix="/auth", tags=["authentication (oauth)"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(teacher_router, prefix="/teacher", tags=["Teacher"])
router.include_router(student_router, prefix="/student", tags=["Student"])

# email preview router
router.include_router(email_preview_router, prefix="/preview/email", tags=["email preview"])

router.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])