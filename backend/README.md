# Todo Backend

A production-ready Todo API built with FastAPI, featuring authentication and CRUD operations for todo items.

## Features

- RESTful API with FastAPI
- JWT-based authentication
- Async database operations with SQLAlchemy
- Support for multiple database backends (SQLite, PostgreSQL, MySQL)
- CORS configuration
- Health check endpoints
- Comprehensive API documentation at `/docs`

## Quick Start

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Deployment Options

This backend can be deployed to various platforms:

### Docker Deployment

Build and run with Docker:
```bash
docker build -t todo-backend .
docker run -p 8000:8000 -e DATABASE_URL=sqlite+aiosqlite:///todos.db todo-backend
```

Or use docker-compose:
```bash
docker-compose up -d
```

### Platform-as-a-Service Deployment

- **Heroku**: Use the included `Procfile` and `runtime.txt`
- **PythonAnywhere**: Use the `wsgi.py` file
- **Render**: Use the configuration in `render.yaml`
- **Railway**: Automatic detection and deployment
- **Vercel**: With Python runtime support

### Self-Hosted Deployment

Deploy on any VPS or dedicated server using the provided startup scripts:
- `start.sh` for development
- `start-production.sh` for production

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///todos.db` |
| `SECRET_KEY` | Secret key for JWT tokens | Required |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration time | `7` |

## Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation
- `/api/auth/*` - Authentication endpoints
- `/api/todos/*` - Todo management endpoints

## Database Migrations

This application uses Alembic for database migrations:

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description of changes"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT