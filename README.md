# Todo Full Stack Application

A production-ready full-stack Todo application built with FastAPI, Next.js, and PostgreSQL.

## Features

- Full CRUD operations for todos
- Mark todos as complete/incomplete
- Filter todos by status (all/active/completed)
- Statistics dashboard
- Responsive UI with Tailwind CSS
- Clean Architecture principles
- Async database operations

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), PostgreSQL
- **Frontend**: Next.js 14, React, Tailwind CSS, Zustand
- **Database**: PostgreSQL (NeonDB compatible)
- **Testing**: pytest (backend), Jest (frontend)

## Project Structure

```
to-do-full-stack/
├── backend/                 # FastAPI Backend
│   ├── src/
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database connection
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   └── pyproject.toml
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # React components
│   │   ├── lib/            # API client & store
│   │   ├── types/          # TypeScript types
│   │   └── __tests__/      # Frontend tests
│   ├── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (NeonDB or local)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your database URL:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname?sslmode=require
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=true
   CORS_ORIGINS=http://localhost:3000
   ```

5. Run migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

   API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   App will be available at `http://localhost:3000`

## API Endpoints

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | List all todos with stats |
| POST | `/api/todos` | Create new todo |
| GET | `/api/todos/{id}` | Get single todo |
| PUT | `/api/todos/{id}` | Update todo |
| PATCH | `/ap/todos/{id}/status` | Toggle completion |
| DELETE | `/api/todos/{id}` | Delete todo |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | API info |

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Environment Variables

### Backend (`.env`)

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname?sslmode=require
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## License

MIT
