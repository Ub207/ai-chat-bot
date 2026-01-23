import sys
import os

# Add the project root to the Python path to import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Provide default values for required environment variables for serverless deployment
default_vars = {
    'APP_ENV': 'production',
    'DATABASE_URL': 'sqlite:///./todo_chatbot.db',  # Use SQLite as fallback
    'JWT_SECRET_KEY': 'fallback-jwt-secret-key-for-serverless-deployment-32chars',
    'OPENAI_API_KEY': 'sk-test-placeholder-api-key-for-serverless',
    'BETTER_AUTH_SECRET': 'fallback-better-auth-secret-for-serverless-32chars',
    'CSRF_SECRET_KEY': 'fallback-csrf-secret-for-serverless-32chars',
}

for key, value in default_vars.items():
    if not os.getenv(key):
        os.environ[key] = value

# Import and create the FastAPI app
from backend.api import app

# This ensures the app is available for Vercel's Python runtime
application = app  # Alternative name for Vercel compatibility

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))