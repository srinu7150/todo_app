"""
Authentication module for user registration and login
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import get_settings
from database.config import get_db
from database.models import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash from a plain password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(db, username: str, password: str):
    """Authenticate user by username and password"""
    from sqlalchemy.orm import Session
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def register_user(db, username: str, email: str, password: str) -> dict:
    """Register a new user"""
    from sqlalchemy.orm import Session
    
    # Check if username already exists
    existing_user = db.query(User).filter(
        User.username == username
    ).first()
    
    if existing_user:
        raise ValueError(f"Username '{username}' already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(
        User.email == email
    ).first()
    
    if existing_email:
        raise ValueError(f"Email '{email}' already exists")
    
    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        },
        "access_token": create_access_token(
            data={"sub": str(new_user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    }


async def get_current_user(db, token: str):
    """Get current user from JWT token"""
    from sqlalchemy.orm import Session
    
    credentials_exception = {
        "detail": "Could not validate credentials"
    }
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = {"id": user_id}
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    
    return user
