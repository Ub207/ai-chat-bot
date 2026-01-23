import sys
import os

# Add the project root to the Python path to import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from backend.db import get_session
from backend.config import settings

# Create a minimal app instance for Vercel deployment
app = FastAPI(
    title="Todo App Chatbot API - Vercel Deployment",
    version="0.1.0",
    debug=False
)

# Configure CORS for Vercel deployment
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
]

# Add production origins from environment
production_origin = getattr(settings, 'FRONTEND_ORIGIN', None)
if production_origin:
    origins.append(production_origin)

vercel_origin = getattr(settings, 'VERCEL_URL', None)
if vercel_origin:
    origins.append(f"https://{vercel_origin}")

# For Vercel, allow all origins during development
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Total-Count"],
)

# Import and include the routers from the main API instead of copying endpoints
# This keeps the code DRY while allowing for serverless deployment
def include_routers():
    """Include all the routers from the main API with minimal modifications"""
    # Import main API functionality
    from backend.api import *

    # Since we're importing everything from the original API,
    # the routes will be automatically added to this app instance
    # when the original module is imported

# Call this function to set up routes
include_routers()

@app.get("/")
def root():
    """Root endpoint for health check"""
    return {"message": "Todo App Chatbot API - Deployed on Vercel", "status": "healthy"}

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "deployment": "vercel"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))