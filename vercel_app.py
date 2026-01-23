"""
Vercel-compatible FastAPI application entrypoint
This file is specifically designed to work with Vercel's Python runtime
"""

from fastapi import FastAPI
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set default environment variables for serverless deployment
default_vars = {
    'APP_ENV': 'production',
    'DATABASE_URL': 'sqlite:///./todo_chatbot.db',
    'JWT_SECRET_KEY': 'fallback-jwt-secret-key-for-serverless-deployment-32chars',
    'OPENAI_API_KEY': 'sk-test-placeholder-api-key-for-serverless',
    'BETTER_AUTH_SECRET': 'fallback-better-auth-secret-for-serverless-32chars',
    'CSRF_SECRET_KEY': 'fallback-csrf-secret-for-serverless-32chars',
}

for key, value in default_vars.items():
    if not os.getenv(key):
        os.environ[key] = value

# Create a fallback app in case of import errors
app = FastAPI(
    title="Todo App Chatbot API - Production Ready",
    version="0.1.0",
    debug=False
)

@app.get("/")
def root():
    return {
        "message": "Todo App Chatbot API is running",
        "status": "healthy",
        "environment": os.getenv('APP_ENV', 'unknown')
    }

# Attempt to import and integrate the main API functionality
try:
    # Import the main API from backend
    from backend.api import app as main_api

    # Copy routes from main_api to this app instance
    # We'll do this by recreating the main app with the same functionality
    app = main_api

    # Override the startup event to avoid database initialization issues in serverless
    async def no_op_startup():
        """No-operation startup for serverless environments"""
        print("Skipping database initialization in serverless environment")
        pass

    # Replace the startup event
    app.router.on_startup.clear()
    app.on_event("startup")(no_op_startup)

except ImportError as e:
    print(f"Warning: Could not import backend.api, using fallback app: {e}")

    @app.get("/health")
    def health_check():
        return {"status": "degraded", "error": str(e)}

except Exception as e:
    print(f"Warning: Unexpected error importing backend.api: {e}")

    @app.get("/health")
    def health_check():
        return {"status": "error", "error": str(e)}

# Make sure the app instance is available as both 'app' and 'application'
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))