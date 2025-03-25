#!/bin/bash
# Script to redeploy the SynthLang Proxy to Fly.io

set -e  # Exit on any error

echo "=== Redeploying SynthLang Proxy to Fly.io ==="

# Check if we're in the proxy directory
if [ ! -f "Dockerfile" ] || [ ! -f "fly.toml" ]; then
    echo "Error: This script must be run from the proxy directory"
    echo "Current directory: $(pwd)"
    echo "Please run: cd proxy && ./redeploy.sh"
    exit 1
fi

# Deploy to Fly.io
echo "Deploying to Fly.io..."
flyctl deploy --app synthlang-proxy

echo "=== Deployment completed ==="
echo "Your application is now available at: https://synthlang-proxy.fly.dev"
echo "Check the logs with: flyctl logs -a synthlang-proxy"