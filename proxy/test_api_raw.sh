#!/bin/bash

# Test script for the API without using jq to process the output
# This helps identify issues with JSON validation

echo "Testing API with direct model name..."
curl -s -X POST "https://synthlang-proxy.fly.dev/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_103519b8a732e92c4cebaa6729d5bfac" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "messages": [
      {"role": "user", "content": "What model are you? Please respond with just the model name."}
    ]
  }'

echo -e "\n\nTesting API with nested JSON but escaping < characters..."
curl -s -X POST "https://synthlang-proxy.fly.dev/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_103519b8a732e92c4cebaa6729d5bfac" \
  -d '{
    "messages": [
      {"role": "user", "content": "{\n    \"model\": \"claude-3-7-sonnet-latest\",\n    \"messages\": [\n      {\"role\": \"user\", \"content\": \"What model are you? Please respond with just the model name. Avoid using \\u003c characters.\"}\n    ]\n  }"}
    ]
  }'

echo -e "\n\nTesting API with content containing <plan> tag..."
curl -s -X POST "https://synthlang-proxy.fly.dev/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_103519b8a732e92c4cebaa6729d5bfac" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "messages": [
      {"role": "user", "content": "Create a plan for me. Use <plan> tags."}
    ]
  }'