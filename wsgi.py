#!/usr/bin/env python3
"""
WSGI configuration for deployment platforms like Hugging Face Spaces.
This file creates a bridge between the server and your FastAPI application.
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import and create the FastAPI app
from src.main import app

# PythonAnywhere expects an 'application' object
application = app

if __name__ == "__main__":
    import uvicorn
    # Use port 7860 for Hugging Face Spaces or fallback to 8000
    import os
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("wsgi:app", host="0.0.0.0", port=port, reload=True)