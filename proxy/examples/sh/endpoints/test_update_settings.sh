#!/bin/bash

# Test script for PUT /v1/keywords/settings endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Testing PUT /v1/keywords/settings Endpoint"
echo "This script tests the endpoint that updates keyword detection settings."
echo ""

# Use the admin API key if available
if [ -n "$ADMIN_API_KEY" ]; then
    echo "Using admin API key for authentication"
    TEST_API_KEY="$ADMIN_API_KEY"
else
    echo "Admin API key not found, using regular API key"
    TEST_API_KEY="$API_KEY"
fi

# Step 1: Get current settings
echo "Step 1: Getting current keyword detection settings..."
echo ""

CURRENT_SETTINGS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

# Check if there was an error
if echo "$CURRENT_SETTINGS_RESPONSE" | jq -e '.error' > /dev/null; then
    echo "Error: $(echo "$CURRENT_SETTINGS_RESPONSE" | jq -r '.error.message')"
    echo "Failed to get current settings. Exiting."
    print_footer
    exit 1
fi

# Extract current settings
CURRENT_DETECTION_ENABLED=$(echo "$CURRENT_SETTINGS_RESPONSE" | jq -r '.settings.enable_detection')
CURRENT_DETECTION_THRESHOLD=$(echo "$CURRENT_SETTINGS_RESPONSE" | jq -r '.settings.detection_threshold')

echo "Current Settings:"
echo "- Detection enabled: $CURRENT_DETECTION_ENABLED"
echo "- Detection threshold: $CURRENT_DETECTION_THRESHOLD"
echo ""

# Step 2: Update settings
echo "Step 2: Updating keyword detection settings..."
echo ""

# Define new settings
# Toggle the current detection enabled value
if [ "$CURRENT_DETECTION_ENABLED" = "true" ]; then
    NEW_DETECTION_ENABLED=false
else
    NEW_DETECTION_ENABLED=true
fi

# Modify the threshold slightly
if (( $(echo "$CURRENT_DETECTION_THRESHOLD < 0.5" | bc -l) )); then
    NEW_DETECTION_THRESHOLD=0.8
else
    NEW_DETECTION_THRESHOLD=0.4
fi

echo "New Settings:"
echo "- Detection enabled: $NEW_DETECTION_ENABLED"
echo "- Detection threshold: $NEW_DETECTION_THRESHOLD"
echo ""

UPDATE_SETTINGS_RESPONSE=$(curl -s -X PUT \
  "${API_BASE_URL}/v1/keywords/settings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_API_KEY" \
  -d '{
    "enable_detection": '"$NEW_DETECTION_ENABLED"',
    "detection_threshold": '"$NEW_DETECTION_THRESHOLD"'
  }')

echo "Update Settings Response:"
print_json "$UPDATE_SETTINGS_RESPONSE"

# Check if there was an error
if echo "$UPDATE_SETTINGS_RESPONSE" | jq -e '.error' > /dev/null; then
    echo ""
    echo "Error: $(echo "$UPDATE_SETTINGS_RESPONSE" | jq -r '.error.message')"
    echo "This endpoint requires admin privileges."
    print_footer
    exit 1
fi

# Extract and display updated fields
UPDATED_FIELDS=$(echo "$UPDATE_SETTINGS_RESPONSE" | jq -r '.updated_fields | join(", ")')
TIMESTAMP=$(echo "$UPDATE_SETTINGS_RESPONSE" | jq -r '.timestamp')

echo ""
echo "Updated fields: $UPDATED_FIELDS"
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 3: Verify settings were updated
echo "Step 3: Verifying settings were updated by getting current settings again..."
echo ""

UPDATED_SETTINGS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/keywords/patterns" \
  -H "Authorization: Bearer $TEST_API_KEY")

# Extract updated settings
UPDATED_DETECTION_ENABLED=$(echo "$UPDATED_SETTINGS_RESPONSE" | jq -r '.settings.enable_detection')
UPDATED_DETECTION_THRESHOLD=$(echo "$UPDATED_SETTINGS_RESPONSE" | jq -r '.settings.detection_threshold')

echo "Updated Settings:"
echo "- Detection enabled: $UPDATED_DETECTION_ENABLED"
echo "- Detection threshold: $UPDATED_DETECTION_THRESHOLD"
echo ""

# Verify the updates were applied
echo "Verification:"
if [ "$UPDATED_DETECTION_ENABLED" = "$NEW_DETECTION_ENABLED" ]; then
    echo "✅ Detection enabled was updated correctly"
else
    echo "❌ Detection enabled was not updated correctly"
    echo "  Expected: $NEW_DETECTION_ENABLED"
    echo "  Actual: $UPDATED_DETECTION_ENABLED"
fi

if (( $(echo "$UPDATED_DETECTION_THRESHOLD == $NEW_DETECTION_THRESHOLD" | bc -l) )); then
    echo "✅ Detection threshold was updated correctly"
else
    echo "❌ Detection threshold was not updated correctly"
    echo "  Expected: $NEW_DETECTION_THRESHOLD"
    echo "  Actual: $UPDATED_DETECTION_THRESHOLD"
fi

# Step 4: Restore original settings
echo ""
echo "Step 4: Restoring original settings..."
echo ""

RESTORE_SETTINGS_RESPONSE=$(curl -s -X PUT \
  "${API_BASE_URL}/v1/keywords/settings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_API_KEY" \
  -d '{
    "enable_detection": '"$CURRENT_DETECTION_ENABLED"',
    "detection_threshold": '"$CURRENT_DETECTION_THRESHOLD"'
  }')

if echo "$RESTORE_SETTINGS_RESPONSE" | jq -e '.error' > /dev/null; then
    echo "Error: $(echo "$RESTORE_SETTINGS_RESPONSE" | jq -r '.error.message')"
    echo "Failed to restore original settings."
else
    echo "✅ Original settings were successfully restored."
fi

print_footer