# 🎯 Lead Management System

A full-stack lead management application built with FastAPI and vanilla JavaScript.

## ✨ Features

- 🔐 **Dual Authentication**: Email/password and Google OAuth 2.0
- 👥 **User Management**: Admin panel for creating and managing users
- 📧 **Email Notifications**: Automated password reset emails via Gmail SMTP
- 📊 **Lead Management**: Full CRUD operations for leads
- 🔒 **Role-Based Access**: Admin and regular user permissions
- 🎨 **Modern UI**: Responsive design with gradient styling
- 🔑 **JWT Authentication**: Secure token-based sessions

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy ORM
- SQLite Database
- Authlib (OAuth)
- PassLib (Password Hashing)
- Python-JOSE (JWT)

**Frontend:**
- HTML5
- CSS3 (Custom styling)
- Vanilla JavaScript

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/lead-management-system.git
cd lead-management-system
```

2. **Create virtual environment**
```bash
conda create -n lead_management python=3.11 -y
conda activate lead_management
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart email-validator authlib httpx itsdangerous
```

4. **Configure environment variables**

Create `.env` file:
```env
DATABASE_URL=sqlite:///./lead_management.db
SECRET_KEY=your-secret-key-here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FRONTEND_URL=http://localhost:3000/frontend.html
API_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

5. **Run the application**

Terminal 1 (Backend):
```bash
python -m uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
python -m http.server 3000
```

6. **Access the application**

Open browser: `http://localhost:3000/frontend.html`

Default admin credentials:
- Email: `admin@example.com`
- Password: `admin123`

## 📁 Project Structure
```
lead_management_system/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Config, security, database
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Email, OAuth services
├── frontend.html     # Frontend UI
├── .env             # Environment variables
└── README.md
```

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/auth/google/callback`
6. Copy Client ID and Secret to `.env`

## 📧 Gmail SMTP Setup

1. Enable 2-Factor Authentication on Google Account
2. Generate App Password at [App Passwords](https://myaccount.google.com/apppasswords)
3. Add credentials to `.env`

## 🚀 Features Demo

- **Admin Panel**: Create users, manage permissions
- **Email Flow**: Automatic password reset emails
- **Google Login**: One-click authentication
- **Lead Dashboard**: Create, edit, delete leads
- **Status Tracking**: Monitor lead progress

## 👨‍💻 Author

Komal Sharma

## 📄 License

MIT License