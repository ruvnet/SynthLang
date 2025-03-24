#!/bin/bash

# Prompt Classification Example
# This script demonstrates how to use the prompt classification endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Prompt Classification Example"
echo "This example demonstrates how to classify a prompt into categories."
echo "The classify endpoint analyzes a text and assigns it to the most relevant category."
echo "This is useful for routing prompts to specialized models or processing pipelines."
echo ""

# Define the text to classify
TEXT=${1:-"Write a function that calculates prime numbers"}

# Define the labels to classify against
LABELS=${2:-"code,math,algorithm,data science"}
# Convert comma-separated string to JSON array
LABELS_JSON=$(echo "$LABELS" | sed 's/,/","/g')
LABELS_JSON="[\"$LABELS_JSON\"]"

echo "Text to classify: $TEXT"
echo "Labels: $LABELS"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/synthlang/classify..."
echo ""

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/classify" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "text": "'"$TEXT"'",
    "labels": '"$LABELS_JSON"'
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the classification results
TEXT=$(echo "$RESPONSE" | jq -r '.text')
LABEL=$(echo "$RESPONSE" | jq -r '.label')
CONFIDENCE=$(echo "$RESPONSE" | jq -r '.confidence')
EXPLANATION=$(echo "$RESPONSE" | jq -r '.explanation')

# Extract all labels and scores
ALL_LABELS=$(echo "$RESPONSE" | jq -r '.all_labels | map(.label + " (" + (.score|tostring) + ")") | join(", ")')

echo ""
echo "Classification Results:"
echo "Text: $TEXT"
echo "Primary Label: $LABEL"
echo "Confidence: $CONFIDENCE"
echo ""
echo "All Labels with Scores: $ALL_LABELS"
echo ""
echo "Explanation: $EXPLANATION"

print_footer