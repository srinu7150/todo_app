"""
Pydantic schemas for request/response validation and serialization
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ============== User Schemas ==============

class UserBase(BaseModel):
    """Base user schema without sensitive fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=128, description="Password (8-128 characters)")


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=8, max_length=128)


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"


# ============== Todo Schemas ==============

class TodoBase(BaseModel):
    """Base todo schema without ID and timestamps"""
    title: str = Field(..., min_length=1, max_length=200, description="Todo title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating a todo (partial update)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TodoResponse(BaseModel):
    """Schema for todo response"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Response Wrappers ==============

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class SuccessResponse(BaseModel):
    """Success response wrapper"""
    success: bool
    message: str
    data: Optional[dict] = None
