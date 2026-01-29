# Deploy Frontend to Vercel - Quick Instructions

## Prerequisites
- A deployed backend API (get the URL)
- Git repository with the code pushed

## Steps

### 1. Deploy Backend First (Required)
Make sure your backend API is deployed and accessible. You'll need the URL for the next step.

### 2. Deploy Frontend to Vercel

#### Option A: Git Integration (Recommended)
1. Push your code to GitHub/GitLab/Bitbucket
2. Go to https://vercel.com
3. Click "New Project" → "Import Project"
4. Select your repository
5. Set the root directory to `frontend`
6. In Environment Variables, add:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your backend API URL (e.g., `https://your-backend-app.vercel.app/api`)
7. Click "Deploy"

#### Option B: Vercel CLI
1. Install CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Navigate to frontend: `cd frontend`
4. Deploy: `vercel --env NEXT_PUBLIC_API_URL='https://your-backend-api.com/api'`

### 3. Verify Deployment
- Visit your deployed frontend URL
- Check that it connects to the backend API
- Test creating, updating, and deleting todos

## Need Help?
Refer to `Vercel_Deployment_Guide.md` for detailed instructions.