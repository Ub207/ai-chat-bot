# Troubleshooting Vercel Deployment Issues

## Current Situation
- You have a Vercel project at: https://vercel.com/ubaid-ur-rahmans-projects-6b672f56/full-stack-todo-app-wemu
- Backend has been deployed
- Frontend deployment is showing errors

## Common Causes and Solutions

### 1. Environment Variable Issues
Make sure your Vercel project has the correct environment variable set:
- Go to your Vercel dashboard: https://vercel.com/ubaid-ur-rahmans-projects-6b672f56/full-stack-todo-app-wemu
- Click on "Settings" → "Environment Variables"
- Add this environment variable:
  - Key: `NEXT_PUBLIC_API_URL`
  - Value: Your backend API URL (e.g., the URL where your backend is deployed)

### 2. Build Issues
Check the build logs in your Vercel dashboard for specific error messages:
- Go to your project dashboard
- Look at the "Deployments" tab
- Click on the failed deployment to see detailed logs

### 3. Project Root Directory
Make sure Vercel is looking in the right directory:
- In your Vercel project settings, set the "Root Directory" to `frontend`
- This ensures Vercel builds from the frontend folder, not the root

### 4. Framework Configuration
Verify that Vercel detects this as a Next.js project:
- It should automatically detect Next.js based on your package.json
- Make sure your `vercel.json` in the frontend directory is properly configured

## Steps to Fix

### Step 1: Check Current Environment Variables
1. Go to https://vercel.com/ubaid-ur-rahmans-projects-6b672f56/full-stack-todo-app-wemu/settings/environment-variables
2. Verify `NEXT_PUBLIC_API_URL` is set correctly

### Step 2: Redeploy
1. In your Vercel dashboard, go to Deployments
2. Click the "Redeploy" button on the failed deployment
3. Or push a new commit to trigger a fresh build

### Step 3: If Still Having Issues
1. Go to Project Settings → General
2. Under "Build & Development Settings", make sure:
   - Framework Preset: Next.js
   - Root Directory: frontend
   - Build Command: `npm run build` or leave empty for auto-detection
   - Output Directory: Leave empty for Next.js (auto-detected)

## Backend URL Verification
Since you mentioned the backend is deployed, you need to know the exact URL of your backend API to set in the `NEXT_PUBLIC_API_URL` variable. Common patterns are:
- If deployed on Vercel: `https://your-backend-project-name.vercel.app/api`
- If deployed elsewhere: `https://yourdomain.com/api`

Check your backend deployment to get the exact URL, then update the environment variable in your Vercel project.