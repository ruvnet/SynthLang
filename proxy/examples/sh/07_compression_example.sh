#!/bin/bash

# SynthLang compression example
# This script demonstrates using SynthLang compression

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

echo "=== SynthLang Compression Example ==="
echo "This example demonstrates using SynthLang compression to reduce token usage."
echo "The system will automatically compress the messages before sending them to the model."
echo "This reduces token usage and costs while maintaining response quality."
echo ""

# Create a longer system message to demonstrate compression benefits
SYSTEM_MESSAGE="You are an AI assistant specialized in explaining complex technical concepts in simple terms."

# Make the API request
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "'"$SYSTEM_MESSAGE"'"},
      {"role": "user", "content": "Explain how quantum computing works"}
    ]
  }' | jq

echo ""
echo "=== Example Completed ==="