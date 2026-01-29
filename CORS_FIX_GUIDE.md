# CORS Configuration for Your Backend

## Current Issue
Your backend on Hugging Face Spaces is configured with these allowed origins:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `https://ubaid-ai-to-do-full-stack.hf.space`

But your frontend is on Vercel at: `https://full-stack-todo-app-wemu.vercel.app`

## Solution
You need to update your backend's CORS settings to allow requests from your Vercel frontend.

### Step 1: Update CORS_ORIGINS in your Hugging Face Space
1. Go to your Hugging Face Space for the backend: https://huggingface.co/spaces/ubaid-ai/fullstack-todo-backend
2. Click on the "Files" tab
3. Edit the `space.yaml` file
4. Update the CORS_ORIGINS line to include your Vercel domain:

Change from:
```
- CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://ubaid-ai-to-do-full-stack.hf.space
```

To:
```
- CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://ubaid-ai-to-do-full-stack.hf.space,https://full-stack-todo-app-wemu.vercel.app
```

### Step 2: If you know your custom domain
If you have a custom domain for your Vercel frontend, add that as well:
```
- CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://ubaid-ai-to-do-full-stack.hf.space,https://full-stack-todo-app-wemu.vercel.app,https://your-custom-domain.com
```

### Step 3: Restart Your Space
After updating the configuration, restart your Hugging Face Space for the changes to take effect.

### Step 4: Update Vercel Environment Variable
Make sure your Vercel project environment variable is set correctly:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://ubaid-ai-fullstack-todo-backend.hf.space`

## Alternative: Allow All Origins (Less Secure)
If you want to temporarily allow all origins for testing (not recommended for production):
```
- CORS_ORIGINS=*
```

## Verification
After making these changes:
1. Wait for your Hugging Face Space to restart
2. Check your Vercel frontend deployment
3. Look at the browser console to see if CORS errors are resolved