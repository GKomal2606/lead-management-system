from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from starlette.requests import Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models import User, PasswordResetToken
from app.schemas import UserLogin, Token, UserSetPassword, UserResponse
from app.api.dependencies import get_current_user
from app.services.google_auth import oauth

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login endpoint - returns JWT token
    
    1. Find user by email
    2. Verify password
    3. Create and return JWT token
    """
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not user.hashed_password or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account not activated. Please set your password first."
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/set-password", response_model=UserResponse)
def set_password(data: UserSetPassword, db: Session = Depends(get_db)):
    """
    Set password for new user using reset token
    
    1. Validate token
    2. Set password and profile info
    3. Activate user account
    """
    # Find valid token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == data.token
    ).first()
    
    if not token_record or not token_record.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Get user
    user = token_record.user
    
    # Set password and profile info
    user.hashed_password = get_password_hash(data.password)
    user.full_name = data.full_name
    user.phone = data.phone
    user.is_active = True
    
    # Mark token as used
    token_record.is_used = True
    
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current logged-in user's information
    Requires valid JWT token
    """
    return current_user

@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirect to Google OAuth login
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Google OAuth callback - creates or logs in user
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        email = user_info.get('email')
        name = user_info.get('name')
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                full_name=name,
                is_active=True,  # Auto-activate Google users
                is_admin=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, 
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        frontend_url = f"{settings.FRONTEND_URL}?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {str(e)}"
        )