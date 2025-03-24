#!/bin/bash

# GPT-4o-mini example
# This script demonstrates using the gpt-4o-mini model

# Load environment variables
if [ -f "../../.env" ]; then
    export $(grep -v '^#' ../../.env | xargs)
elif [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if API_KEY is set
if [ -z "$API_KEY" ]; then
    echo "Error: API_KEY not found in environment variables"
    echo "Please run: python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env"
    exit 1
fi

echo "=== GPT-4o-mini Example ==="
echo "This example uses the gpt-4o-mini model, which is a smaller, faster version of GPT-4o."
echo "It's good for tasks that don't require the full capabilities of GPT-4o."
echo ""

# Make the API request
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Explain the concept of machine learning in simple terms"}
    ]
  }' | jq

echo ""
echo "=== Example Completed ==="