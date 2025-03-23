#!/bin/bash

# List Models Example
# This script demonstrates how to list available models

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "List Models Example"
echo "This example demonstrates how to list all available models in the SynthLang Proxy API."
echo "The models endpoint returns information about the models that can be used for completions."
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/models..."
echo ""

RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/models" \
  -H "Authorization: Bearer $API_KEY")

echo "Response:"
print_json "$RESPONSE"

# Extract and display model information
echo ""
echo "Available Models:"
echo "$RESPONSE" | jq -r '.data[] | "- " + .id + " (Owner: " + .owned_by + ")"'

print_footer