
import requests
import json

url = "http://localhost:8000/api/todos"

print(f"Testing POST to {url}...")
try:
    payload = {"title": "Probe Task", "description": "Checking 8000"}
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text}")
except Exception as e:
    print(f"Error: {e}")
