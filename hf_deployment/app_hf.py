import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# For Hugging Face Spaces, we rely on the config fallback mechanism instead of setting defaults here
# This allows the Settings validation to fail and trigger the fallback mechanism
# Only set the minimal APP_ENV to indicate production mode
if not os.getenv('APP_ENV'):
    os.environ['APP_ENV'] = 'production'

# Also set HF_SPACE indicator for the config
if 'HF_SPACE' not in os.environ:
    os.environ['HF_SPACE'] = 'true'

# Import and create the FastAPI app
from backend.api import app

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a root endpoint for Hugging Face Spaces
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AI Chat Bot Backend API is running on Hugging Face Spaces",
        "environment": os.getenv('APP_ENV', 'unknown'),
        "deployment": "huggingface-spaces"
    }

# Add health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Service is operational",
        "timestamp": os.getenv('APP_ENV', 'unknown')
    }

if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces uses port 7860 by default
    uvicorn.run(
        "app_hf:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860)),
        log_level="info"
    )