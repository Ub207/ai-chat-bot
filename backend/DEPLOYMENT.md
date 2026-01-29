# Deployment Guide for Todo Backend

This guide provides instructions for deploying the Todo backend application to various platforms.

## Prerequisites

- Python 3.11+
- pip package manager
- Git (for deployment to cloud platforms)

## Deployment Options

### 1. Deploy to PythonAnywhere

PythonAnywhere is a cloud hosting platform that supports Python web applications.

#### Steps:

1. Sign up for a PythonAnywhere account
2. Create a new web application
3. Clone your repository:
   ```bash
   git clone <your-repo-url>
   ```
4. Set up a virtual environment:
   ```bash
   mkvirtualenv todo-backend --python=/usr/bin/python3.11
   pip install -r requirements.txt
   ```
5. Configure your web app:
   - Go to the Web tab in PythonAnywhere dashboard
   - Set the WSGI configuration file to point to your `wsgi.py`
   - Update the path in `wsgi.py` to match your PythonAnywhere directory
6. Set environment variables in the PythonAnywhere dashboard:
   - DATABASE_URL
   - SECRET_KEY
   - CORS_ORIGINS
   - Other environment variables as needed

### 2. Deploy with Docker

Create a Dockerfile for containerized deployment:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t todo-backend .
docker run -p 8000:8000 -e DATABASE_URL=sqlite+aiosqlite:///todos.db todo-backend
```

### 3. Deploy to Heroku

1. Create a `Procfile` in your project root:
   ```
   web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
   ```

2. Create a `runtime.txt` to specify Python version:
   ```
   python-3.11.0
   ```

3. Deploy using Heroku CLI:
   ```bash
   heroku create
   heroku buildpacks:set heroku/python
   git push heroku main
   heroku config:set DATABASE_URL=<your-database-url>
   heroku config:set SECRET_KEY=<your-secret-key>
   heroku open
   ```

### 4. Deploy to Render

1. Create a `render.yaml` file:
   ```yaml
   services:
     - type: web
       name: todo-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           fromDatabase: tododb
             name: todo-db
         - key: SECRET_KEY
           generateValue: true
   databases:
     - name: todo-db
       region: frankfurt  # or us-west
       plan: free
   ```

2. Connect your GitHub repository to Render and deploy.

### 5. Deploy to Railway

1. Install Railway CLI or connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Railway will automatically detect and deploy the Python application

### 6. Self-hosted Deployment

For self-hosted deployment on a VPS or dedicated server:

1. Install Python 3.11+ and pip
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd todo-backend
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set environment variables:
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost/tododb
   export SECRET_KEY=your-very-long-secret-key
   export CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
   ```
6. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## Environment Variables

Required environment variables:

- `DATABASE_URL`: Database connection string (e.g., `postgresql://user:pass@localhost/dbname`)
- `SECRET_KEY`: Secret key for JWT tokens (generate a strong random key)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time (default: 7)

## Database Setup

The application supports multiple database backends:

- SQLite: `sqlite+aiosqlite:///todos.db`
- PostgreSQL: `postgresql+asyncpg://user:password@localhost/dbname`
- MySQL: `mysql+aiomysql://user:password@localhost/dbname`

## Running with Gunicorn (Production)

For production deployments, use Gunicorn with Uvicorn worker:

```bash
pip install gunicorn
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT
```

## Health Checks

The application provides a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "message": "Todo API is running"
}
```

## Monitoring and Logging

The application uses FastAPI's built-in logging. For production, consider implementing:

- Structured logging with log levels
- Centralized log aggregation
- Application performance monitoring
- Error tracking services