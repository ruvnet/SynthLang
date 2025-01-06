#!/bin/bash

# Exit on error
set -e

# Add Fly.io binary to PATH
export FLYCTL_INSTALL="/home/codespace/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"

# Destroy existing app
echo "Destroying existing app..."
flyctl apps destroy synthlang --yes

# Create new app
echo "Creating new app..."
flyctl apps create synthlang

# Build the project
echo "Building project..."
npm run build

# Deploy to Fly.io
echo "Deploying to Fly.io..."
flyctl deploy --app synthlang

echo "Deployment complete! Visit https://synthlang.fly.dev"
