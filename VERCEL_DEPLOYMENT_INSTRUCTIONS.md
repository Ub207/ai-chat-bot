# Deploying Frontend to Vercel

Since you already have the `NEXT_PUBLIC_API_URL` set, here are the steps to deploy your frontend to Vercel:

## Prerequisites
- Vercel CLI installed: `npm install -g vercel`
- Logged into Vercel: `vercel login`

## Deployment Steps

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Deploy with the environment variable:
   ```bash
   vercel --env NEXT_PUBLIC_API_URL='https://ubaid-ai-to-do-full-stack.hf.space/api'
   ```

OR if you want to deploy without specifying the environment variable in the command (since you already have it set locally):

```bash
cd frontend
vercel
```

Then follow the prompts in the Vercel CLI to complete the deployment.

## Alternative: Git Integration (Recommended)

For easier future deployments:

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to https://vercel.com and import your repository
3. In the project settings, make sure `NEXT_PUBLIC_API_URL` is set to `'https://ubaid-ai-to-do-full-stack.hf.space/api'`
4. Vercel will automatically deploy when you push to your repository

Your frontend should now be ready for deployment on Vercel!