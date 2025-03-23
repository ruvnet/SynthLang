#!/bin/bash

# Check examples
# This script checks if all example scripts are working correctly

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
echo "SynthLang Proxy API Examples Check"
echo "========================================================"
echo "This script will check if all example scripts are working correctly."
echo "========================================================"
echo ""

# Array of example scripts
EXAMPLES=(
    "01_simple_chat.sh"
    "02_gpt4o_mini_example.sh"
    "03_o3_mini_example.sh"
    "04_streaming_example.sh"
    "05_weather_tool_example.sh"
    "06_calculator_tool_example.sh"
    "07_compression_example.sh"
    "08_gzip_compression_example.sh"
    "09_hashtag_directive_example.sh"
    "10_function_calling_example.sh"
    "11_complex_example.sh"
)

# Function to check if a script works
check_example() {
    echo "Checking $1..."
    OUTPUT=$("$SCRIPT_DIR/$1" 2>&1)
    
    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "❌ $1 failed to execute"
        return 1
    fi
    
    # Check if the output contains an error message
    if [[ $OUTPUT == *"error"* ]]; then
        echo "❌ $1 returned an error"
        return 1
    fi
    
    echo "✅ $1 is working correctly"
    return 0
}

# Check each example script
FAILED=0
for example in "${EXAMPLES[@]}"; do
    check_example "$example"
    if [ $? -ne 0 ]; then
        FAILED=$((FAILED+1))
    fi
done

echo ""
echo "========================================================"
if [ $FAILED -eq 0 ]; then
    echo "All examples are working correctly! ✅"
else
    echo "$FAILED examples failed the check. ❌"
fi
echo "========================================================"