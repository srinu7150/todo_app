"""
Main FastAPI application with Todo CRUD endpoints
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import get_settings
from database.config import get_db
from database.models import User, Todo
from app.auth import (
    authenticate_user,
    register_user,
    get_current_user,
    create_access_token
)
from app.schemas import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    MessageResponse,
    SuccessResponse
)

settings = get_settings()
router = APIRouter(prefix="/api", tags=["API"])

# OAuth2 password scheme for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ============== Authentication Endpoints ==============

@router.post("/auth/register", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (8-128 characters)
    
    Returns access token upon successful registration.
    """
    try:
        result = await register_user(db, user_data.username, user_data.email, user_data.password)
        return SuccessResponse(
            success=True,
            message=result["message"],
            data={"access_token": result.get("access_token")}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get access token
    
    - **username**: Username or email
    - **password**: User's password
    
    Returns JWT access token for authenticated requests.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email
    )


# ============== Todo CRUD Endpoints ==============

@router.get("/todos", response_model=List[TodoResponse])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all todos for the authenticated user
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **completed**: Filter by completion status (optional)
    
    Returns paginated list of user's todos.
    """
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    todos = query.offset(skip).limit(limit).all()
    return [TodoResponse(
        id=t.id,
        user_id=t.user_id,
        title=t.title,
        description=t.description,
        completed=t.completed,
        due_date=t.due_date,
        created_at=t.created_at,
        updated_at=t.updated_at
    ) for t in todos]


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific todo by ID
    
    Returns the todo if it belongs to the authenticated user.
    Raises 404 if not found or doesn't belong to user.
    """
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return TodoResponse(
        id=todo.id,
        user_id=todo.user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        due_date=todo.due_date,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo
    
    - **title**: Required todo title (1-200 characters)
    - **description**: Optional description (up to 1000 characters)
    - **due_date**: Optional due date/time
    
    Returns the created todo with all fields.
    """
    new_todo = Todo(
        user_id=current_user.id,
        title=todo_data.title,
        description=todo_data.description,
        completed=False,
        due_date=todo_data.due_date
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return TodoResponse(
        id=new_todo.id,
        user_id=new_todo.user_id,
        title=new_todo.title,
        description=new_todo.description,
        completed=new_todo.completed,
        due_date=new_todo.due_date,
        created_at=new_todo.created_at,
        updated_at=new_todo.updated_at
    )


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing todo
    
    - **todo_id**: ID of the todo to update
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **completed**: Completion status (optional)
    - **due_date**: New due date (optional)
    
    Returns the updated todo. Raises 404 if not found or doesn't belong to user.
    """
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update fields that were provided
    update_data = todo_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    
    return TodoResponse(
        id=todo.id,
        user_id=todo.user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        due_date=todo.due_date,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a todo
    
    - **todo_id**: ID of the todo to delete
    
    Returns 204 No Content on success. Raises 404 if not found or doesn't belong to user.
    """
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    db.delete(todo)
    db.commit()
    
    return {"message": "Todo deleted successfully"}


# ============== Utility Endpoints ==============

@router.get("/health", response_model=MessageResponse)
async def health_check():
    """Health check endpoint"""
    return MessageResponse(message="OK")
