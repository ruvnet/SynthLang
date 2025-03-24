#!/bin/bash

# Logarithmic compression example
# This script demonstrates using the new logarithmic symbolic compression

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

echo "=== Logarithmic Symbolic Compression Example ==="
echo "This example demonstrates using the new logarithmic symbolic compression."
echo "This advanced compression technique combines multiple strategies:"
echo "- Breaking text into logical chunks"
echo "- Replacing common phrases with symbols"
echo "- Applying logarithmic compression to repetitive patterns"
echo "- Formatting text in a more compact representation"
echo ""

# Create a complex system message to demonstrate compression benefits
SYSTEM_MESSAGE="You are an AI assistant specialized in data analysis and visualization. Your task is to help users understand complex datasets, identify patterns, and create meaningful visualizations. You should follow these guidelines: 1) Always ask for clarification about the data structure if it's not clear, 2) Suggest appropriate visualization types based on the data characteristics, 3) Explain your reasoning for choosing specific visualization approaches, 4) Provide code examples when relevant using Python libraries like matplotlib, seaborn, or plotly, 5) Consider the audience's technical level when explaining concepts."

USER_MESSAGE="I have a dataset with customer information including age, income, purchase history, and satisfaction scores. What would be the best way to visualize relationships between these variables to identify key factors affecting customer satisfaction?"

# Make the API request with high compression level
echo "Making request with high compression level (includes logarithmic compression)..."
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "'"$SYSTEM_MESSAGE"'"},
      {"role": "user", "content": "'"$USER_MESSAGE"'"}
    ],
    "synthlang_compression_level": "high"
  }' | jq

echo ""
echo "=== Example Completed ==="