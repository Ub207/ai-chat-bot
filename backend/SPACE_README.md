# Todo Backend on Hugging Face Spaces

This is a FastAPI-based Todo application deployed on Hugging Face Spaces.

## About

This is a production-ready Todo API with authentication, built with FastAPI. It provides:

- RESTful API endpoints for todo management
- JWT-based authentication
- Support for multiple database backends
- CORS configuration
- Health check endpoints
- Interactive API documentation

## API Documentation

Once deployed, you can access the interactive API documentation at:
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation

## Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check endpoint
- `/api/auth/*` - Authentication endpoints
- `/api/todos/*` - Todo management endpoints

## Environment Variables

The application requires the following environment variables to be set:

- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SECRET_KEY`: Secret key for JWT tokens
- `CORS_ORIGINS`: Comma-separated list of allowed origins

## Usage

After deployment, the API will be accessible at the Space URL. Use the `/docs` endpoint to explore the API interactively.