from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schema for admin creating a new user
    Only email is required initially
    """
    email: EmailStr
    is_admin: bool = False

class UserSetPassword(BaseModel):
    """
    Schema for user setting their password via reset token
    """
    token: str
    password: str = Field(..., min_length=8)
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """
    Schema for updating user profile
    """
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    """
    Schema for user data in responses
    Excludes sensitive information
    """
    id: int
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models

class Token(BaseModel):
    """
    Schema for JWT token response
    """
    access_token: str
    token_type: str = "bearer"