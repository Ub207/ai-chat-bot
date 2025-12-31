# Phase-2 Specifications - Todo Full Stack Application

## 📋 Overview
A production-ready full-stack Todo application with user authentication, built using FastAPI (backend) and Next.js (frontend), with NeonDB PostgreSQL database.

---

## 🏗️ Architecture

```
to-do-full-stack/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Settings and environment variables
│   │   ├── database.py     # Database connection and session management
│   │   ├── models/         # SQLAlchemy models
│   │   │   ├── user.py     # User model
│   │   │   └── todo.py     # Todo model
│   │   ├── schemas/        # Pydantic schemas for validation
│   │   │   ├── user.py     # User schemas
│   │   │   └── todo.py     # Todo schemas
│   │   ├── routers/        # API endpoints
│   │   │   ├── auth.py     # Authentication routes
│   │   │   └── todos.py    # Todo CRUD routes
│   │   ├── services/       # Business logic
│   │   │   ├── auth.py     # Auth service
│   │   │   └── todo.py     # Todo service
│   │   └── utils/          # Utility functions
│   │       └── security.py # Password hashing, JWT handling
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
├── frontend/               # Next.js Frontend
│   ├── app/               # App Router
│   │   ├── (auth)/        # Auth routes (login/register)
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/   # Protected dashboard routes
│   │   │   ├── page.tsx   # Dashboard home
│   │   │   └── todos/
│   │   │       └── page.tsx
│   │   ├── api/           # API routes (for SSR)
│   │   └── layout.tsx     # Root layout
│   ├── components/        # React components
│   │   ├── ui/            # Base UI components
│   │   ├── auth/          # Auth-related components
│   │   └── todos/         # Todo-related components
│   ├── lib/               # Utilities and API client
│   │   ├── api.ts         # API client
│   │   ├── auth.ts        # Auth utilities
│   │   └── utils.ts       # Helper functions
│   ├── hooks/             # Custom React hooks
│   │   └── useAuth.ts     # Auth hook
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.local
├── .env.example           # Environment template
├── .gitignore
└── README.md
```

---

## 🗄️ Database Schema (PostgreSQL/NeonDB)

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    priority INTEGER DEFAULT 0,  -- 0: Low, 1: Medium, 2: High
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Authentication System

### JWT Token Structure
- **Access Token**: 30-minute expiry
- **Refresh Token**: 7-day expiry
- **Algorithm**: HS256

### Password Security
- **Hashing**: bcrypt
- **Salt rounds**: 12

---

## 📡 API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/logout` | Logout (client-side) |

### Todos (`/api/todos`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all user's todos |
| POST | `/api/todos` | Create new todo |
| GET | `/api/todos/{id}` | Get single todo |
| PUT | `/api/todos/{id}` | Update todo |
| DELETE | `/api/todos/{id}` | Delete todo |
| PATCH | `/api/todos/{id}/toggle` | Toggle todo completion |

---

## 📝 Request/Response Schemas

### User Schemas

**Register Request:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Login Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Login Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

### Todo Schemas

**Create Todo Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": 1
}
```

**Todo Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "priority": 1,
  "user_id": 1,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

---

## 🎨 Frontend Pages

### Public Pages
- `/login` - Login form
- `/register` - Registration form

### Protected Pages (Require Auth)
- `/` - Dashboard with todo list
- Todo management interface

### Components
- `TodoList` - Display all todos
- `TodoItem` - Individual todo with actions
- `TodoForm` - Create/edit todo modal
- `Button`, `Input`, `Card` - Base UI components
- `Header` - Navigation with user info
- `Layout` - Page wrapper with auth check

---

## ⚙️ Environment Variables

### Backend (`.env`)
```env
# Database (NeonDB)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔒 Security Measures

1. **Password Hashing**: bcrypt with salt rounds
2. **JWT Tokens**: Short-lived access tokens with refresh token rotation
3. **CORS**: Restrict allowed origins
4. **Rate Limiting**: Protect against brute force attacks
5. **Input Validation**: Pydantic schemas
6. **SQL Injection Prevention**: SQLAlchemy ORM
7. **HTTPS**: Enforce in production

---

## 🧪 Testing Strategy

### Backend Tests
- Unit tests for services
- Integration tests for API endpoints
- Test coverage: >80%

### Frontend Tests
- Component unit tests
- E2E tests for critical flows

---

## 📦 Dependencies

### Backend
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### Frontend
```
next==14.1.0
react==18.2.0
react-dom==18.2.0
tailwindcss==3.4.1
axios==1.6.7
zustand==4.5.0
```

---

## 🚀 Deployment Plan

### Backend
- Platform: Render / Railway / Fly.io
- Database: NeonDB (PostgreSQL)

### Frontend
- Platform: Vercel / Netlify

---

## ✅ Definition of Done

1. [ ] User registration and login work
2. [ ] Full CRUD for todos
3. [ ] JWT authentication protects all todo endpoints
4. [ ] Frontend is responsive and user-friendly
5. [ ] Code follows Clean Architecture principles
6. [ ] All environment variables documented
7. [ ] Project runs locally with `docker-compose up`
8. [ ] API documentation available at `/docs`
