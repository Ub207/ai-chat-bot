# Deployment Guide: Backend on Hugging Face & Frontend on Vercel

## Overview

This guide explains how to deploy the AI Chat Bot application with:
- Backend API on Hugging Face Spaces
- Frontend on Vercel

## Prerequisites

- GitHub account
- Hugging Face account
- Vercel account
- Git installed locally

## Backend Deployment on Hugging Face Spaces

### Method 1: Direct Upload to Hugging Face

1. Create a new Space on Hugging Face:
   - Go to https://huggingface.co/new-space
   - Choose a name for your space
   - Select "Docker" SDK
   - Select "GPU" or "CPU" hardware (CPU is sufficient for this app)
   - Click "Create Space"

2. Clone your space repository:
   ```bash
   git clone https://huggingface.co/spaces/[your-username]/[space-name]
   cd [space-name]
   ```

3. Copy all files from this repository to your space:
   ```bash
   # From your cloned space directory
   cp -r /path/to/ai-chat-bot/* .
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

### Method 2: Using Git Integration (Recommended)

1. Create a new public repository on GitHub with the code

2. Create a new Space on Hugging Face:
   - Go to https://huggingface.co/new-space
   - Choose a name for your space
   - Select "Docker" SDK
   - Choose "CPU" hardware
   - Under "Repository Type", select "Using Git integration"
   - Enter your GitHub repository URL
   - Click "Duplicate Space"

3. The Space will automatically build and deploy from your GitHub repository

## Frontend Deployment on Vercel

### Prerequisites

Make sure your frontend is in a separate repository or in a way that can be deployed independently.

### Steps

1. Prepare your frontend for deployment:
   - Ensure you have a `frontend/` directory with Next.js application
   - Make sure `frontend/vercel.json` exists (already provided)

2. Deploy to Vercel:
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Import your frontend repository
   - Configure the project:
     - Framework Preset: Next.js
     - Root Directory: `frontend`
     - Environment Variables (set these in Vercel dashboard):
       - `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., `https://your-username.hf.space`)
       - `NEXT_PUBLIC_OPENAI_API_KEY`: Your OpenAI API key (optional for demo)
       - `NEXT_PUBLIC_BETTER_AUTH_URL`: URL of your deployed app
       - `NEXT_PUBLIC_APP_ENV`: `production`
       - `NEXT_PUBLIC_OPENAI_DOMAIN`: `https://api.openai.com`
       - `NEXT_PUBLIC_ENABLE_ANALYTICS`: `false`
       - `NEXT_PUBLIC_MAINTENANCE_MODE`: `false`

3. Click "Deploy" and Vercel will build and deploy your frontend

## Configuration Details

### Backend Configuration

The backend includes a fallback mechanism for Hugging Face Spaces that allows it to run without required secrets:

- If environment variables are missing, the app sets safe demo defaults
- SQLite is used as fallback database (`/tmp/todo.db`)
- Safe placeholder secrets are used (32+ characters to pass validation)
- CORS is configured to allow all origins for demo purposes

### Frontend Configuration

- The frontend expects the backend API to be available at `NEXT_PUBLIC_API_URL`
- All necessary environment variables are configured in `frontend/vercel.json`

## Environment Variables

### Backend (for Hugging Face Spaces)

The following variables are automatically configured with safe defaults for Hugging Face deployment:
- `DATABASE_URL`: Defaults to SQLite in `/tmp/todo.db`
- `JWT_SECRET_KEY`: Demo key with 32+ characters
- `BETTER_AUTH_SECRET`: Demo key with 32+ characters
- `CSRF_SECRET_KEY`: Demo key with 32+ characters
- `OPENAI_API_KEY`: Optional, can be empty for demo

### Frontend (for Vercel)

Required environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., `https://your-username.hf.space`)

## Troubleshooting

### Backend Issues

1. **Build fails on Hugging Face Spaces**:
   - Check that `space.yaml` and `Dockerfile` exist
   - Verify that `requirements_hf.txt` contains all necessary dependencies
   - Look at the build logs in the Hugging Face Space settings

2. **App crashes after deployment**:
   - Check the runtime logs in Hugging Face Space settings
   - Verify that the port is correctly set (should be 7860 for Hugging Face)

3. **Database connection issues**:
   - The app uses SQLite by default for Hugging Face Spaces
   - Check that `/tmp` directory is writable

### Frontend Issues

1. **Cannot connect to backend API**:
   - Verify that `NEXT_PUBLIC_API_URL` is correctly set in Vercel
   - Check browser developer tools for CORS errors
   - Ensure the backend is deployed and accessible

2. **Frontend build fails on Vercel**:
   - Check that `frontend/vercel.json` exists and is properly configured
   - Verify all required environment variables are set

## Scaling Considerations

### For Production Use

While this setup works well for demos, for production use consider:

- Use PostgreSQL instead of SQLite for the backend
- Set strong, unique secrets for JWT, auth, and CSRF
- Implement proper authentication
- Add rate limiting
- Set up proper logging and monitoring

## Updates

To update your deployments:

### Backend
1. Make changes to your GitHub repository
2. Push changes - Hugging Face will automatically rebuild

### Frontend
1. Make changes to your frontend repository
2. Push changes - Vercel will automatically rebuild and deploy

## Testing Your Deployment

Once both deployments are complete:

1. Visit your Hugging Face Space URL to test the backend API
   - Health check: `https://your-username.hf.space/health`
   - API docs: `https://your-username.hf.space/docs`

2. Visit your Vercel deployment URL to test the frontend
   - The frontend should connect to your backend API

3. Test the full functionality by creating conversations and tasks