#!/bin/bash

# SynthLang Translation Example
# This script demonstrates how to use the SynthLang translation endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "SynthLang Translation Example"
echo "This example demonstrates how to translate natural language to SynthLang format."
echo "The translation endpoint converts natural language descriptions into SynthLang symbolic notation."
echo "This is useful for creating more efficient and precise prompts."
echo ""

# Define the text to translate
TEXT=${1:-"Create a chatbot that helps users with programming questions"}

# Define optional instructions
INSTRUCTIONS=${2:-""}

echo "Text to translate: $TEXT"
if [ -n "$INSTRUCTIONS" ]; then
    echo "Instructions: $INSTRUCTIONS"
fi
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/synthlang/translate..."
echo ""

REQUEST_BODY='{
    "text": "'"$TEXT"'"'

if [ -n "$INSTRUCTIONS" ]; then
    REQUEST_BODY="${REQUEST_BODY}, \"instructions\": \"$INSTRUCTIONS\""
else
    REQUEST_BODY="${REQUEST_BODY}, \"instructions\": null"
fi

REQUEST_BODY="${REQUEST_BODY} }"

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/translate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$REQUEST_BODY")

echo "Response:"
print_json "$RESPONSE"

# Extract and display the translation
SOURCE=$(echo "$RESPONSE" | jq -r '.source')
TARGET=$(echo "$RESPONSE" | jq -r '.target')
EXPLANATION=$(echo "$RESPONSE" | jq -r '.explanation')

echo ""
echo "Original text: $SOURCE"
echo "SynthLang translation: $TARGET"
echo "Explanation: $EXPLANATION"

print_footer