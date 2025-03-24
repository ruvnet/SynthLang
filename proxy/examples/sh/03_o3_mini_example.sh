#!/bin/bash

# o3-mini example
# This script demonstrates using the o3-mini model

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

echo "=== o3-mini Example ==="
echo "This example uses the o3-mini model, which is a lightweight alternative to gpt-4o."
echo "It's optimized for speed and efficiency while maintaining good quality responses."
echo ""

# Make the API request
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "o3-mini",
    "messages": [
      {"role": "user", "content": "Write a short poem about artificial intelligence"}
    ]
  }' | jq

echo ""
echo "=== Example Completed ==="