#!/bin/bash

# PII Masking Before LLM Example
# This script demonstrates how to enable PII masking before sending to LLMs

# Load environment variables
if [ -f "../../../.env" ]; then
    export $(grep -v '^#' ../../../.env | xargs)
elif [ -f "../../.env" ]; then
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

echo "=== PII Masking Before LLM Example ==="
echo "This example demonstrates how to enable PII masking before sending to LLMs."
echo "It temporarily sets MASK_PII_BEFORE_LLM=1 for this request."
echo ""
echo "Using API key: $API_KEY"
echo ""

# Text with various PII examples - all on one line to avoid JSON formatting issues
PII_TEXT="Hello, my name is Jane Doe. My email is jane.doe@example.com and my phone number is (555) 987-6543. My SSN is 987-65-4321 and my credit card number is 5555-5555-5555-4444. I live at 456 Oak Avenue, Somewhere, NY 54321 and my IP address is 10.0.0.1. My passport number is CD7654321 and my date of birth is 05/20/1990."

echo "Original text with PII:"
echo "$PII_TEXT"
echo ""
echo "Sending request to API with PII text and MASK_PII_BEFORE_LLM=1..."
echo ""

# Make the API request with the header to enable PII masking before LLM
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant. When you see masked PII in the user message, point it out and explain what was masked."},
      {"role": "user", "content": "'"$PII_TEXT"'"}
    ]
  }' | jq

echo ""
echo "Note: The PII in the request should be masked before being sent to the LLM."
echo "The LLM should see placeholders like <EMAIL_ADDRESS>, <PHONE_NUMBER>, etc."
echo "Check the server logs to confirm PII was masked."
echo ""
echo "=== Example Completed ==="