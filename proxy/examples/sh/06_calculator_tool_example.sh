#!/bin/bash

# Calculator tool example
# This script demonstrates using the calculator tool through keyword detection

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

echo "=== Calculator Tool Example ==="
echo "This example demonstrates using the calculator tool through keyword detection."
echo "The system will detect the calculation query and automatically invoke the calculator tool."
echo "The tool will perform the calculation and return the result."
echo ""

# Make the API request
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "o3-mini",
    "messages": [
      {"role": "user", "content": "Calculate 15% of 85.50"}
    ]
  }' | jq

echo ""
echo "=== Example Completed ==="