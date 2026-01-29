# Hugging Face Spaces entry point
import os
import sys
import os.path

# Add the parent directory to Python path to ensure src can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.main import app

# For Hugging Face Spaces, we need to expose the app at module level
# The application will be served using the app variable

if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces requires the app to run on port 7860 by default
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )