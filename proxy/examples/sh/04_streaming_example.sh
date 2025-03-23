#!/bin/bash

# Streaming example
# This script demonstrates streaming responses from the API

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

echo "=== Streaming Response Example ==="
echo "This example demonstrates streaming responses from the API."
echo "You'll see the response come in chunks rather than all at once."
echo "This is useful for providing real-time feedback to users."
echo ""

# Make the API request
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Write a short story about a robot learning to feel emotions"}
    ],
    "stream": true
  }'

echo ""
echo ""
echo "=== Example Completed ==="