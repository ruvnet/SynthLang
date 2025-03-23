#!/bin/bash

# Health Check Example
# This script demonstrates how to use the health check endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Health Check Example"
echo "This example demonstrates how to check the health of the SynthLang Proxy API."
echo "The health check endpoint returns information about the service status and its components."
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/health..."
echo ""

RESPONSE=$(curl -s "${API_BASE_URL}/health")

echo "Response:"
print_json "$RESPONSE"

# Extract and display specific information
STATUS=$(echo "$RESPONSE" | jq -r '.status')
VERSION=$(echo "$RESPONSE" | jq -r '.version')
TIMESTAMP=$(echo "$RESPONSE" | jq -r '.timestamp')

echo ""
echo "Service Status: $STATUS"
echo "Version: $VERSION"
echo "Timestamp: $TIMESTAMP"

print_footer