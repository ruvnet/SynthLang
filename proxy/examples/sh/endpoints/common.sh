#!/bin/bash

# Common utility functions for SynthLang Proxy API examples

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

# Base URL for the API
API_BASE_URL=${API_BASE_URL:-"http://localhost:8000"}

# Check if API_KEY is set
if [ -z "$API_KEY" ]; then
    # Try to create a new API key
    echo "API_KEY not found in environment variables. Creating a new one..."
    NEW_KEY=$(cd /workspaces/SynthLang/proxy && python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env)
    if [[ $NEW_KEY == *"API key created successfully"* ]]; then
        export API_KEY=$(echo "$NEW_KEY" | grep -o 'sk_[a-f0-9]*')
        echo "Created and using API key: $API_KEY"
    else
        echo "Error: Failed to create API key"
        echo "Please run: python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env"
        exit 1
    fi
fi

# Function to print section headers
print_header() {
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

# Function to print section footers
print_footer() {
    echo ""
    echo "============================================================"
    echo "Example completed"
    echo "============================================================"
}

# Function to print JSON in a readable format
print_json() {
    echo "$1" | jq '.'
}

# Function to check if the API server is running
check_api_server() {
    if ! curl -s "${API_BASE_URL}/health" > /dev/null; then
        echo "Error: The SynthLang Proxy API server is not running."
        echo "Please start the server with: cd /workspaces/SynthLang/proxy && python -m src.app.main"
        exit 1
    fi
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Warning: jq is not installed. JSON output will not be formatted."
    # Define a simple function to just echo the input if jq is not available
    print_json() {
        echo "$1"
    }
fi

# Check if the API server is running
check_api_server