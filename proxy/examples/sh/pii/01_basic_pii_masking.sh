#!/bin/bash

# Basic PII Masking Example
# This script demonstrates the basic PII masking functionality in SynthLang Proxy

# Set the directory containing the example scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Source the common functions if available
if [ -f "$PARENT_DIR/common.sh" ]; then
    source "$PARENT_DIR/common.sh"
else
    echo "Common functions not found. Using default settings."
    API_KEY=${API_KEY:-"your_api_key"}
    PROXY_URL=${PROXY_URL:-"http://localhost:8000"}
fi

# Define a message with PII
MESSAGE="Hello, my name is John Doe. My email is john.doe@example.com and my phone number is (555) 123-4567. 
My credit card number is 4111-1111-1111-1111 and my SSN is 123-45-6789. 
I live at 123 Main Street, Anytown, CA 12345 and my IP address is 192.168.1.1."

echo "========================================================"
echo "SynthLang Proxy - Basic PII Masking Example"
echo "========================================================"
echo "This example demonstrates the basic PII masking functionality."
echo "The following message contains various types of PII:"
echo ""
echo "$MESSAGE"
echo ""
echo "Sending request to SynthLang Proxy with PII masking enabled..."
echo "========================================================"

# Make the API request with PII masking headers
curl -s -X POST "${PROXY_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant. When you see placeholders like <EMAIL_ADDRESS>, <PHONE_NUMBER>, etc., explain that these are PII that have been masked."},
      {"role": "user", "content": "'"$MESSAGE"'"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
  }' | jq .

echo ""
echo "========================================================"
echo "PII Masking Results"
echo "========================================================"
echo "The request was sent with the X-Mask-PII-Before-LLM and X-Mask-PII-In-Logs headers."
echo "If PII masking is working correctly:"
echo "1. The LLM should have received the message with PII replaced by placeholders"
echo "2. The logs should not contain any of the original PII"
echo "3. The response should mention the masked PII placeholders"
echo ""
echo "Check the proxy logs to verify that PII was masked in the logs."
echo "========================================================"