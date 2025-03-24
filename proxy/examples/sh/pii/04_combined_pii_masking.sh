#!/bin/bash

# Combined PII Masking Example
# This script demonstrates a combination of PII masking techniques

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

echo "=== Combined PII Masking Example ==="
echo "This example demonstrates a combination of PII masking techniques:"
echo "1. Masking PII before sending to LLMs"
echo "2. Masking PII in logs"
echo "3. Comparing responses with and without PII masking"
echo ""
echo "Using API key: $API_KEY"
echo ""

# Text with various PII examples - all on one line to avoid JSON formatting issues
PII_TEXT="Hello, my name is Michael Brown. My email is michael.brown@example.com and my phone number is +1 (888) 555-1234. My SSN is 444-55-6666 and my credit card number is 6011-0000-0000-0000. I live at 101 Maple Drive, Somewhere, WA 98765 and my IP address is 192.0.2.1. My passport number is GH1122334 and my date of birth is 07/04/1985."

echo "Original text with PII:"
echo "$PII_TEXT"
echo ""

# First request: No PII masking before LLM
echo "1. Sending request WITHOUT PII masking before LLM..."
echo ""

curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-Before-LLM: 0" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant. Respond briefly."},
      {"role": "user", "content": "'"$PII_TEXT"'"}
    ]
  }' | jq '.choices[0].message.content' -r

echo ""
echo "2. Sending request WITH PII masking before LLM..."
echo ""

# Second request: With PII masking before LLM
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant. Respond briefly."},
      {"role": "user", "content": "'"$PII_TEXT"'"}
    ]
  }' | jq '.choices[0].message.content' -r

echo ""
echo "Note: Compare the two responses above."
echo "In the first response, the LLM may reference the PII directly."
echo "In the second response, the LLM should only see masked PII placeholders."
echo ""
echo "Both requests should have PII masked in the server logs."
echo "Check the server logs to confirm PII masking behavior."
echo ""
echo "=== Example Completed ==="