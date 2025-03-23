#!/bin/bash

# Function calling example
# This script demonstrates using function calling with parameters

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
    # Try to create a new API key
    echo "API_KEY not found in environment variables. Creating a new one..."
    NEW_KEY=$(python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env)
    if [[ $NEW_KEY == *"API key created successfully"* ]]; then
        export API_KEY=$(echo "$NEW_KEY" | grep -o 'sk_[a-f0-9]*')
        echo "Created and using API key: $API_KEY"
    else
        echo "Error: Failed to create API key"
        echo "Please run: python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env"
        exit 1
    fi
fi

echo "Using API key: $API_KEY"
echo ""

echo "=== Function Calling Example ==="
echo "This example demonstrates using function calling with parameters."
echo "The #calculator directive allows you to call the calculator tool with an expression parameter."
echo "This provides precise control over tool invocation with explicit parameter passing."
echo ""

# Make the API request
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "o3-mini",
    "messages": [
      {"role": "user", "content": "#calculator Calculate 15% of 85.50 + 25"}
    ]
  }' | jq

echo ""
echo "=== Example Completed ==="