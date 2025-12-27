"""Pydantic models and schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# =============================================================================
# Auth Schemas
# =============================================================================

class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (safe to return to client)."""
    id: str
    email: str
    created_at: Optional[datetime] = None


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    user: UserResponse
    access_token: str
    refresh_token: Optional[str] = None
    message: str = "Success"


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True


# =============================================================================
# Task Schemas (for Phase 3)
# =============================================================================

class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    attachment_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

