# Deployment Guide

This document provides step-by-step instructions for deploying the AI Chat Bot application to production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Environment Variables Setup](#environment-variables-setup)
- [Database Migration](#database-migration-steps)
- [Post-Deployment Testing](#post-deployment-testing)
- [Troubleshooting](#troubleshooting-common-issues)

## Prerequisites

Before deploying the application, ensure you have:

- An account on your chosen hosting platform (Railway, Render, or Vercel for backend; Vercel for frontend)
- Access to a PostgreSQL database (managed or self-hosted)
- OpenAI API key
- Better Auth secret keys
- Domain name (optional but recommended)

## Backend Deployment

### Deploying to Railway

1. **Connect your GitHub repository to Railway**
   - Log in to Railway (https://railway.app)
   - Click "New Project" and select "From GitHub"
   - Choose your repository containing the AI Chat Bot

2. **Configure the project**
   - Railway will automatically detect the project as Python
   - Set the builder to "Nixpacks" (configured in railway.json)
   - Set the start command to `cd backend && bash start.sh`

3. **Set environment variables**
   - Add all required environment variables (see Environment Variables Setup section)
   - Ensure `DATABASE_URL`, `JWT_SECRET_KEY`, `OPENAI_API_KEY`, and `BETTER_AUTH_SECRET` are properly configured

4. **Deploy**
   - Click "Deploy" to start the deployment process
   - Monitor the deploy logs for any errors
   - Once complete, note the assigned domain URL

### Deploying to Render

1. **Connect your GitHub repository to Render**
   - Log in to Render (https://render.com)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository

2. **Configure the build settings**
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && bash start.sh`
   - Environment: Python 3.12.3 (or latest compatible version)

3. **Set environment variables**
   - Add all required environment variables (see Environment Variables Setup section)

4. **Configure additional settings**
   - Set the region closest to your users
   - Configure auto-deploy from the main branch (optional)
   - Set up a PostgreSQL database service if needed

5. **Deploy**
   - Click "Create Web Service" to start the deployment
   - Monitor the build logs for any errors

### Deploying to Other Platforms (Heroku-style)

The application can also be deployed to platforms that support Procfile-based deployments:

1. **Platform Setup**
   - The Procfile defines the web process as: `web: cd backend && bash start.sh`
   - Ensure your platform supports Python 3.12 and can run bash scripts

2. **Deployment Process**
   - Follow your platform's standard deployment process
   - Ensure environment variables are configured before deployment

## Frontend Deployment

### Deploying to Vercel

1. **Connect your GitHub repository to Vercel**
   - Log in to Vercel (https://vercel.com)
   - Click "New Project" and import your repository
   - Select the frontend directory

2. **Configure the project settings**
   - Framework Preset: Next.js (will be auto-detected)
   - Build Command: `npm run build` (configured in vercel.json)
   - Output Directory: Default Next.js output

3. **Set environment variables**
   - Add all required frontend environment variables (see Environment Variables Setup section)
   - Ensure `NEXT_PUBLIC_API_URL` points to your backend deployment URL

4. **Deploy**
   - Click "Deploy" to start the deployment process
   - Vercel will automatically build and deploy your frontend
   - Once complete, you'll receive a preview URL

5. **Configure Custom Domain (Optional)**
   - Go to Project Settings → Domains
   - Add your custom domain and follow DNS configuration instructions

## Environment Variables Setup

### Backend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL database connection string |
| `JWT_SECRET_KEY` | Yes | Secret key for JWT token signing |
| `OPENAI_API_KEY` | Yes | OpenAI API key for chat completions |
| `BETTER_AUTH_SECRET` | Yes | Secret key for Better Auth |
| `BETTER_AUTH_URL` | Yes | Base URL for Better Auth |
| `SERVER_HOST` | No | Host address for the server (defaults to 0.0.0.0) |
| `SERVER_PORT` | No | Port number for the server (defaults to 8000) |
| `WORKERS` | No | Number of worker processes (defaults to 4) |

### Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL (e.g., https://your-app.railway.app) |
| `NEXT_PUBLIC_OPENAI_API_KEY` | No | OpenAI API key (not recommended for production) |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Yes | Better Auth URL |
| `NEXT_PUBLIC_APP_ENV` | No | Application environment (development, staging, production) |
| `NEXT_PUBLIC_OPENAI_DOMAIN` | No | OpenAI domain override |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | No | Enable analytics (true/false) |
| `NEXT_PUBLIC_MAINTENANCE_MODE` | No | Enable maintenance mode (true/false) |

## Database Migration Steps

The application handles database initialization automatically during startup:

1. **Automatic Initialization**
   - The start script (`backend/start.sh`) automatically runs database initialization
   - The `init_db()` function creates tables if they don't exist
   - No manual migration steps are required

2. **Manual Database Setup (Alternative)**
   If automatic initialization fails, you can manually initialize the database:
   ```bash
   cd backend
   python -c "from db import init_db; init_db()"
   ```

3. **Backup and Restore**
   - Regular backups should be configured based on your hosting provider
   - For PostgreSQL, you can use `pg_dump` and `pg_restore` for manual backups

## Post-Deployment Testing

After successful deployment, perform the following tests:

1. **Health Check**
   - Visit the health endpoint: `https://your-backend-url/health`
   - Verify the response indicates healthy status

2. **API Endpoints**
   - Test the main API endpoints to ensure they're accessible
   - Verify authentication endpoints work correctly

3. **Frontend Connection**
   - Visit your frontend URL
   - Ensure it can connect to the backend API
   - Test user registration and login functionality

4. **Chat Functionality**
   - Test the chat interface to ensure it communicates with the backend
   - Verify that messages are properly sent and received

5. **Database Operations**
   - Test creating, reading, updating, and deleting tasks
   - Ensure data persists correctly in the database

## Troubleshooting Common Issues

### Deployment Failures

**Issue: Build fails due to missing dependencies**
- Solution: Verify that `requirements.txt` includes all necessary packages
- Check that the Python version is compatible (3.12 recommended)

**Issue: Start script fails**
- Solution: Check the deployment logs for specific error messages
- Verify that all required environment variables are set
- Ensure the start command is correctly configured

### Environment Variable Issues

**Issue: Application crashes due to missing environment variables**
- Solution: Double-check that all required environment variables are set
- Verify that variable names match exactly (case-sensitive)

**Issue: Database connection fails**
- Solution: Verify the `DATABASE_URL` format is correct
- Check that the database is accessible from the deployment environment
- Ensure the database credentials are correct

### CORS and API Issues

**Issue: Frontend cannot connect to backend API**
- Solution: Verify that the backend CORS settings allow the frontend origin
- Check that `NEXT_PUBLIC_API_URL` points to the correct backend URL

**Issue: Authentication fails**
- Solution: Ensure `BETTER_AUTH_URL` and related variables are correctly set
- Verify that the frontend and backend are properly configured for authentication

### Performance Issues

**Issue: Slow response times**
- Solution: Check the server resources and consider scaling up
- Verify that the database connection is optimized
- Consider implementing caching if needed

**Issue: High memory usage**
- Solution: Monitor memory usage and optimize as needed
- Consider reducing the number of workers if memory is limited
- Optimize database queries if necessary

### Health Check Failures

If the health endpoint indicates issues:

1. Check the application logs for error messages
2. Verify database connectivity
3. Test individual components separately
4. Review the health check implementation in `backend/health.py`

## Additional Resources

- [Application Documentation](README.md)
- [API Documentation](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Security Best Practices](docs/SECURITY.md)