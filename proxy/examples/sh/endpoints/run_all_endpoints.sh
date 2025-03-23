#!/bin/bash

# Run All Endpoints Examples
# This script runs all the endpoint example scripts in sequence

# Set the directory containing the example scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/*.sh

# Check if the API server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: The SynthLang Proxy API server is not running."
    echo "Please start the server with: cd /workspaces/SynthLang/proxy && python -m src.app.main"
    exit 1
fi

echo "========================================================"
echo "SynthLang Proxy API Endpoints Examples"
echo "========================================================"
echo "This script will run all endpoint example scripts in sequence."
echo "Each example demonstrates different endpoints of the SynthLang Proxy API."
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
run_example "01_health_check.sh"
run_example "02_list_models.sh"
run_example "03_chat_completions.sh"
run_example "04_streaming_chat_completions.sh"
run_example "05_completions_legacy.sh"
run_example "06_synthlang_translate.sh"
run_example "07_system_prompt_generation.sh"
run_example "08_prompt_optimization.sh"
run_example "09_prompt_evolution.sh"
run_example "10_prompt_classification.sh"
run_example "11_prompt_management.sh"
run_example "12_cache_management.sh"
run_example "13_agent_tools.sh"
run_example "14_keyword_pattern_management.sh"

echo "========================================================"
echo "All endpoint examples completed!"
echo "========================================================"