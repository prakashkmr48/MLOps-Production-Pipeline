"""Configuration Management"""
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    """Application settings"""
    MODEL_PATH: str = os.getenv("MODEL_PATH", "/app/models")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    API_VERSION: str = "v1.0.0"
    APP_NAME: str = "MLOps Production API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
