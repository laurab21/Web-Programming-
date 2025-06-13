from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5000"]
    DATABASE_URL: str = "sqlite:///./test.db"
    PROJECT_NAME: str = "Lab5 API"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
