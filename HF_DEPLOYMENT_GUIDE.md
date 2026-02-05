# Deploying the AI Chat Bot Backend on Hugging Face Spaces

## Overview

Your backend is located in the `hf_deployment` folder and is specifically configured for Hugging Face Spaces deployment.

## Ready-to-Deploy Files in `hf_deployment`:

- `space.yaml`: Configures the Hugging Face Space with title, emoji, and Docker SDK
- `Dockerfile`: Sets up the container environment and exposes port 7860
- `app_hf.py`: Entry point for Hugging Face Spaces with CORS middleware
- `requirements_hf.txt`: Python dependencies for Hugging Face
- `backend/`: The backend code with API endpoints, models, and database connection

## Deployment Steps:

### Option 1: Direct Upload to Hugging Face (Easy)

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Name**: Choose a unique name for your space
   - **SDK**: Select "Docker" (already configured!)
   - **Hardware**: Choose CPU (sufficient for this application)
   - **Repository Type**: Select "Upload to Hub" (for direct upload)
4. Download the `hf_deployment` folder contents as a ZIP file:
   ```bash
   cd hf_deployment
   zip -r hf_backend.zip . -x "*.git*" "__pycache__/*" "*.pyc"
   ```
5. Upload the ZIP file to your Hugging Face Space
6. Your backend will be deployed!

### Option 2: Git Integration (Recommended)

1. Create a new GitHub repository with the `hf_deployment` files:
   ```bash
   # Copy the hf_deployment folder to a new location
   cp -r hf_deployment ~/my-backend-repo

   # Initialize git in the new folder
   cd ~/my-backend-repo
   git init
   git add .
   git commit -m "Initial backend deployment"

   # Connect to your GitHub repository
   git remote add origin https://github.com/yourusername/your-backend-repo.git
   git push -u origin main
   ```

2. Create a Hugging Face Space with Git integration:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Fill in the details:
     - **Name**: Choose a unique name for your space
     - **SDK**: Select "Docker"
     - **Hardware**: Choose CPU
     - **Repository Type**: Select "Using Git integration"
     - **Repository URL**: Enter your GitHub repository URL

3. Complete the deployment:
   - After creating the space, Hugging Face will automatically start building
   - Monitor the build logs in the "Logs" tab of your space

## Access Your Deployment:

- Your backend API will be available at: `https://[your-username]-[your-space-name].hf.space`
- API Documentation: `https://[your-username]-[your-space-name].hf.space/docs`
- Health Check: `https://[your-username]-[your-space-name].hf.space/health`

## API Endpoints Available:

- `/docs` - Interactive API documentation
- `/conversations/` - Manage conversations
- `/conversations/{conversation_id}/messages` - Get conversation messages
- `/tasks/` - Manage tasks
- `/tasks/{user_id}` - Get user tasks
- `/health` - Health check endpoint

## Key Features:

- Automatic fallback configuration for demo deployment
- SQLite database for easy setup (no external DB required)
- CORS enabled for frontend integration
- JWT authentication ready
- Complete CRUD operations for conversations and tasks

## Troubleshooting:

- If build fails, check the Logs tab in your Hugging Face Space
- Make sure all files from the `hf_deployment` folder are included
- The Dockerfile is configured to run on port 7860 (Hugging Face default)

Your backend is ready for deployment! The `hf_deployment` folder contains everything needed for a successful Hugging Face Spaces deployment.