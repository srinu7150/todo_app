"""
Configuration settings for the Todo Application
"""
import os
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://admin:admin123@localhost:5432/todo_db"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "admin"
    DATABASE_PASSWORD: str = "admin123"
    DATABASE_NAME: str = "todo_db"
    
    # Application Settings
    APP_NAME: str = "Todo App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @classmethod
    def create(cls):
        """Create settings instance from environment variables"""
        cls.DATABASE_URL = os.getenv("DATABASE_URL", cls.DATABASE_URL)
        cls.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        cls.SECRET_KEY = os.getenv("SECRET_KEY", cls.SECRET_KEY)
        return cls()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings.create()
