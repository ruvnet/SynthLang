#!/bin/bash

# Prompt Optimization Example
# This script demonstrates how to use the prompt optimization endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Prompt Optimization Example"
echo "This example demonstrates how to optimize a prompt for clarity, specificity, and efficiency."
echo "The optimize endpoint takes a basic prompt and improves it through multiple iterations."
echo "This helps create more effective prompts that yield better results from language models."
echo ""

# Define the prompt to optimize
PROMPT=${1:-"Tell me about databases"}

# Define the maximum number of iterations
MAX_ITERATIONS=${2:-3}

echo "Original prompt: $PROMPT"
echo "Maximum iterations: $MAX_ITERATIONS"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/synthlang/optimize..."
echo ""

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/optimize" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "prompt": "'"$PROMPT"'",
    "max_iterations": '"$MAX_ITERATIONS"'
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the optimized prompt
ORIGINAL=$(echo "$RESPONSE" | jq -r '.original')
OPTIMIZED=$(echo "$RESPONSE" | jq -r '.optimized')
IMPROVEMENTS=$(echo "$RESPONSE" | jq -r '.improvements | join("\n- ")')
ORIGINAL_TOKENS=$(echo "$RESPONSE" | jq -r '.metrics.original_tokens')
OPTIMIZED_TOKENS=$(echo "$RESPONSE" | jq -r '.metrics.optimized_tokens')
CLARITY_SCORE=$(echo "$RESPONSE" | jq -r '.metrics.clarity_score')
SPECIFICITY_SCORE=$(echo "$RESPONSE" | jq -r '.metrics.specificity_score')
ITERATIONS=$(echo "$RESPONSE" | jq -r '.metrics.iterations')

echo ""
echo "Original prompt: $ORIGINAL"
echo ""
echo "Optimized prompt:"
echo "------------------------------------------------------------------------------"
echo "$OPTIMIZED"
echo "------------------------------------------------------------------------------"
echo ""
echo "Improvements made:"
echo "- $IMPROVEMENTS"
echo ""
echo "Metrics:"
echo "- Original tokens: $ORIGINAL_TOKENS"
echo "- Optimized tokens: $OPTIMIZED_TOKENS"
echo "- Clarity score: $CLARITY_SCORE"
echo "- Specificity score: $SPECIFICITY_SCORE"
echo "- Iterations performed: $ITERATIONS"

print_footer