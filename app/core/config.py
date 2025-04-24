from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from app.workers.celery_app import REDIS_URL

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = REDIS_URL

    # App settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI App")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    DOMAIN: str = os.getenv("DOMAIN")

    # Auth Settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "secret")
    ACCESS_TOKEN_EXPIRY: int = int(os.getenv("ACCESS_TOKEN_EXPIRY", 172800))
    REFRESH_TOKEN_EXPIRY: int = int(os.getenv("REFRESH_TOKEN_EXPIRY", 604800))

    # Mail and Resend Settings
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    RESEND_MAIL_FROM: str = os.getenv("RESEND_MAIL_FROM")

    # Oauth Secrets
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URL : str = os.getenv("GOOGLE_REDIRECT_URL", "http://localhost:8000/api/v1/auth/callback/google")

    class Config:
        env_file = ".env"  # Load from .env file
        env_file_encoding = "utf-8"


# Create an instance of settings
settings = Settings()
