---
title: AI Chat Bot Backend API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "4.0.0"
python_version: "3.11"
app_file: app_hf.py
pinned: false
---

# AI Chat Bot Backend - Hugging Face Space

FastAPI-based backend for the AI Chat Bot application, packaged for Hugging Face Spaces.

## Features
- FastAPI REST API with SQLite persistence
- JWT authentication (demo fallbacks available)
- Todo management + conversation history
- OpenAPI docs at `/docs` and `/redoc`

## Runtime / Config
- Port: **7860** (HF default)
- DB: `sqlite:////tmp/todo.db` fallback
- Env vars (set in Space Settings → Variables & secrets):
  - `JWT_SECRET_KEY` (>=32 chars)
  - `BETTER_AUTH_SECRET` (>=32 chars)
  - `CSRF_SECRET_KEY` (>=32 chars)
  - `OPENAI_API_KEY` (optional)
  - `DATABASE_URL` (optional; defaults to SQLite)

## Key Endpoints
- `GET /` — status
- `GET /health` — health
- `POST /conversations/` — create conversation
- `GET /conversations` — list conversations
- `GET /conversations/{id}/messages` — list messages
- `POST /conversations/{id}/messages` — chat
- `POST /tasks/` — create task
- `GET /tasks/{user_id}` — list tasks
- `PUT /tasks/{id}/complete` — complete task
- `DELETE /tasks/{id}` — delete task

## Deploy Steps (summary)
1) Clone Space repo and copy: `app_hf.py`, `Dockerfile`, `requirements_hf.txt`, `space.yaml`, `.dockerignore`, `backend/`, and this `README_HF.md` (rename to `README.md` in the Space repo).
2) `git add . && git commit -m "Deploy backend" && git push`
3) Set env vars (recommended) in Space Settings.
4) Wait for build, then test: `https://ubaid-ai-bot.hf.space/health`
