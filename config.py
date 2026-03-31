"""
Configuration settings for the Todo Application
"""
import os
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/todo_db")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_USER: str = os.getenv("DATABASE_USER", "admin")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "admin123")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "todo_db")
    
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "Todo App")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
