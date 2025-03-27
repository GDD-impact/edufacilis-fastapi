from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import router as main_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
version = settings.VERSION
version_prefix =f"/api/{version}"
app.include_router(main_router, prefix=version_prefix)


