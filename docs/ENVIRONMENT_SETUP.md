# Environment Setup Guide

## Overview

This guide provides step-by-step instructions for setting up the environment variables required for the Todo App Chatbot - Phase III project. Proper environment configuration is essential for the application to function correctly.

## Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed for the backend
- Node.js 18+ installed for the frontend
- Access to required external services (Neon DB, OpenAI, etc.)

## Backend Environment Setup

### Step 1: Navigate to Backend Directory

```bash
cd /path/to/your/project/backend
```

### Step 2: Create the .env File

Copy the example environment file:

```bash
cp .env.example .env
```

### Step 3: Configure Database (Neon PostgreSQL)

1. **Sign up for Neon**:
   - Go to [Neon.tech](https://neon.tech)
   - Create a free account

2. **Create a Project**:
   - Log into your Neon dashboard
   - Click "New Project"
   - Choose your region and PostgreSQL version
   - Give your project a name (e.g., "todo-chatbot-db")

3. **Get Connection String**:
   - In your project dashboard, find the connection details
   - Copy the connection string in the format: `postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require`
   - Replace the `DATABASE_URL` in your `.env` file with this connection string

### Step 4: Configure OpenAI 

1. **Get API Key**:
   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Sign in to your account
   - Click "Create new secret key"
   - Copy the generated key (starts with `sk-`)

2. **Set Environment Variable**:
   - Replace `your-super-secret-jwt-key-here-make-it-long-and-random` with your actual key in the `.env` file

### Step 5: Configure JWT Secret Key

1. **Generate Secure Key**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set Environment Variable**:
   - Replace `your-super-secret-jwt-key-here-make-it-long-and-random` with the generated key

### Step 6: Configure Better Auth

1. **Generate Secret**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set Environment Variables**:
   - Replace `your-better-auth-secret-here-make-it-long-and-random` with the generated key
   - Set `BETTER_AUTH_URL` to your application URL (default: `http://localhost:3000`)

### Step 7: Configure CSRF Secret

1. **Generate Secure Key**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set Environment Variable**:
   - Replace `your-csrf-secret-key-here-make-it-long-and-random` with the generated key

## Frontend Environment Setup

### Step 1: Navigate to Frontend Directory

```bash
cd /path/to/your/project/frontend
```

### Step 2: Create the .env.local File

Copy the example environment file:

```bash
cp .env.local.example .env.local
```

### Step 3: Configure API URL

1. **Set Backend API URL**:
   - For development: `NEXT_PUBLIC_API_URL=http://localhost:8000`
   - For production: `NEXT_PUBLIC_API_URL=https://yourdomain.com`

### Step 4: Configure OpenAI

1. **Use Same Key as Backend**:
   - Use the same OpenAI API key you obtained for the backend
   - Set `NEXT_PUBLIC_OPENAI_API_KEY=sk-your-openai-api-key-here`

### Step 5: Configure Better Auth URL

1. **Set Auth URL**:
   - For development: `NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000`
   - For production: `NEXT_PUBLIC_BETTER_AUTH_URL=https://yourdomain.com`

### Step 6: Configure OpenAI Domain

1. **Set OpenAI Domain**:
   - For standard OpenAI API: `NEXT_PUBLIC_OPENAI_DOMAIN=https://api.openai.com`
   - This is used for ChatKit integration

## Complete Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens (32+ chars) | `random-string-generated-with-secrets-module` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-your-api-key-here` |
| `BETTER_AUTH_SECRET` | Secret for Better Auth (32+ chars) | `random-string-generated-with-secrets-module` |
| `BETTER_AUTH_URL` | Auth service URL | `http://localhost:3000` |
| `APP_ENV` | Environment mode | `development` |
| `LOG_LEVEL` | Logging level | `info` |
| `SERVER_HOST` | Server host | `0.0.0.0` |
| `SERVER_PORT` | Server port | `8000` |
| `MCP_SERVER_URL` | MCP server URL | `http://localhost:8000` |
| `CSRF_SECRET_KEY` | CSRF protection key (32+ chars) | `random-string-generated-with-secrets-module` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_OPENAI_API_KEY` | OpenAI API key | `sk-your-api-key-here` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Auth service URL | `http://localhost:3000` |
| `NEXT_PUBLIC_APP_ENV` | Environment mode | `development` |
| `NEXT_PUBLIC_OPENAI_DOMAIN` | OpenAI domain | `https://api.openai.com` |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | Enable analytics | `false` |
| `NEXT_PUBLIC_MAINTENANCE_MODE` | Maintenance mode | `false` |

## Validation and Testing

### Backend Validation

Run the configuration validation:

```bash
cd backend
python -m backend.config
```

This will check all required environment variables and provide helpful error messages if any are missing or incorrectly formatted.

### Frontend Validation

During development, the configuration is automatically validated when the app starts. Look for console messages indicating the configuration status.

## Common Issues and Solutions

### Issue: "DATABASE_URL environment variable is required"

**Solution**:
1. Verify you have created a Neon PostgreSQL database
2. Check that the connection string format is correct
3. Ensure the connection string starts with `postgresql://` or `postgres://`

### Issue: "JWT_SECRET_KEY should be at least 32 characters long"

**Solution**:
1. Generate a new key using the secrets module: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
2. Replace the JWT_SECRET_KEY with the new value

### Issue: "OPENAI_API_KEY should start with 'sk-' prefix"

**Solution**:
1. Verify you have copied the correct API key from OpenAI dashboard
2. Ensure the key starts with `sk-`
3. Check for any leading or trailing whitespace

### Issue: "Invalid credentials" for Neon Database

**Solution**:
1. Check your Neon dashboard for the correct username and password
2. Verify the connection string format
3. Ensure SSL mode is set to `require` for Neon

### Issue: "Network error" connecting to API

**Solution**:
1. Verify the backend server is running
2. Check that the API URL in frontend matches the backend server URL
3. Ensure ports are not blocked by firewall

## Development vs Production

### Development Configuration

For development, use:
- `APP_ENV=development`
- Local URLs (e.g., `http://localhost:8000`)
- Lower security requirements for testing

### Production Configuration

For production, ensure:
- `APP_ENV=production`
- HTTPS URLs for all services
- Strong, randomly generated secret keys
- Proper SSL certificates
- Environment variables stored securely (not in version control)

## Security Best Practices

1. **Never commit .env files** to version control
2. **Use strong, randomly generated secrets** (at least 32 characters)
3. **Rotate API keys** periodically
4. **Use environment-specific configurations** for different deployment stages
5. **Store sensitive information** in secure vaults when possible
6. **Validate all environment variables** at application startup

## Troubleshooting Tips

1. **Check file permissions**: Ensure `.env` files are readable by your application
2. **Verify variable names**: Environment variables are case-sensitive
3. **Look for typos**: Double-check all configuration values
4. **Review documentation**: Refer to the respective service documentation for correct format
5. **Check network connectivity**: Ensure your application can reach external services

## Next Steps

Once your environment is configured:

1. Start the backend: `cd backend && python -m uvicorn main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Visit your application in the browser
4. Verify all functionality works as expected

Remember to restart your applications after making changes to environment variables.