#!/bin/bash

# Start script for Todo App Chatbot backend
# This script initializes the application and starts the server

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Todo App Chatbot backend..."

# Check if required environment variables are set
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL environment variable is not set"
    exit 1
fi

if [ -z "$JWT_SECRET_KEY" ]; then
    echo "Error: JWT_SECRET_KEY environment variable is not set"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    exit 1
fi

if [ -z "$BETTER_AUTH_SECRET" ]; then
    echo "Error: BETTER_AUTH_SECRET environment variable is not set"
    exit 1
fi

echo "Environment variables validated successfully"

# Initialize database
echo "Initializing database..."
python -c "from backend.db import init_db; init_db()"
echo "Database initialized"

# Start the application
echo "Starting FastAPI server..."
exec uvicorn backend.api:app --host ${SERVER_HOST:-0.0.0.0} --port ${SERVER_PORT:-8000} --workers ${WORKERS:-4}