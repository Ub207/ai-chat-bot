"""
Main entry point for Hugging Face Spaces deployment.
This file serves as the main application entry point for Hugging Face Spaces.
"""
import os
import sys

# Add the directory containing this file to Python path to ensure src can be imported
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Import the main app from the src structure
from src.main import app

# Hugging Face Spaces expects an 'app' variable at the module level
# This will be picked up by the Spaces runtime