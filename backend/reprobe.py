
import requests
import sys

try:
    # Check Health
    print("Checking Health...")
    r = requests.get("http://localhost:8000/health")
    print(f"Health: {r.status_code} - {r.text}")

    # Check Root
    print("Checking Root...")
    r = requests.get("http://localhost:8000/")
    print(f"Root: {r.status_code} - {r.text}")

    # Check Todos List (GET)
    print("Checking GET /api/todos...")
    r = requests.get("http://localhost:8000/api/todos")
    print(f"GET Todos: {r.status_code} - {r.text[:100]}...")

except Exception as e:
    print(f"Error: {e}")
