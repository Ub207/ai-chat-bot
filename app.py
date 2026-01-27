import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

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
    return {"status": "ok", "message": "AI Chat Bot Backend API is running"}

# Create the Mangum handler for ASGI compatibility
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces uses port 7860 by default
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))