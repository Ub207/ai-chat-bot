# This file makes the app directory a Python package
# For Hugging Face Spaces compatibility, expose the main app from src
import sys
import os

# Ensure src is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src.main import app
except ImportError as e:
    print(f"Error importing app from src: {e}")
    raise

# Make the app available when importing from the app package
__all__ = ['app']
