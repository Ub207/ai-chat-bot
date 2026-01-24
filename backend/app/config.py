from pydantic_settings import BaseSettings
from typing import List, Union
from functools import lru_cache
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / "backend.env"


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # App
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"]

    class Config:
        env_file = ENV_FILE_PATH
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    # Handle comma-separated CORS origins from environment variable
    if isinstance(settings.CORS_ORIGINS, str):
        settings.CORS_ORIGINS = [origin.strip() for origin in settings.CORS_ORIGINS.split(',')]
    return settings


settings = get_settings()
