#!/bin/bash
# Deploy script for SynthLang Proxy with forgiving validation

set -e  # Exit on error

echo "Deploying SynthLang Proxy with forgiving validation to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "flyctl not found, installing..."
    curl -L https://fly.io/install.sh | sh
    export FLYCTL_INSTALL="/home/$(whoami)/.fly"
    export PATH="$FLYCTL_INSTALL/bin:$PATH"
fi

# Verify flyctl is working
echo "Verifying flyctl installation..."
flyctl version

# Build and deploy the application
echo "Building and deploying application..."
cd "$(dirname "$0")"  # Ensure we're in the proxy directory

# Deploy to Fly.io
echo "Deploying to Fly.io..."
flyctl deploy --remote-only

echo "Deployment complete!"
echo "Your application is now running at https://synthlang-proxy.fly.dev"
echo ""
echo "To check the status of your application, run:"
echo "flyctl status -a synthlang-proxy"
echo ""
echo "To view logs, run:"
echo "flyctl logs -a synthlang-proxy"