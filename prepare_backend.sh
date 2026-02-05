#!/bin/bash
# Script to prepare backend for Hugging Face deployment

echo "Preparing backend for Hugging Face Spaces deployment..."

# Create a directory for the deployment package
mkdir -p hf_backend_deployment
cd hf_backend_deployment

# Copy the essential backend files
cp -r ../fullstack-todo-backend/* .

# Verify we have the necessary files
echo "Files prepared for Hugging Face deployment:"
ls -la

echo ""
echo "Deployment Instructions:"
echo "1. Create a new GitHub repository with these files"
echo "2. Go to https://huggingface.co/spaces and create a new space"
echo "3. Select 'Docker' SDK and use Git integration pointing to your GitHub repo"
echo "4. Your backend will be deployed at: https://your-username-your-space-name.hf.space"
echo ""
echo "The backend is already configured with:"
echo "- Dockerfile for containerization"
echo "- space.yaml for Hugging Face configuration"
echo "- Default secrets for demo deployment"
echo "- Port 7860 exposed (Hugging Face default)"