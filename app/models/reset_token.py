from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.core.database import Base
import secrets

class PasswordResetToken(Base):
    """
    Token model for password reset functionality
    Tokens expire after 24 hours
    """
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Token validity
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="reset_tokens")
    
    @staticmethod
    def generate_token() -> str:
        """
        Generate a secure random token
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_expiry_time() -> datetime:
        """
        Get token expiration time (24 hours from now)
        """
        return datetime.utcnow() + timedelta(hours=24)
    
    def is_valid(self) -> bool:
        """
        Check if token is still valid (not expired and not used)
        """
        return not self.is_used and datetime.utcnow() < self.expires_at