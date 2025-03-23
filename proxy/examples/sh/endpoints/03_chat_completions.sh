#!/bin/bash

# Chat Completions Example
# This script demonstrates how to use the chat completions endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Chat Completions Example"
echo "This example demonstrates how to create a chat completion using the SynthLang Proxy API."
echo "The chat completions endpoint generates responses based on a conversation history."
echo ""

# Define the model to use
MODEL=${1:-"gpt-4o-mini"}
echo "Using model: $MODEL"
echo ""

# Define the system message
SYSTEM_MESSAGE="You are a helpful assistant specialized in explaining technical concepts in simple terms."

# Define the user message
USER_MESSAGE="Explain how quantum computing works in 3 sentences."

echo "System message: $SYSTEM_MESSAGE"
echo "User message: $USER_MESSAGE"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/chat/completions..."
echo ""

RESPONSE=$(curl -s -X POST \
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
    "use_synthlang": true
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the assistant's message
ASSISTANT_MESSAGE=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')
TOKENS_USED=$(echo "$RESPONSE" | jq -r '.usage.total_tokens')

echo ""
echo "Assistant's response:"
echo "$ASSISTANT_MESSAGE"
echo ""
echo "Total tokens used: $TOKENS_USED"

print_footer