#!/bin/bash

# Completions (Legacy) Example
# This script demonstrates how to use the legacy completions endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Completions (Legacy) Example"
echo "This example demonstrates how to create a completion using the legacy endpoint."
echo "The completions endpoint generates text based on a prompt without conversation history."
echo "This is compatible with older OpenAI API integrations."
echo ""

# Define the model to use
MODEL=${1:-"gpt-4o-mini"}
echo "Using model: $MODEL"
echo ""

# Define the prompt
PROMPT="Write a short story that begins with: Once upon a time in Silicon Valley,"

echo "Prompt: $PROMPT"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/completions..."
echo ""

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "'"$MODEL"'",
    "prompt": "'"$PROMPT"'",
    "temperature": 0.7,
    "max_tokens": 150,
    "use_synthlang": true
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the generated text
GENERATED_TEXT=$(echo "$RESPONSE" | jq -r '.choices[0].text')
TOKENS_USED=$(echo "$RESPONSE" | jq -r '.usage.total_tokens')

echo ""
echo "Generated text:"
echo "$GENERATED_TEXT"
echo ""
echo "Total tokens used: $TOKENS_USED"

print_footer