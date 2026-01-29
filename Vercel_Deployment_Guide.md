# Deploying the Todo Frontend to Vercel

This guide will walk you through deploying the frontend of the Todo application to Vercel.

## Prerequisites

1. A GitHub, GitLab, or Bitbucket account
2. A deployed backend API (either self-hosted or on a platform like Vercel, Heroku, etc.)

## Option 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Prepare Your Repository

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Make sure your repository contains:
   - The frontend code in the `frontend` directory
   - Proper `package.json` with all dependencies
   - `vercel.json` configuration file
   - `next.config.mjs` configuration file

### Step 2: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Choose the `frontend` directory as your project root
5. Configure the project settings:
   - Framework Preset: Next.js (should be auto-detected)
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Development Command: `npm run dev`

### Step 3: Set Environment Variables

During the deployment setup or afterward in the project settings:

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add the following environment variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: The URL of your deployed backend API
     (e.g., `https://your-backend-app.vercel.app/api` or `https://yourdomain.com/api`)

### Step 4: Deploy

Click "Deploy" and Vercel will build and deploy your application.

## Option 2: Deploy via Vercel CLI

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

Note: If you're getting permission errors, you might need to use:
```bash
sudo npm install -g vercel
```
or install Node.js with a node version manager like `nvm`.

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 4: Deploy

```bash
vercel --env NEXT_PUBLIC_API_URL='https://your-backend-api.com/api'
```

Or, you can set environment variables interactively:

```bash
vercel
```

And follow the prompts to set your environment variables.

## Backend API Requirements

Your frontend needs to connect to a backend API that provides the following endpoints:

- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PATCH /api/todos/:id/status` - Update todo status
- `DELETE /api/todos/:id` - Delete a todo

### Deploying the Backend First

If you don't have a backend deployed yet, you'll need to deploy the backend first. The backend is located in the `backend` directory of this repository and is built with FastAPI.

#### Option 1: Deploy Backend to Vercel

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `vercel.json` file in the backend directory:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

3. Install Vercel CLI and deploy:
   ```bash
   vercel --prod
   ```

4. Set environment variables during deployment:
   - `DATABASE_URL`: Your database connection string (e.g., `sqlite:///todos.db` for SQLite)
   - `SECRET_KEY`: A secure secret key for JWT tokens
   - `CORS_ORIGINS`: Comma-separated list of allowed origins (include your frontend URL)

#### Option 2: Deploy Backend to Other Platforms

You can also deploy the backend to:
- **Heroku**: Use the included `Procfile`
- **Railway**: Connect your GitHub repo and Railway will auto-detect
- **Render**: Create a web service with the included configuration
- **Self-hosted server**: Follow the self-hosted deployment instructions in the backend README

#### Option 3: Use a Pre-deployed Backend

If you have access to an existing backend API, you can use that URL for the `NEXT_PUBLIC_API_URL` variable.

### Backend Environment Variables

When deploying the backend, ensure you set these environment variables:

- `DATABASE_URL`: Database connection string (e.g., `postgresql://user:pass@host/db` or `sqlite:///todos.db`)
- `SECRET_KEY`: Secure secret key for JWT authentication (at least 32 characters)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (e.g., `https://your-frontend.vercel.app,https://yourdomain.com`)
- `ALGORITHM`: JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: `30`)

## Configuration Details

### vercel.json

The project already includes a `vercel.json` file configured for Next.js deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": {
        "serverless": true
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}
```

### next.config.mjs

The project includes API proxying configuration:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  // Apply rewrites in both development and production
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/:path*`,
      },
    ];
  },
};

export default nextConfig;
```

## Troubleshooting

### Common Issues

1. **API Connection Issues**: Make sure your `NEXT_PUBLIC_API_URL` environment variable is correctly set to your backend API URL.

2. **CORS Errors**: Ensure your backend API has proper CORS configuration to allow requests from your frontend domain.

3. **Build Failures**: Check that all dependencies are properly listed in `package.json`.

### Verifying Your Deployment

After deployment:

1. Visit your deployed frontend URL
2. Check the browser console for any errors
3. Verify that the API connection status indicator shows "connected"
4. Test creating, updating, and deleting todos

## Post-Deployment

Once deployed, you can manage your application through the Vercel dashboard where you can:

- View deployment logs
- Rollback to previous versions
- Configure custom domains
- Set up SSL certificates
- Monitor performance
- Configure advanced settings

## Updating Your Deployment

To update your deployed application:

1. Make changes to your code
2. Commit and push to your Git repository
3. Vercel will automatically build and deploy the new version (if Git integration is set up)
4. Or redeploy manually using the CLI: `vercel --prod`

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel for GitHub Integration](https://vercel.com/docs/concepts/git)