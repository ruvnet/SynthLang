#!/bin/bash

# Test script for JSON validation issues
# This script tests the API's handling of special characters in JSON content

# Source common utilities
source "$(dirname "$0")/endpoints/common.sh"

print_header "Testing JSON validation with special characters"

# Test 1: Basic request with direct model name
echo "Test 1: Basic request with direct model name"
curl -s -X POST "${API_BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "messages": [
      {"role": "user", "content": "What model are you? Please respond with just the model name."}
    ]
  }' | print_json

echo -e "\n\n"

# Test 2: Request with nested JSON but escaping < characters
echo "Test 2: Request with nested JSON but escaping < characters"
curl -s -X POST "${API_BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "{\n    \"model\": \"claude-3-7-sonnet-latest\",\n    \"messages\": [\n      {\"role\": \"user\", \"content\": \"What model are you? Please respond with just the model name. Avoid using \\u003c characters.\"}\n    ]\n  }"}
    ]
  }' | print_json

echo -e "\n\n"

# Test 3: Request with content containing <plan> tag
echo "Test 3: Request with content containing <plan> tag"
curl -s -X POST "${API_BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "messages": [
      {"role": "user", "content": "Create a plan for me. Use <plan> tags."}
    ]
  }' | print_json

echo -e "\n\n"

# Test 4: Request with content containing XML-like syntax
echo "Test 4: Request with content containing XML-like syntax"
curl -s -X POST "${API_BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "<plan>This is a test plan</plan>"}
    ]
  }' | print_json

print_footer