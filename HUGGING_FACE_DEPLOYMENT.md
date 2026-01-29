# Deploying Todo Backend on Hugging Face Spaces

This guide explains how to deploy the Todo backend application on Hugging Face Spaces.

## Prerequisites

- A Hugging Face account
- Git access to push code
- A repository containing the backend code

## Deployment Steps

### Option 1: Direct Upload (Using the Hugging Face Hub)

1. Create a new Space on Hugging Face:
   - Go to https://huggingface.co/new-space
   - Choose "Docker" SDK
   - Choose "CPUTiny" hardware (or higher based on your needs)

2. Upload the backend files to your Space repository:
   - Clone your Space repository locally
   - Copy all the files from the `/backend` folder to your Space repository
   - Push the changes to your Space repository

3. Configure the environment variables in your Space settings:
   - Go to your Space settings
   - Add the following environment variables:
     - `DATABASE_URL`: Your database connection string (e.g., `sqlite+aiosqlite:///todos.db` for SQLite)
     - `SECRET_KEY`: A long, random secret key for JWT tokens
     - `CORS_ORIGINS`: Comma-separated list of allowed origins (e.g., `https://yourdomain.hf.space,http://localhost:3000`)

### Option 2: Git-based Deployment

1. Initialize your Space with the files:
```bash
git clone https://huggingface.co/spaces/[your-username]/[space-name]
cd [space-name]
cp -r /path/to/backend/* .
git add .
git commit -m "Initial commit with Todo backend"
git push
```

2. The Space will automatically build and deploy using the Dockerfile.

### Option 3: Using Hugging Face CLI

1. Install the Hugging Face CLI:
```bash
pip install huggingface_hub
```

2. Log in to your account:
```bash
huggingface-cli login
```

3. Upload the files to your Space:
```bash
huggingface-cli upload [your-username]/[space-name] /path/to/backend/ . --repo-type space
```

## Required Files

Your Space repository should contain:

- `Dockerfile` - Defines the container environment
- `app.py` - Entry point for the application
- `requirements.txt` - Python dependencies
- `app/` directory - Contains the FastAPI application
- `space.yaml` - Hugging Face Space configuration (optional)
- `setup.sh` - Setup script (optional)

## Environment Variables

Set these in your Space settings under the "Secrets" tab:

- `DATABASE_URL`: Database connection string (e.g., `sqlite+aiosqlite:///todos.db`)
- `SECRET_KEY`: Secret key for JWT tokens (at least 32 characters)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `DEBUG`: Set to `false` for production (optional)

## API Access

Once deployed, your API will be available at:
- `https://[your-username]-[space-name].hf.space` - Main API
- `https://[your-username]-[space-name].hf.space/docs` - Interactive API documentation
- `https://[your-username]-[space-name].hf.space/health` - Health check

## Troubleshooting

1. **Build failures**: Check the build logs in your Space settings for dependency issues
2. **Runtime errors**: Check the runtime logs in your Space settings
3. **Database issues**: Make sure your database URL is properly configured
4. **CORS errors**: Verify your CORS_ORIGINS setting includes the Space URL

## Scaling Considerations

- For production use, consider using PostgreSQL instead of SQLite
- Monitor resource usage and upgrade hardware if needed
- Implement proper backup strategies for your database
- Consider using environment variables for sensitive configuration