#!/usr/bin/env python3
"""
Test script to verify that the app can be imported without errors
"""
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_import():
    print("Testing app import...")

    try:
        # Set required environment variables for the test
        os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')
        os.environ.setdefault('JWT_SECRET_KEY', 'test-key-for-validation')
        os.environ.setdefault('OPENAI_API_KEY', 'sk-test-key')
        os.environ.setdefault('BETTER_AUTH_SECRET', 'test-auth-secret')
        os.environ.setdefault('CSRF_SECRET_KEY', 'test-csrf-key')

        # Import the app
        from app import app
        print("✓ Successfully imported app")

        # Check if app is a FastAPI instance
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            print("✓ App is a valid FastAPI instance")
        else:
            print("✗ App is not a FastAPI instance")

        # Check for the existence of routes
        routes = [route.path for route in app.routes]
        print(f"✓ Found {len(routes)} routes: {routes[:5]}{'...' if len(routes) > 5 else ''}")

        return True

    except Exception as e:
        print(f"✗ Error importing app: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_import()
    if success:
        print("\n✓ App import test passed!")
    else:
        print("\n✗ App import test failed!")
        sys.exit(1)