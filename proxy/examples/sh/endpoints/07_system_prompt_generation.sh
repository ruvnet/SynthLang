#!/bin/bash

# System Prompt Generation Example
# This script demonstrates how to use the system prompt generation endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "System Prompt Generation Example"
echo "This example demonstrates how to generate a system prompt from a task description."
echo "The generate endpoint creates a well-crafted system prompt based on a high-level task description."
echo "This is useful for creating effective prompts without manual engineering."
echo ""

# Define the task description
TASK_DESCRIPTION=${1:-"Create a system prompt for a chatbot that helps with programming"}

echo "Task description: $TASK_DESCRIPTION"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/synthlang/generate..."
echo ""

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "task_description": "'"$TASK_DESCRIPTION"'"
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the generated prompt
PROMPT=$(echo "$RESPONSE" | jq -r '.prompt')
RATIONALE=$(echo "$RESPONSE" | jq -r '.rationale')
TOKENS=$(echo "$RESPONSE" | jq -r '.metadata.tokens')
MODEL=$(echo "$RESPONSE" | jq -r '.metadata.model')

echo ""
echo "Generated System Prompt:"
echo "------------------------------------------------------------------------------"
echo "$PROMPT"
echo "------------------------------------------------------------------------------"
echo ""
echo "Rationale: $RATIONALE"
echo ""
echo "Tokens: $TOKENS"
echo "Model used: $MODEL"

print_footer