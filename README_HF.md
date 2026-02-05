# AI Chat Bot Backend - Hugging Face Space

This is the backend API for the AI Chat Bot application, deployed as a Hugging Face Space.

## Features
- FastAPI-based REST API
- SQLite database for persistence
- JWT-based authentication
- Todo management functionality
- AI-powered chat capabilities

## Configuration
- Runs on port 7860 (Hugging Face default)
- Uses SQLite database stored as `todo_chatbot.db`
- Environment variables are configured automatically for Hugging Face Spaces

## Endpoints
- `GET /` - Health check and status
- `GET /health` - Health check endpoint
- `/api/v1/` - Main API routes
- `/docs` - Interactive API documentation
- `/redoc` - Alternative API documentation

## Deployment
This Space is automatically deployed from the GitHub repository. When changes are pushed to the main branch, Hugging Face Spaces will rebuild and redeploy the application.

## Environment Variables
The application is configured to work with Hugging Face Spaces environment and will use fallback values for required configuration when environment variables are not set.
