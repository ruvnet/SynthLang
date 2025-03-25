#!/bin/bash
# Script to install Fly.io CLI and deploy the SynthLang Proxy

set -e  # Exit on any error

echo "=== Installing Fly.io CLI and deploying SynthLang Proxy ==="

# Check if we're in the proxy directory
if [ ! -f "Dockerfile" ] || [ ! -f "fly.toml" ]; then
    echo "Error: This script must be run from the proxy directory"
    echo "Current directory: $(pwd)"
    echo "Please run: cd proxy && ./install_flyctl.sh"
    exit 1
fi

# Install Fly.io CLI if not already installed
if ! command -v flyctl &> /dev/null; then
    echo "Installing Fly.io CLI..."
    curl -L https://fly.io/install.sh | sh
    
    # Add Fly.io to PATH for the current session
    export FLYCTL_INSTALL="/home/$USER/.fly"
    export PATH="$FLYCTL_INSTALL/bin:$PATH"
    
    # Add Fly.io to PATH permanently
    echo 'export FLYCTL_INSTALL="/home/$USER/.fly"' >> ~/.bashrc
    echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' >> ~/.bashrc
    
    echo "Fly.io CLI installed successfully"
else
    echo "Fly.io CLI is already installed"
fi

# Log in to Fly.io if not already logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "Please log in to Fly.io:"
    flyctl auth login
else
    echo "Already logged in to Fly.io"
fi

# Create the app if it doesn't exist
if ! flyctl apps list | grep -q "synthlang-proxy"; then
    echo "Creating Fly.io app 'synthlang-proxy'..."
    flyctl apps create synthlang-proxy
else
    echo "App 'synthlang-proxy' already exists"
fi

# Create a volume for persistent data if it doesn't exist
if ! flyctl volumes list | grep -q "synthlang_data"; then
    echo "Creating volume 'synthlang_data'..."
    flyctl volumes create synthlang_data --size 1 --region iad
else
    echo "Volume 'synthlang_data' already exists"
fi

# Set OpenAI API key as a secret if provided
if [ -n "$OPENAI_API_KEY" ]; then
    echo "Setting OpenAI API key as a secret..."
    flyctl secrets set OPENAI_API_KEY="$OPENAI_API_KEY"
else
    echo "Warning: OPENAI_API_KEY environment variable not set."
    echo "You can set it later with: flyctl secrets set OPENAI_API_KEY=your_key"
fi

# Deploy the application
echo "Deploying to Fly.io..."
flyctl deploy

echo "=== Deployment completed ==="
echo "Your application is now available at: https://synthlang-proxy.fly.dev"
echo "Check the logs with: flyctl logs -a synthlang-proxy"