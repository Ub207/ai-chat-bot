
import requests
import sys
import os

# Use port 7860 for Hugging Face Spaces or fallback to 8000
port = int(os.environ.get("PORT", 7860))

try:
    # Check Health
    print("Checking Health...")
    r = requests.get(f"http://localhost:{port}/health")
    print(f"Health: {r.status_code} - {r.text}")

    # Check Root
    print("Checking Root...")
    r = requests.get(f"http://localhost:{port}/")
    print(f"Root: {r.status_code} - {r.text}")

    # Check Todos List (GET)
    print("Checking GET /api/todos...")
    r = requests.get(f"http://localhost:{port}/api/todos")
    print(f"GET Todos: {r.status_code} - {r.text[:100]}...")

except Exception as e:
    print(f"Error: {e}")
