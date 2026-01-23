import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Set default environment variables for serverless
os.environ.setdefault('APP_ENV', 'production')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./todo_chatbot.db')
os.environ.setdefault('JWT_SECRET_KEY', 'fallback-jwt-secret-key-for-serverless-deployment-32chars')
os.environ.setdefault('OPENAI_API_KEY', 'sk-test-placeholder-api-key-for-serverless')
os.environ.setdefault('BETTER_AUTH_SECRET', 'fallback-better-auth-secret-for-serverless-32chars')
os.environ.setdefault('CSRF_SECRET_KEY', 'fallback-csrf-secret-for-serverless-32chars')

# Create the FastAPI app directly for Vercel
app = FastAPI(
    title="Todo App Chatbot API - Vercel Deployment",
    version="0.1.0",
    debug=False
)

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for serverless deployment
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Total-Count"],
)

# Import and include routes conditionally to avoid circular imports during build
try:
    # Import the main API to get all routes
    from backend.api import app as main_app

    # Copy routes from main app to this instance
    for route in main_app.routes:
        app.routes.append(route)

    # Ensure startup events are handled appropriately for serverless
    async def startup_event():
        # Skip heavy initialization in serverless environment
        pass

    app.on_event("startup")(startup_event)

except ImportError as e:
    # If there's an import error, provide a basic working app
    @app.get("/")
    def health_check():
        return {
            "status": "error",
            "message": f"Failed to load main application: {str(e)}",
            "details": "Please check your dependencies and imports"
        }

# Vercel expects the application to be available as 'app' or 'application'
# Both are available here as the same object
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))