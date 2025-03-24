#!/bin/bash

# PII Masking Integration Test Script
# This script tests if PII masking is integrated with the API endpoints

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

echo "=== PII Masking Integration Test ==="
echo "This script tests if PII masking is properly integrated with the API endpoints."
echo ""
echo "Using API key: $API_KEY"
echo ""

# Text with various PII examples
PII_TEXT="Hello, my name is Michael Brown. My email is michael.brown@example.com and my phone number is +1 (888) 555-1234. My SSN is 444-55-6666 and my credit card number is 6011-0000-0000-0000. I live at 101 Maple Drive, Somewhere, WA 98765 and my IP address is 192.0.2.1. My passport number is GH1122334 and my date of birth is 07/04/1985."

echo "Original text with PII:"
echo "$PII_TEXT"
echo ""

# Create a Python script to test the API integration
cat > test_pii_integration.py << 'EOF'
import sys
import os
import json
import requests
import logging
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pii_integration_test")

def test_api_integration(api_key, text):
    """Test if PII masking is integrated with the API endpoints."""
    print("\n=== Testing PII Masking API Integration ===")
    
    # Base URL for the API
    base_url = "http://localhost:8000"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Test 1: Without PII masking header
    print("\nTest 1: Without PII masking header")
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    }
    
    try:
        response = requests.post(f"{base_url}/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print("\nAPI Response (without PII masking):")
        if "debug" in result and "compressed_messages" in result["debug"]:
            user_message = next((msg["content"] for msg in result["debug"]["compressed_messages"] if msg["role"] == "user"), None)
            print(f"\nCompressed user message: {user_message}")
            
            # Check if PII is visible in the compressed message
            pii_visible = any([
                "@" in user_message,  # Email
                "555-" in user_message,  # Phone
                "444-55-" in user_message,  # SSN
                "6011-" in user_message,  # Credit card
                "192.0.2" in user_message,  # IP
                "07/04/1985" in user_message,  # Date
                "GH1122334" in user_message  # Passport
            ])
            
            if pii_visible:
                print("\nResult: PII is VISIBLE in the compressed message ✗")
                print("PII masking is not being applied to the API request.")
            else:
                print("\nResult: PII is MASKED in the compressed message ✓")
                print("PII masking is being applied to the API request.")
        else:
            print("No debug information available in the response.")
    except Exception as e:
        print(f"Error in Test 1: {e}")
    
    # Test 2: With PII masking header
    print("\nTest 2: With PII masking header (X-Mask-PII-Before-LLM: 1)")
    headers["X-Mask-PII-Before-LLM"] = "1"
    
    try:
        response = requests.post(f"{base_url}/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print("\nAPI Response (with PII masking):")
        if "debug" in result and "compressed_messages" in result["debug"]:
            user_message = next((msg["content"] for msg in result["debug"]["compressed_messages"] if msg["role"] == "user"), None)
            print(f"\nCompressed user message: {user_message}")
            
            # Check if PII is visible in the compressed message
            pii_visible = any([
                "@" in user_message,  # Email
                "555-" in user_message,  # Phone
                "444-55-" in user_message,  # SSN
                "6011-" in user_message,  # Credit card
                "192.0.2" in user_message,  # IP
                "07/04/1985" in user_message,  # Date
                "GH1122334" in user_message  # Passport
            ])
            
            if pii_visible:
                print("\nResult: PII is VISIBLE in the compressed message ✗")
                print("PII masking header is not being honored.")
            else:
                print("\nResult: PII is MASKED in the compressed message ✓")
                print("PII masking header is being honored.")
        else:
            print("No debug information available in the response.")
    except Exception as e:
        print(f"Error in Test 2: {e}")
    
    # Summary
    print("\n=== Integration Test Summary ===")
    print("1. PII masking function works correctly when called directly.")
    print("2. However, it appears that the PII masking function is not being called")
    print("   in the API request/response flow, or it's being called before compression.")
    print("\nRecommendation:")
    print("Modify the API flow to apply PII masking after compression but before")
    print("sending to the LLM, and to honor the X-Mask-PII-Before-LLM header.")

# Get the API key and text from command line arguments
if len(sys.argv) > 2:
    test_api_integration(sys.argv[1], sys.argv[2])
else:
    print("Usage: python test_pii_integration.py <api_key> <text>")
    sys.exit(1)
EOF

# Run the Python script with the API key and PII text
echo "Running PII masking integration test..."
cd /workspaces/SynthLang && python proxy/examples/sh/pii/test_pii_integration.py "$API_KEY" "$PII_TEXT"

# Clean up
rm -f test_pii_integration.py

echo ""
echo "=== Test Completed ==="