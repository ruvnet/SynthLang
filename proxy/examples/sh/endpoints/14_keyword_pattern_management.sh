#!/bin/bash

# Keyword Pattern Management Example
# This script demonstrates how to use the keyword pattern management endpoints

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Keyword Pattern Management Example"
echo "This example demonstrates how to manage keyword patterns for tool detection."
echo "The keyword pattern endpoints allow you to list, add, update, and delete patterns."
echo "Keyword patterns are used to automatically detect when to invoke tools based on user messages."
echo ""

# 1. List existing patterns
echo "1. Listing existing keyword patterns..."
echo ""

PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $API_KEY")

echo "Patterns Response:"
print_json "$PATTERNS_RESPONSE"

# Extract and display pattern information
PATTERN_COUNT=$(echo "$PATTERNS_RESPONSE" | jq -r '.count')
DETECTION_ENABLED=$(echo "$PATTERNS_RESPONSE" | jq -r '.settings.enable_detection')
DETECTION_THRESHOLD=$(echo "$PATTERNS_RESPONSE" | jq -r '.settings.detection_threshold')
DEFAULT_ROLE=$(echo "$PATTERNS_RESPONSE" | jq -r '.settings.default_role')

echo ""
echo "Keyword Detection Settings:"
echo "- Detection enabled: $DETECTION_ENABLED"
echo "- Detection threshold: $DETECTION_THRESHOLD"
echo "- Default role: $DEFAULT_ROLE"
echo ""
echo "Existing Patterns ($PATTERN_COUNT):"
echo "$PATTERNS_RESPONSE" | jq -r '.patterns[] | "- " + .name + ": " + .description + " (Tool: " + .tool + ", Priority: " + (.priority|tostring) + ", Enabled: " + (.enabled|tostring) + ")"'
echo ""

# 2. Add a new pattern
echo "2. Adding a new keyword pattern..."
echo ""

# Define the new pattern
PATTERN_NAME="stock_price_query"
PATTERN_REGEX="(?:what's|what is|get|check)\\\\s+(?:the)?\\\\s*(?:stock price|share price|stock value)\\\\s+(?:of|for)?\\\\s+(?P<ticker>[A-Z]+)"
TOOL_NAME="stock_price"
DESCRIPTION="Detects requests for stock price information"
PRIORITY=95
REQUIRED_ROLE="premium"
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

ADD_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
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
echo ""

# 3. Update the pattern
echo "3. Updating the keyword pattern..."
echo ""

# Define the updates
NEW_PRIORITY=97
NEW_ENABLED=false

echo "Updates:"
echo "- Priority: $NEW_PRIORITY"
echo "- Enabled: $NEW_ENABLED"
echo ""

UPDATE_RESPONSE=$(curl -s -X PUT \
  "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "priority": '"$NEW_PRIORITY"',
    "enabled": '"$NEW_ENABLED"'
  }')

echo "Update Pattern Response:"
print_json "$UPDATE_RESPONSE"

# Extract and display updated fields
UPDATED_FIELDS=$(echo "$UPDATE_RESPONSE" | jq -r '.updated_fields | join(", ")')
TIMESTAMP=$(echo "$UPDATE_RESPONSE" | jq -r '.timestamp')

echo ""
echo "Updated fields: $UPDATED_FIELDS"
echo "Timestamp: $TIMESTAMP"
echo ""

# 4. List patterns again to see the update
echo "4. Listing patterns again to verify update..."
echo ""

UPDATED_PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $API_KEY")

echo "Updated Patterns Response:"
print_json "$UPDATED_PATTERNS_RESPONSE"

# Find and display the updated pattern
echo ""
echo "Updated Pattern Details:"
echo "$UPDATED_PATTERNS_RESPONSE" | jq -r '.patterns[] | select(.name == "'"$PATTERN_NAME"'") | "- Name: " + .name + "\n- Tool: " + .tool + "\n- Priority: " + (.priority|tostring) + "\n- Enabled: " + (.enabled|tostring)'
echo ""

# 5. Update keyword detection settings
echo "5. Updating keyword detection settings..."
echo ""

# Define new settings
NEW_DETECTION_THRESHOLD=0.8

echo "New Settings:"
echo "- Detection threshold: $NEW_DETECTION_THRESHOLD"
echo ""

SETTINGS_RESPONSE=$(curl -s -X PUT \
  "${API_BASE_URL}/v1/keywords/settings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "detection_threshold": '"$NEW_DETECTION_THRESHOLD"'
  }')

echo "Update Settings Response:"
print_json "$SETTINGS_RESPONSE"
echo ""

# 6. Delete the pattern
echo "6. Deleting the keyword pattern..."
echo ""

DELETE_RESPONSE=$(curl -s -X DELETE \
  "${API_BASE_URL}/v1/keywords/patterns/${PATTERN_NAME}" \
  -H "Authorization: Bearer $API_KEY")

echo "Delete Pattern Response:"
print_json "$DELETE_RESPONSE"

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

# 7. List patterns one final time to confirm deletion
echo "7. Listing patterns one final time to confirm deletion..."
echo ""

FINAL_PATTERNS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $API_KEY")

echo "Final Patterns Response:"
print_json "$FINAL_PATTERNS_RESPONSE"

# Check if the pattern was deleted
FINAL_PATTERN_COUNT=$(echo "$FINAL_PATTERNS_RESPONSE" | jq -r '.count')
PATTERN_STILL_EXISTS=$(echo "$FINAL_PATTERNS_RESPONSE" | jq -r '.patterns[] | select(.name == "'"$PATTERN_NAME"'") | .name' 2>/dev/null)

echo ""
echo "Final Pattern Count: $FINAL_PATTERN_COUNT"
if [ -z "$PATTERN_STILL_EXISTS" ]; then
    echo "Pattern '$PATTERN_NAME' was successfully deleted."
else
    echo "Warning: Pattern '$PATTERN_NAME' still exists."
fi

print_footer