#!/bin/bash

echo "🚀 MCP Experiments - GitHub + Vercel Deployment"
echo "================================================"
echo ""

# Check if repository is provided
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <github-username>"
    echo "Example: ./deploy.sh yourusername"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="MCP-Experiments"
GITHUB_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "📦 Preparing deployment..."
echo "GitHub: $GITHUB_URL"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run 'git init' first."
    exit 1
fi

# Add all files
echo "📝 Adding files to git..."
git add -A

# Commit if there are changes
if git diff --staged --quiet; then
    echo "✅ No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Prepare for deployment"
fi

# Add remote if not exists
if ! git remote | grep -q "origin"; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin $GITHUB_URL
else
    echo "✅ GitHub remote already exists"
    git remote set-url origin $GITHUB_URL
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin master --force

echo ""
echo "✅ Pushed to GitHub successfully!"
echo ""
echo "📱 Next steps:"
echo "1. Go to https://vercel.com"
echo "2. Click 'New Project'"
echo "3. Import: $GITHUB_URL"
echo "4. Click 'Deploy'"
echo ""
echo "🎉 Your app will be live in minutes!"
