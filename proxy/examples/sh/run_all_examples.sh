#!/bin/bash

# Run all examples
# This script runs all the example scripts in sequence

# Set the directory containing the example scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/*.sh

# Check if the proxy server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: The proxy server is not running."
    echo "Please start the server with: cd /workspaces/SynthLang/proxy && python -m src.app.main"
    exit 1
fi

# Check if API key exists
if [ -z "$API_KEY" ]; then
    echo "No API_KEY found in environment. Creating one..."
    cd /workspaces/SynthLang/proxy
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

echo "========================================================"
echo "SynthLang Proxy API Examples"
echo "========================================================"
echo "This script will run all example scripts in sequence."
echo "Each example demonstrates different features of the SynthLang Proxy API."
echo "Press Ctrl+C at any time to stop the execution."
echo "========================================================"
echo ""

# Function to run a script with a pause after
run_example() {
    echo "========================================================"
    echo "Running example: $1"
    echo "========================================================"
    "$SCRIPT_DIR/$1"
    
    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "Warning: Example $1 may have encountered an error."
    fi
    
    echo ""
    echo "Press Enter to continue to the next example..."
    read
    echo ""
}

# Run each example script in order
run_example "01_simple_chat.sh"
run_example "02_gpt4o_mini_example.sh"
run_example "03_o3_mini_example.sh"
run_example "04_streaming_example.sh"
run_example "05_weather_tool_example.sh"
run_example "06_calculator_tool_example.sh"
run_example "07_compression_example.sh"
run_example "08_gzip_compression_example.sh"
run_example "09_hashtag_directive_example.sh"
run_example "10_function_calling_example.sh"
run_example "11_complex_example.sh"

echo "========================================================"
echo "All examples completed!"
echo "========================================================"