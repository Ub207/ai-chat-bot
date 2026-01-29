
import requests
import json
import os

# Use port 7860 for Hugging Face Spaces or fallback to 8000
port = int(os.environ.get("PORT", 7860))
url = f"http://localhost:{port}/api/todos"

print(f"Testing POST to {url}...")
try:
    payload = {"title": "Probe Task", "description": f"Checking port {port}"}
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text}")
except Exception as e:
    print(f"Error: {e}")
