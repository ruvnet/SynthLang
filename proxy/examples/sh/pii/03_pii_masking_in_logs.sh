#!/bin/bash

# PII Masking in Logs Example
# This script demonstrates how PII masking works in logs

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

echo "=== PII Masking in Logs Example ==="
echo "This example demonstrates how PII is masked in server logs."
echo "It ensures MASK_PII_IN_LOGS=1 for this request."
echo ""
echo "Using API key: $API_KEY"
echo ""

# Text with various PII examples - all on one line to avoid JSON formatting issues
PII_TEXT="Hello, my name is Robert Johnson. My email is robert.johnson@example.com and my phone number is 123-456-7890. My SSN is 111-22-3333 and my credit card number is 3333-3333-3333-3333. I live at 789 Pine Street, Somewhere, TX 67890 and my IP address is 172.16.0.1. My passport number is EF9876543 and my date of birth is 11/30/1975."

echo "Original text with PII:"
echo "$PII_TEXT"
echo ""
echo "Sending request to API with PII text and ensuring MASK_PII_IN_LOGS=1..."
echo ""

# Make the API request with the header to ensure PII masking in logs
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "'"$PII_TEXT"'"}
    ]
  }' | jq

echo ""
echo "Note: The PII in the request should be masked in the server logs."
echo "Check the server logs to confirm PII was masked."
echo "The log entries should contain placeholders like <EMAIL_ADDRESS>, <PHONE_NUMBER>, etc."
echo ""
echo "=== Example Completed ==="