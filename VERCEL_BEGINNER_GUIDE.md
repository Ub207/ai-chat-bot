# Vercel Setup Guide for Beginners

## Step 1: Create a Vercel Account
1. Go to https://vercel.com/signup
2. Sign up using your email, GitHub, or GitLab account
3. Verify your email if required

## Step 2: Log in to Vercel CLI
1. Open your terminal/command prompt
2. Run this command:
   ```bash
   vercel login
   ```
3. Follow the prompts to authenticate

## Step 3: Deploy Your Frontend
After logging in, you can deploy with:
```bash
cd frontend
vercel --prod
```

## Alternative Method (Recommended for Beginners): Git Integration
Instead of using the CLI, you can deploy using Git integration:

1. Create a GitHub repository:
   ```bash
   cd /mnt/d/to-do-full-stack
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a new repository on GitHub (https://github.com/new)

3. Push your code to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   git branch -M main
   git push -u origin main
   ```

4. Go to https://vercel.com and click "New Project"

5. Click "Continue" when prompted to import your Git repository

6. Select your repository from the list

7. Vercel will detect it's a Next.js project - just click "Deploy"

8. In the project settings, make sure to set the environment variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://ubaid-ai-to-do-full-stack.hf.space/api`

This Git integration method is often easier for beginners as it handles authentication automatically through GitHub.