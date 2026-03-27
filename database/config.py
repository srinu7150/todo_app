"""
Database configuration and connection setup
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings

settings = get_settings()

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG  # Set to True for SQL query logging in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base (for declarative models)
Base = declarative_base()


def get_db():
    """
    Get database session dependency for FastAPI routes
    
    Usage:
        def get_todos(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables
    Call this after database creation but before running the app
    """
    from database.models import User, Todo
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
