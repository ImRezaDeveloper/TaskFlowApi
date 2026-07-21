# src/taskflow/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "dev-secret-change-me"
    REFRESH_SECRET_KEY: str = "dev-refresh-secret-change-me"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20

    # Database
    DB_NAME: str = "TaskFlow_DB"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "rezapapi1384"
    DB_PORT: int = 5433
    DB_HOST: str = "localhost"

    # App
    PORT: int = 8000
    PROJECT_NAME: str = "TASK_MANAGEMENT_API"

    # LOGS
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"