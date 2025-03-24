#!/bin/bash

# Test script for POST /v1/keywords/patterns endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing POST /v1/keywords/patterns Endpoint"
echo "This script tests the endpoint that creates a new keyword pattern."
echo ""

# Use the admin API key if available
if [ -n "$ADMIN_API_KEY" ]; then
    echo "Using admin API key for authentication"
    TEST_API_KEY="$ADMIN_API_KEY"
else
    echo "Admin API key not found, using regular API key"
    TEST_API_KEY="$API_KEY"
fi

# Define the new pattern
PATTERN_NAME="test_pattern_$(date +%s)"
PATTERN_REGEX="(?:find|locate|search for)\\\\s+(?:a|the)?\\\\s*(?:file|document)\\\\s+(?:named|called|with name)?\\\\s+(?P<filename>.+)"
TOOL_NAME="file_search"
DESCRIPTION="Test pattern for file search queries"
PRIORITY=85
REQUIRED_ROLE="basic"
ENABLED=true

echo "New Pattern:"
echo "- Name: $PATTERN_NAME"
echo "- Regex: $PATTERN_REGEX"
echo "- Tool: $TOOL_NAME"
echo "- Description: $DESCRIPTION"
echo "- Priority: $PRIORITY"
echo "- Required role: $REQUIRED_ROLE"
echo "- Enabled: $ENABLED"
echo ""

# Create the new pattern
echo "Creating new pattern..."
echo ""

ADD_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_API_KEY" \
  -d '{
    "name": "'"$PATTERN_NAME"'",
    "pattern": "'"$PATTERN_REGEX"'",
    "tool": "'"$TOOL_NAME"'",
    "description": "'"$DESCRIPTION"'",
    "priority": '"$PRIORITY"',
    "required_role": "'"$REQUIRED_ROLE"'",
    "enabled": '"$ENABLED"'
  }')

echo "Add Pattern Response:"
print_json "$ADD_RESPONSE"

# Check if there was an error
if echo "$ADD_RESPONSE" | jq -e '.error' > /dev/null; then
    echo ""
    echo "Error: $(echo "$ADD_RESPONSE" | jq -r '.error.message')"
    echo "This endpoint requires admin privileges."
    print_footer
    exit 1
fi

# Extract and display pattern information
CREATED_PATTERN=$(echo "$ADD_RESPONSE" | jq -r '.pattern')
TIMESTAMP=$(echo "$ADD_RESPONSE" | jq -r '.timestamp')

echo ""
echo "Pattern created successfully at timestamp: $TIMESTAMP"
echo ""

# Verify the pattern was created by listing all patterns
echo "Verifying pattern was created by listing all patterns..."
echo ""

PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

# Check if the pattern exists in the list
PATTERN_EXISTS=$(echo "$PATTERNS_RESPONSE" | jq -r '.patterns[] | select(.name == "'"$PATTERN_NAME"'") | .name')

if [ -n "$PATTERN_EXISTS" ]; then
    echo "✅ Pattern '$PATTERN_NAME' was successfully created and verified."
else
    echo "❌ Pattern '$PATTERN_NAME' was not found in the patterns list."
fi

# Clean up by deleting the test pattern
echo ""
echo "Cleaning up by deleting the test pattern..."
echo ""

DELETE_RESPONSE=$(curl -s -X DELETE \
  "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
  -H "Authorization: Bearer $TEST_API_KEY")

SUCCESS=$(echo "$DELETE_RESPONSE" | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    echo "✅ Pattern '$PATTERN_NAME' was successfully deleted."
else
    echo "❌ Failed to delete pattern '$PATTERN_NAME'."
fi

print_footer