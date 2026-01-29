# Hugging Face Spaces entry point
import os
from src.main import app

# For Hugging Face Spaces, we need to expose the app at module level
# The application will be served using the app variable

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )