# Fix for Hugging Face Backend Connection

## Your Backend URL
Your backend is deployed on Hugging Face Spaces at:
https://huggingface.co/spaces/ubaid-ai/fullstack-todo-backend

The actual API URL is:
https://ubaid-ai-fullstack-todo-backend.hf.space

## Required Configuration

### 1. Update Environment Variable in Vercel
In your Vercel project settings (https://vercel.com/ubaid-ur-rahmans-projects-6b672f56/full-stack-todo-app-wemu), set:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://ubaid-ai-fullstack-todo-backend.hf.space`

### 2. Important: Check Hugging Face Space Settings
Hugging Face Spaces might have CORS restrictions. You need to ensure your Hugging Face Space allows requests from your Vercel frontend.

### 3. Alternative Solution
If you continue having issues, you might need to check if your Hugging Face Space backend has proper CORS configuration to accept requests from your Vercel frontend domain.

### 4. Steps to Fix
1. Go to your Vercel dashboard: https://vercel.com/ubaid-ur-rahmans-projects-6b672f56/full-stack-todo-app-wemu
2. Go to Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` to: `https://ubaid-ai-fullstack-todo-backend.hf.space`
4. Go to Deployments and click "Redeploy"
5. Check the build logs for any errors

## Common Issue: CORS
Hugging Face Spaces sometimes have CORS restrictions that prevent external websites (like your Vercel frontend) from accessing the API. This is likely why you're seeing errors even though the backend is deployed.

## Potential Solution
If CORS is the issue, you might need to:
1. Modify your backend to include proper CORS headers for your Vercel domain
2. Or deploy both frontend and backend to Vercel for seamless integration