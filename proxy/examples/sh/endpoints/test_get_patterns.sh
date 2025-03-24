#!/bin/bash

# Test script for GET /v1/keywords/patterns endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing GET /v1/keywords/patterns Endpoint"
echo "This script tests the endpoint that lists all keyword patterns."
echo ""

# Use the admin API key if available
if [ -n "$ADMIN_API_KEY" ]; then
    echo "Using admin API key for authentication"
    TEST_API_KEY="$ADMIN_API_KEY"
else
    echo "Admin API key not found, using regular API key"
    TEST_API_KEY="$API_KEY"
fi

# List existing patterns
echo "Listing existing keyword patterns..."
echo ""

PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

echo "Patterns Response:"
print_json "$PATTERNS_RESPONSE"

# Check if there was an error
if echo "$PATTERNS_RESPONSE" | jq -e '.error' > /dev/null; then
    echo ""
    echo "Error: $(echo "$PATTERNS_RESPONSE" | jq -r '.error.message')"
    echo "This endpoint requires admin privileges."
    print_footer
    exit 1
fi

# Extract and display pattern information
PATTERN_COUNT=$(echo "$PATTERNS_RESPONSE" | jq -r '.count')
DETECTION_ENABLED=$(echo "$PATTERNS_RESPONSE" | jq -r '.settings.enable_detection')
DETECTION_THRESHOLD=$(echo "$PATTERNS_RESPONSE" | jq -r '.settings.detection_threshold')

echo ""
echo "Keyword Detection Settings:"
echo "- Detection enabled: $DETECTION_ENABLED"
echo "- Detection threshold: $DETECTION_THRESHOLD"
echo ""
echo "Existing Patterns ($PATTERN_COUNT):"
echo "$PATTERNS_RESPONSE" | jq -r '.patterns[] | "- " + .name + ": " + .description + " (Tool: " + .tool + ", Priority: " + (.priority|tostring) + ", Enabled: " + (.enabled|tostring) + ")"'
echo ""

print_footer