#!/bin/bash

# Test script for all keyword pattern management endpoints

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing All Keyword Pattern Management Endpoints"
echo "This script runs all the tests for the keyword pattern management endpoints."
echo ""

# Function to run a test script and check its exit code
run_test() {
    local script_name="$1"
    local script_path="$SCRIPT_DIR/$script_name"
    
    echo "Running $script_name..."
    echo "----------------------------------------"
    
    # Run the script
    "$script_path"
    local exit_code=$?
    
    echo "----------------------------------------"
    if [ $exit_code -eq 0 ]; then
        echo "✅ $script_name completed successfully"
    else
        echo "❌ $script_name failed with exit code $exit_code"
    fi
    echo ""
    
    return $exit_code
}

# Run all the test scripts
TESTS=(
    "test_get_patterns.sh"
    "test_create_pattern.sh"
    "test_update_pattern.sh"
    "test_delete_pattern.sh"
    "test_update_settings.sh"
)

FAILED_TESTS=()

for test in "${TESTS[@]}"; do
    run_test "$test"
    if [ $? -ne 0 ]; then
        FAILED_TESTS+=("$test")
    fi
done

# Print summary
echo "Test Summary:"
echo "----------------------------------------"
echo "Total tests: ${#TESTS[@]}"
echo "Passed: $((${#TESTS[@]} - ${#FAILED_TESTS[@]}))"
echo "Failed: ${#FAILED_TESTS[@]}"

if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo ""
    echo "Failed tests:"
    for test in "${FAILED_TESTS[@]}"; do
        echo "- $test"
    done
    exit 1
else
    echo ""
    echo "All tests passed successfully!"
fi

print_footer