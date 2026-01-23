import os
from contextlib import asynccontextmanager

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

# Define lifespan to avoid database initialization during startup
@asynccontextmanager
async def lifespan(app):
    print("Starting up - skipping database initialization in serverless environment")
    yield
    print("Shutting down")

# Mock the database initialization to prevent issues during import
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Temporarily mock init_db to prevent database initialization during import
import backend.db
original_init_db = getattr(backend.db, 'init_db', lambda: None)

def mock_init_db():
    print("Database initialization skipped for serverless deployment")
    pass

backend.db.init_db = mock_init_db

# Now import the main API with all its routes
from backend.api import app as backend_app

# Replace the startup event to avoid database initialization issues in serverless
async def no_op_startup():
    print("Skipping database initialization in serverless environment")
    pass

# Clear any existing startup events and add our no-op startup
backend_app.router.on_startup.clear()
backend_app.router.on_shutdown.clear()  # Also clear shutdown events
backend_app.router.lifespan_context = lifespan

# Add a simple health check endpoint
@backend_app.get("/")
def root():
    return {
        "message": "Todo App Chatbot API is running",
        "status": "healthy",
        "environment": os.getenv('APP_ENV', 'unknown'),
        "deployment": "vercel"
    }

# Make sure the app instance is available as both 'app' and 'application'
app = backend_app
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))