from fastapi import FastAPI
from app.api.v1.auth.errors import register_all_errors
from app.core.config import settings
from app.core.routes import router as main_router
from app.core.middleware import register_middleware

description = """
A REST API for edufacilis Web and Mobile Applications.
handle all the requests for the edufacilis Web and Mobile Applications.

"""

app = FastAPI(title=settings.PROJECT_NAME,
              description=description,
              version=settings.VERSION,
              contact={
                  "name": "Edufacilis",
                  "url": "https://edufacilis.app",
                  "email": "gddimpactsoftwares@gmail.com",
              },
              )
version_prefix = f"/api/v1"
app.include_router(main_router, prefix=version_prefix)

register_all_errors(app)
register_middleware(app)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Edufacilis API!"}
