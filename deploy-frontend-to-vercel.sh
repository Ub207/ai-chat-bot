#!/bin/bash
# Vercel Deployment Script for Todo Frontend

set -e  # Exit on any error

echo "🚀 Starting Vercel deployment for Todo Frontend..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found in current directory"
    echo "💡 Please navigate to the frontend directory before running this script"
    exit 1
fi

echo "✅ Found package.json in current directory"

# Check if NEXT_PUBLIC_API_URL is set
if [ -z "$NEXT_PUBLIC_API_URL" ]; then
    echo "⚠️  WARNING: NEXT_PUBLIC_API_URL environment variable is not set"
    echo "💡 This is required for the frontend to connect to the backend API"
    echo "💡 Please set it before deployment:"
    echo "   export NEXT_PUBLIC_API_URL='https://your-backend-api.com/api'"
    echo ""

    read -p "Do you want to continue without setting the API URL? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Deployment cancelled"
        exit 1
    fi
fi

echo "🔧 Installing dependencies..."
npm install

echo "🧪 Running tests (if available)..."
if [ -f "package.json" ] && grep -q "test" package.json; then
    npm test || echo "⚠️  Tests failed, but continuing with deployment..."
else
    echo "⚠️  No tests found in package.json"
fi

echo "🔍 Checking for Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed"
    echo "💡 Install it with: npm install -g vercel"
    echo "💡 Or visit: https://vercel.com/cli"
    exit 1
fi

echo "✅ Vercel CLI is installed"

echo "🌐 Checking Vercel login status..."
if ! vercel whoami &> /dev/null; then
    echo "🔒 You are not logged in to Vercel"
    echo "💡 Please log in first: vercel login"
    exit 1
fi

echo "✅ Logged in to Vercel"

echo "📦 Building the application..."
npm run build

echo "🚀 Deploying to Vercel..."
if [ -n "$NEXT_PUBLIC_API_URL" ]; then
    vercel --env NEXT_PUBLIC_API_URL="$NEXT_PUBLIC_API_URL"
else
    vercel
fi

echo "🎉 Deployment completed!"
echo ""
echo "🔗 Your application should be available at the URL provided above"
echo ""
echo "📝 Remember to set the NEXT_PUBLIC_API_URL environment variable in Vercel dashboard if you didn't set it during deployment"