from fastapi import APIRouter
from app.api.v1.teacher.routes import teacher_router
from app.api.v1.student.routes import student_router
from app.workers.routes import schedule_router

router = APIRouter()

# Include other routers
router.include_router(teacher_router, prefix="/teacher", tags=["Teacher"])
router.include_router(student_router, prefix="/student", tags=["Student"])
router.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])