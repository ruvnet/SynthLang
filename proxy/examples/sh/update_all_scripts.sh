#!/bin/bash

# Update all scripts with improved API key handling
# This script updates all example scripts with improved API key handling

# Set the directory containing the example scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# API key handling code to insert
API_KEY_CODE='# Check if API_KEY is set
if [ -z "$API_KEY" ]; then
    # Try to create a new API key
    echo "API_KEY not found in environment variables. Creating a new one..."
    NEW_KEY=$(python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env)
    if [[ $NEW_KEY == *"API key created successfully"* ]]; then
        export API_KEY=$(echo "$NEW_KEY" | grep -o '"'"'sk_[a-f0-9]*'"'"')
        echo "Created and using API key: $API_KEY"
    else
        echo "Error: Failed to create API key"
        echo "Please run: python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env"
        exit 1
    fi
fi

echo "Using API key: $API_KEY"
echo ""'

# Update each script except this one and run_all_examples.sh
for script in "$SCRIPT_DIR"/*.sh; do
    # Skip this script and run_all_examples.sh
    if [[ "$script" == "$SCRIPT_DIR/update_all_scripts.sh" || "$script" == "$SCRIPT_DIR/run_all_examples.sh" ]]; then
        continue
    fi
    
    # Replace the API key check section
    sed -i '/# Check if API_KEY is set/,/fi/c\'"$API_KEY_CODE" "$script"
    
    echo "Updated $script"
done

echo "All scripts updated successfully!"