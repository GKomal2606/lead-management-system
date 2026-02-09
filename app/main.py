from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import init_db, get_db
from app.models import User
from app.core.security import get_password_hash
from app.api import auth, leads, users
from app.core.config import settings

app = FastAPI(title="Lead Management System API")

# Session middleware (MUST be added before OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(users.router)

@app.on_event("startup")
def startup_event():
    # Initialize database
    init_db()
    
    # Create default admin user if not exists
    db = next(get_db())
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("Default admin user created: admin@example.com / admin123")

@app.get("/")
def root():
    return {
        "message": "Lead Management System API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}