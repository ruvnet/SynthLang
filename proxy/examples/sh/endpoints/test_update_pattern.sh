#!/bin/bash

# Test script for PUT /v1/keywords/patterns/{name} endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing PUT /v1/keywords/patterns/{name} Endpoint"
echo "This script tests the endpoint that updates an existing keyword pattern."
echo ""

# Use the admin API key if available
if [ -n "$ADMIN_API_KEY" ]; then
    echo "Using admin API key for authentication"
    TEST_API_KEY="$ADMIN_API_KEY"
else
    echo "Admin API key not found, using regular API key"
    TEST_API_KEY="$API_KEY"
fi

# First, create a test pattern to update
PATTERN_NAME="test_update_pattern_$(date +%s)"
PATTERN_REGEX="(?:find|locate|search for)\\\\s+(?:a|the)?\\\\s*(?:file|document)\\\\s+(?:named|called|with name)?\\\\s+(?P<filename>.+)"
TOOL_NAME="file_search"
DESCRIPTION="Test pattern for file search queries"
PRIORITY=85
REQUIRED_ROLE="basic"
ENABLED=true

echo "Step 1: Creating a test pattern to update..."
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

# Define the updates
NEW_DESCRIPTION="Updated test pattern for file search queries"
NEW_PRIORITY=90
NEW_ENABLED=false

echo "Step 2: Updating the pattern..."
echo ""
echo "Updates:"
echo "- Description: $NEW_DESCRIPTION"
echo "- Priority: $NEW_PRIORITY"
echo "- Enabled: $NEW_ENABLED"
echo ""

UPDATE_RESPONSE=$(curl -s -X PUT \
  "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_API_KEY" \
  -d '{
    "description": "'"$NEW_DESCRIPTION"'",
    "priority": '"$NEW_PRIORITY"',
    "enabled": '"$NEW_ENABLED"'
  }')

echo "Update Pattern Response:"
print_json "$UPDATE_RESPONSE"

# Check if there was an error
if echo "$UPDATE_RESPONSE" | jq -e '.error' > /dev/null; then
    echo ""
    echo "Error: $(echo "$UPDATE_RESPONSE" | jq -r '.error.message')"
    echo "This endpoint requires admin privileges."
    
    # Clean up by deleting the test pattern
    echo ""
    echo "Cleaning up by deleting the test pattern..."
    curl -s -X DELETE \
      "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
      -H "Authorization: Bearer $TEST_API_KEY" > /dev/null
    
    print_footer
    exit 1
fi

# Extract and display updated fields
UPDATED_FIELDS=$(echo "$UPDATE_RESPONSE" | jq -r '.updated_fields | join(", ")')
TIMESTAMP=$(echo "$UPDATE_RESPONSE" | jq -r '.timestamp')

echo ""
echo "Updated fields: $UPDATED_FIELDS"
echo "Timestamp: $TIMESTAMP"
echo ""

# Verify the pattern was updated by listing all patterns
echo "Step 3: Verifying pattern was updated by listing all patterns..."
echo ""

PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

# Extract the updated pattern
UPDATED_PATTERN=$(echo "$PATTERNS_RESPONSE" | jq -r '.patterns[] | select(.name == "'"$PATTERN_NAME"'")')

echo "Updated Pattern Details:"
echo "$UPDATED_PATTERN" | jq '.'
echo ""

# Verify the updates were applied
CURRENT_DESCRIPTION=$(echo "$UPDATED_PATTERN" | jq -r '.description')
CURRENT_PRIORITY=$(echo "$UPDATED_PATTERN" | jq -r '.priority')
CURRENT_ENABLED=$(echo "$UPDATED_PATTERN" | jq -r '.enabled')

echo "Verification:"
if [ "$CURRENT_DESCRIPTION" = "$NEW_DESCRIPTION" ]; then
    echo "✅ Description was updated correctly"
else
    echo "❌ Description was not updated correctly"
    echo "  Expected: $NEW_DESCRIPTION"
    echo "  Actual: $CURRENT_DESCRIPTION"
fi

if [ "$CURRENT_PRIORITY" = "$NEW_PRIORITY" ]; then
    echo "✅ Priority was updated correctly"
else
    echo "❌ Priority was not updated correctly"
    echo "  Expected: $NEW_PRIORITY"
    echo "  Actual: $CURRENT_PRIORITY"
fi

if [ "$CURRENT_ENABLED" = "$NEW_ENABLED" ]; then
    echo "✅ Enabled flag was updated correctly"
else
    echo "❌ Enabled flag was not updated correctly"
    echo "  Expected: $NEW_ENABLED"
    echo "  Actual: $CURRENT_ENABLED"
fi

# Clean up by deleting the test pattern
echo ""
echo "Step 4: Cleaning up by deleting the test pattern..."
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