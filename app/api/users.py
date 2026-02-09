from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.reset_token import PasswordResetToken
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.dependencies import get_current_admin, get_current_user
from app.services.email import send_password_reset_email

router = APIRouter(prefix="/users", tags=["User Management"])

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin creates a new user
    
    Flow:
    1. Admin creates user with just email
    2. Generate password reset token
    3. Send email with reset link
    4. User clicks link to set password and complete profile
    
    Requires: Admin privileges
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user (inactive until password is set)
    new_user = User(
        email=user_data.email,
        is_admin=user_data.is_admin,
        is_active=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate password reset token
    reset_token = PasswordResetToken(
        token=PasswordResetToken.generate_token(),
        user_id=new_user.id,
        expires_at=PasswordResetToken.get_expiry_time()
    )
    db.add(reset_token)
    db.commit()
    
    # Send email with reset link
    email_sent = send_password_reset_email(new_user.email, reset_token.token)
    
    if not email_sent:
        print(f"⚠️ Warning: User created but email failed to send")
    
    return new_user

@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = 0,
    limit: int = 100
):
    """List all users (Admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get specific user by ID (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile"""
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name
    if user_data.phone is not None:
        current_user.phone = user_data.phone
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.email} deleted successfully"}