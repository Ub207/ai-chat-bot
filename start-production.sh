#!/bin/bash
# Production start script for the Todo Backend

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if not already installed
if ! python -c "import fastapi" >/dev/null 2>&1; then
    pip install -r requirements.txt
fi

# Run the application with production settings
echo "Starting Todo Backend in production mode..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 4