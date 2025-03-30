from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from app.workers.celery_app import REDIS_URL

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI App")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "secret")
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_PORT: int = os.getenv("MAIL_PORT", 587)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = REDIS_URL
    DOMAIN: str = os.getenv("DOMAIN")

    class Config:
        env_file = ".env"  # Load from .env file
        env_file_encoding = "utf-8"


# Create an instance of settings
settings = Settings()
