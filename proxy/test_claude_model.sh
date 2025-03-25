#!/bin/bash

# Script to test if the Claude model selection is working correctly

# Set API key - replace with your actual API key or set it in your environment
API_KEY=${OPENAI_API_KEY:-"sk_a006079d291f135266b0a5c15d87cce5"}

echo "Testing Claude model selection..."
echo "Sending request to use claude-3-7-sonnet-latest model..."

# Send a request to the API
response=$(curl -s -X POST "http://127.0.0.1:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "claude-3-7-sonnet-latest",
    "messages": [
      {"role": "user", "content": "What model are you? Please respond with just the model name."}
    ]
  }')

# Extract the model name from the response
model=$(echo $response | jq -r '.model')
content=$(echo $response | jq -r '.choices[0].message.content')

echo "Response received:"
echo "Model reported in response: $model"
echo "Content: $content"

# Check if the model is correct
if [[ "$model" == "claude-3-7-sonnet-latest" ]]; then
  echo "✅ Success: The model name in the response is correct."
else
  echo "❌ Error: The model name in the response is not claude-3-7-sonnet-latest."
  echo "Full response:"
  echo "$response" | jq
fi

echo ""
echo "Testing nested JSON request format..."
echo "Sending request with nested JSON..."

# Send a request with nested JSON
nested_response=$(curl -s -X POST "http://127.0.0.1:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "messages": [
      {"role": "user", "content": "{\n    \"model\": \"claude-3-7-sonnet-latest\",\n    \"messages\": [\n      {\"role\": \"user\", \"content\": \"What model are you? Please respond with just the model name.\"}\n    ]\n  }"}
    ]
  }')

# Extract the model name from the nested response
nested_model=$(echo $nested_response | jq -r '.model')
nested_content=$(echo $nested_response | jq -r '.choices[0].message.content')

echo "Nested JSON response received:"
echo "Model reported in response: $nested_model"
echo "Content: $nested_content"

# Check if the model is correct for nested JSON
if [[ "$nested_model" == "claude-3-7-sonnet-latest" ]]; then
  echo "✅ Success: The model name in the nested JSON response is correct."
else
  echo "❌ Error: The model name in the nested JSON response is not claude-3-7-sonnet-latest."
  echo "Full response:"
  echo "$nested_response" | jq
fi