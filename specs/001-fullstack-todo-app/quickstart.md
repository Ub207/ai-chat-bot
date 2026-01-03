# Quickstart Guide: Full Stack Todo Application

**Phase**: 1 - Design
**Date**: 2025-12-31
**Status**: Approved

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database on Neon
- Git

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd to-do-full-stack
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Neon database connection string

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload
```

**Backend will run at:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with API URL

# Start development server
npm run dev
```

**Frontend will run at:** http://localhost:3000

### 4. Verify Installation

```bash
# Test backend health
curl http://localhost:8000/health

# Test frontend
open http://localhost:3000
```

## Environment Variables

### Backend (.env)

```env
# Neon PostgreSQL connection
DATABASE_URL=postgresql://user:password@ep-xxx.region.neon.tech/todo_db?sslmode=require

# Application settings
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Project Structure

```
to-do-full-stack/
├── backend/
│   ├── src/
│   │   ├── main.py          # Application entry point
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── api/             # Route handlers
│   │   └── db/              # Database connection
│   ├── tests/
│   ├── alembic/             # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Next.js pages
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript types
│   ├── public/
│   └── package.json
└── specs/
    └── 001-fullstack-todo-app/
        ├── spec.md
        ├── plan.md
        └── contracts/
            └── api-endpoints.md
```

## Common Commands

### Backend

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Lint code
flake8 src/
black src/

# Generate migration
alembic revision --autogenerate -m "description"
```

### Frontend

```bash
# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Deployment

### Backend Deployment (Railway/Render)

1. Connect repository to hosting platform
2. Set environment variables (DATABASE_URL, etc.)
3. Deploy automatically from main branch

### Frontend Deployment (Vercel)

1. Connect repository to Vercel
2. Set NEXT_PUBLIC_API_URL environment variable
3. Deploy automatically from main branch

## Troubleshooting

### Database Connection Issues

- Verify Neon connection string is correct
- Check SSL mode is required for Neon
- Ensure IP allowlist includes hosting platform

### CORS Errors

- Configure CORS settings in backend/main.py
- Add frontend origin to allowed hosts

### Port Already in Use

- Change port in .env or command line
- Kill process using the port: `lsof -ti:8000 | xargs kill`
