#!/bin/bash

# Test script for DELETE /v1/keywords/patterns/{name} endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing DELETE /v1/keywords/patterns/{name} Endpoint"
echo "This script tests the endpoint that deletes a keyword pattern."
echo ""

# Use the admin API key if available
if [ -n "$ADMIN_API_KEY" ]; then
    echo "Using admin API key for authentication"
    TEST_API_KEY="$ADMIN_API_KEY"
else
    echo "Admin API key not found, using regular API key"
    TEST_API_KEY="$API_KEY"
fi

# First, create a test pattern to delete
PATTERN_NAME="test_delete_pattern_$(date +%s)"
PATTERN_REGEX="(?:find|locate|search for)\\\\s+(?:a|the)?\\\\s*(?:file|document)\\\\s+(?:named|called|with name)?\\\\s+(?P<filename>.+)"
TOOL_NAME="file_search"
DESCRIPTION="Test pattern for deletion"
PRIORITY=75
REQUIRED_ROLE="basic"
ENABLED=true

echo "Step 1: Creating a test pattern to delete..."
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

# Check if there was an error
if echo "$ADD_RESPONSE" | jq -e '.error' > /dev/null; then
    echo "Error: $(echo "$ADD_RESPONSE" | jq -r '.error.message')"
    echo "Failed to create test pattern. Exiting."
    print_footer
    exit 1
fi

echo "Test pattern created successfully:"
print_json "$ADD_RESPONSE"
echo ""

# Verify the pattern was created by listing all patterns
echo "Step 2: Verifying pattern was created by listing all patterns..."
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
    print_footer
    exit 1
fi

# Delete the pattern
echo ""
echo "Step 3: Deleting the pattern..."
echo ""

DELETE_RESPONSE=$(curl -s -X DELETE \
  "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
  -H "Authorization: Bearer $TEST_API_KEY")

echo "Delete Pattern Response:"
print_json "$DELETE_RESPONSE"

# Check if there was an error
if echo "$DELETE_RESPONSE" | jq -e '.error' > /dev/null; then
    echo ""
    echo "Error: $(echo "$DELETE_RESPONSE" | jq -r '.error.message')"
    echo "This endpoint requires admin privileges."
    print_footer
    exit 1
fi

# Extract and display deletion confirmation
SUCCESS=$(echo "$DELETE_RESPONSE" | jq -r '.success')
DELETED_NAME=$(echo "$DELETE_RESPONSE" | jq -r '.name')
DELETE_TIMESTAMP=$(echo "$DELETE_RESPONSE" | jq -r '.timestamp')

echo ""
echo "Deletion Results:"
echo "- Success: $SUCCESS"
echo "- Deleted pattern: $DELETED_NAME"
echo "- Timestamp: $DELETE_TIMESTAMP"
echo ""

# Verify the pattern was deleted by listing all patterns again
echo "Step 4: Verifying pattern was deleted by listing all patterns again..."
echo ""

FINAL_PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

# Check if the pattern still exists in the list
PATTERN_STILL_EXISTS=$(echo "$FINAL_PATTERNS_RESPONSE" | jq -r '.patterns[] | select(.name == "'"$PATTERN_NAME"'") | .name' 2>/dev/null)

if [ -z "$PATTERN_STILL_EXISTS" ]; then
    echo "✅ Pattern '$PATTERN_NAME' was successfully deleted and verified."
else
    echo "❌ Pattern '$PATTERN_NAME' still exists in the patterns list."
fi

print_footer