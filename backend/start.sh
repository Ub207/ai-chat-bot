#!/bin/bash
# Start script for the Todo Backend

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the application
echo "Starting Todo Backend..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --reload