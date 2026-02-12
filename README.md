Lead Management System
A production-ready full-stack lead management application with dual authentication methods, role-based access control, and automated email workflows.
Overview
Lead Management System is a comprehensive CRM solution designed to streamline customer relationship management. Built with modern web technologies, it provides enterprises and small businesses with tools to efficiently track, manage, and convert leads through an intuitive interface.

Key Features

Authentication & Security

Dual authentication system supporting traditional email/password and Google OAuth 2.0
JWT-based session management with configurable token expiration
Password encryption using bcrypt hashing
Role-based access control with admin and user permission levels

User Management

Administrative dashboard for user creation and management
Automated email-based user onboarding workflow
Self-service password reset functionality
User profile management capabilities

Lead Management

Complete CRUD operations for lead records
Customizable lead status tracking (New, Contacted, Qualified, Closed)
Per-user lead isolation with admin override
Contact information management including company details and notes

Communication

Gmail SMTP integration for transactional emails
Automated password reset email delivery
Professional HTML email templates
Reliable email delivery with error handling

User Interface

Responsive single-page application design
Modern gradient-based visual design
Real-time form validation
Optimized for desktop and mobile devices


Technical Architecture

Backend Stack

FastAPI: High-performance Python web framework
SQLAlchemy: Object-relational mapping layer
SQLite: Embedded relational database
Authlib: OAuth 2.0 implementation
Passlib: Cryptographic password hashing
Python-JOSE: JSON Web Token handling

Frontend Stack

HTML5: Semantic markup structure
CSS3: Custom styling with gradient themes
Vanilla JavaScript: No framework dependencies
Fetch API: RESTful backend communication

Security & Authentication

JWT tokens with configurable expiration
Bcrypt password hashing (12 rounds)
OAuth 2.0 authorization code flow
Session management via secure cookies
CORS configuration for cross-origin requests

Installation Guide

Prerequisites

Python 3.11 or higher
Conda package manager
Git version control
Gmail account with App Password enabled
Google Cloud Console project with OAuth credentials

Step 1: Clone Repository
bashgit clone https://github.com/YOUR_USERNAME/lead-management-system.git
cd lead-management-system
Step 2: Environment Setup
bashconda create -n lead_management python=3.11 -y
conda activate lead_management
Step 3: Install Dependencies
bashpip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart email-validator authlib httpx itsdangerous
Step 4: Environment Configuration
Create a .env file in the project root:
env# Database Configuration
DATABASE_URL=sqlite:///./lead_management.db

# Security Settings
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-character-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Lead Management System

# Application URLs
FRONTEND_URL=http://localhost:3000/frontend.html
API_URL=http://localhost:8000

# Google OAuth Credentials
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
Step 5: Launch Application
Start the backend server (Terminal 1):
bashpython -m uvicorn app.main:app --reload
Start the frontend server (Terminal 2):
bashpython -m http.server 3000
```

**Step 6: Access Application**

Navigate to `http://localhost:3000/frontend.html` in your web browser.

Default administrator credentials:
- Email: admin@example.com
- Password: admin123

Note: Change the default admin password immediately after first login.

## Project Structure
```text
lead_management_system/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── leads.py           # Lead management endpoints
│   │   └── dependencies.py    # Shared dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   └── security.py        # Security utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User database model
│   │   ├── lead.py            # Lead database model
│   │   └── reset_token.py     # Password reset token model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # User validation schemas
│   │   └── lead.py            # Lead validation schemas
│   └── services/
│       ├── __init__.py
│       ├── email.py           # Email delivery service
│       └── google_auth.py     # Google OAuth integration
├── frontend.html               # Single-page application
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file


Configuration Details
Google OAuth Setup

Navigate to the Google Cloud Console at console.cloud.google.com
Create a new project or select an existing one
Navigate to "APIs & Services" and click "Enable APIs and Services"
Search for and enable the "Google+ API"
Go to "Credentials" and click "Create Credentials"
Select "OAuth client ID" and choose "Web application"
Add authorized redirect URI: http://localhost:8000/auth/google/callback
Copy the Client ID and Client Secret to your .env file

Gmail SMTP Configuration

Enable Two-Factor Authentication on your Google Account
Visit myaccount.google.com/apppasswords
Select "Mail" as the app and "Other" as the device
Generate and copy the 16-character password
Add the password to your .env file without spaces

Security Considerations

Generate a cryptographically secure random string for SECRET_KEY
Never commit the .env file to version control
Rotate OAuth credentials periodically
Use HTTPS in production deployments
Implement rate limiting for authentication endpoints

API Documentation
Once the application is running, interactive API documentation is available at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

Available Endpoints
Authentication:

POST /auth/login - Email/password authentication
POST /auth/set-password - Complete user registration
GET /auth/me - Retrieve current user information
GET /auth/google/login - Initiate Google OAuth flow
GET /auth/google/callback - Handle OAuth callback

User Management (Admin only):

POST /users/ - Create new user
GET /users/ - List all users
GET /users/{id} - Retrieve specific user
PATCH /users/me - Update current user profile
DELETE /users/{id} - Delete user

Lead Management:

POST /leads/ - Create new lead
GET /leads/ - List leads (filtered by ownership)
GET /leads/{id} - Retrieve specific lead
PATCH /leads/{id} - Update lead information
DELETE /leads/{id} - Delete lead

Development Workflow
Database Migrations
The application automatically creates database tables on startup. To reset the database:
bashrm lead_management.db
python -m uvicorn app.main:app --reload
Adding New Features

Define new database models in app/models/
Create corresponding Pydantic schemas in app/schemas/
Implement business logic in app/services/
Add API endpoints in app/api/
Update frontend.html with new UI components

Testing
Manual testing via Swagger UI at http://localhost:8000/docs
Deployment Recommendations
Production Checklist

Replace SQLite with PostgreSQL or MySQL
Implement proper logging and monitoring
Configure HTTPS with SSL/TLS certificates
Set up automated backups
Implement rate limiting and request throttling
Use environment-specific configuration files
Deploy behind a reverse proxy (nginx/Apache)
Set up CI/CD pipeline for automated deployments

Recommended Hosting Platforms

Backend: Heroku, AWS EC2, DigitalOcean, Google Cloud Run
Frontend: Netlify, Vercel, AWS S3 + CloudFront
Database: AWS RDS, Google Cloud SQL, DigitalOcean Managed Databases

Troubleshooting
Common Issues
Issue: Email not sending

Verify Gmail App Password is correct and has no spaces
Ensure 2FA is enabled on Google Account
Check SMTP settings in .env file

Issue: Google OAuth failing

Confirm redirect URI matches exactly in Google Console
Verify OAuth credentials are correctly set in .env
Check that Google+ API is enabled

Issue: Database errors

Delete lead_management.db and restart application
Check file permissions in project directory

Contributing
Contributions are welcome. Please follow these guidelines:

Fork the repository
Create a feature branch
Make your changes with clear commit messages
Submit a pull request with detailed description

License
This project is licensed under the MIT License. See LICENSE file for details.

Author
Komal Sharma

Acknowledgments
Built with FastAPI, SQLAlchemy, and modern web technologies.