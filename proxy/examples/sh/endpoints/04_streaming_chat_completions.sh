#!/bin/bash

# Streaming Chat Completions Example
# This script demonstrates how to use the streaming chat completions endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Streaming Chat Completions Example"
echo "This example demonstrates how to create a streaming chat completion using the SynthLang Proxy API."
echo "The streaming endpoint returns the response in chunks as they are generated."
echo "This provides a more interactive experience for users."
echo ""

# Define the model to use
MODEL=${1:-"gpt-4o-mini"}
echo "Using model: $MODEL"
echo ""

# Define the system message
SYSTEM_MESSAGE="You are a creative assistant that writes short poems."

# Define the user message
USER_MESSAGE="Write a short poem about artificial intelligence and nature."

echo "System message: $SYSTEM_MESSAGE"
echo "User message: $USER_MESSAGE"
echo ""

# Make the API request
echo "Making streaming request to ${API_BASE_URL}/v1/chat/completions..."
echo "Response will appear below as it's generated:"
echo "--------------------------------------------------------------"

curl -s -X POST \
  "${API_BASE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "'"$MODEL"'",
    "messages": [
      {"role": "system", "content": "'"$SYSTEM_MESSAGE"'"},
      {"role": "user", "content": "'"$USER_MESSAGE"'"}
    ],
    "temperature": 0.7,
    "max_tokens": 150,
    "stream": true,
    "use_synthlang": true
  }'

echo ""
echo "--------------------------------------------------------------"

print_footer