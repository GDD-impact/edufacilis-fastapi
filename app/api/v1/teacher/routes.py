from fastapi import APIRouter

teacher_router = APIRouter()

@teacher_router.get("/")
def get_teachers():
    return {"Hello": "Teachers"}