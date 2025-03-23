#!/bin/bash

# Prompt Management Example
# This script demonstrates how to use the prompt management endpoints

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Prompt Management Example"
echo "This example demonstrates how to save, load, list, delete, and compare prompts."
echo "The prompt management endpoints allow you to store and retrieve prompts for later use."
echo "This is useful for maintaining a library of effective prompts."
echo ""

# Define a prompt name and content
PROMPT_NAME="database-overview-$(date +%s)"
PROMPT_CONTENT="Provide a comprehensive overview of database management systems, including their types (relational, NoSQL, graph, etc.), key features, common use cases, and popular implementations. Include brief explanations of fundamental concepts like ACID properties, indexing, transactions, and normalization. Conclude with recent trends in database technology."

# Define metadata
CATEGORY="technology"
AUTHOR="test_user"
TAGS="database,technology,overview"
TAGS_JSON=$(echo "$TAGS" | sed 's/,/","/g')
TAGS_JSON="[\"$TAGS_JSON\"]"

echo "Prompt name: $PROMPT_NAME"
echo "Prompt content (truncated): ${PROMPT_CONTENT:0:100}..."
echo "Category: $CATEGORY"
echo "Author: $AUTHOR"
echo "Tags: $TAGS"
echo ""

# 1. Save a prompt
echo "1. Saving prompt..."
echo ""

SAVE_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "'"$PROMPT_NAME"'",
    "prompt": "'"$PROMPT_CONTENT"'",
    "metadata": {
      "category": "'"$CATEGORY"'",
      "author": "'"$AUTHOR"'",
      "tags": '"$TAGS_JSON"'
    }
  }')

echo "Save Response:"
print_json "$SAVE_RESPONSE"

# Extract prompt ID
PROMPT_ID=$(echo "$SAVE_RESPONSE" | jq -r '.id')
echo ""
echo "Prompt saved with ID: $PROMPT_ID"
echo ""

# 2. List prompts
echo "2. Listing prompts..."
echo ""

LIST_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/synthlang/prompts/list" \
  -H "Authorization: Bearer $API_KEY")

echo "List Response:"
print_json "$LIST_RESPONSE"

# Count prompts
PROMPT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.count')
echo ""
echo "Found $PROMPT_COUNT prompts"
echo ""

# 3. Load a prompt
echo "3. Loading prompt..."
echo ""

LOAD_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/load" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "'"$PROMPT_NAME"'"
  }')

echo "Load Response:"
print_json "$LOAD_RESPONSE"

# Extract loaded prompt
LOADED_PROMPT=$(echo "$LOAD_RESPONSE" | jq -r '.prompt')
CREATED_AT=$(echo "$LOAD_RESPONSE" | jq -r '.created_at')
UPDATED_AT=$(echo "$LOAD_RESPONSE" | jq -r '.updated_at')

echo ""
echo "Loaded prompt: ${LOADED_PROMPT:0:100}..."
echo "Created at: $CREATED_AT"
echo "Updated at: $UPDATED_AT"
echo ""

# 4. Save a second version of the prompt
PROMPT_NAME_V2="${PROMPT_NAME}-v2"
PROMPT_CONTENT_V2="${PROMPT_CONTENT} Also discuss cloud-based database services and serverless database options."

echo "4. Saving second version of prompt..."
echo ""

SAVE_V2_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "'"$PROMPT_NAME_V2"'",
    "prompt": "'"$PROMPT_CONTENT_V2"'",
    "metadata": {
      "category": "'"$CATEGORY"'",
      "author": "'"$AUTHOR"'",
      "tags": '"$TAGS_JSON"'
    }
  }')

echo "Save V2 Response:"
print_json "$SAVE_V2_RESPONSE"
echo ""

# 5. Compare prompts
echo "5. Comparing prompts..."
echo ""

COMPARE_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/compare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name1": "'"$PROMPT_NAME"'",
    "name2": "'"$PROMPT_NAME_V2"'"
  }')

echo "Compare Response:"
print_json "$COMPARE_RESPONSE"

# Extract comparison metrics
SIMILARITY_SCORE=$(echo "$COMPARE_RESPONSE" | jq -r '.metrics.similarity_score')
TOKEN_DIFFERENCE=$(echo "$COMPARE_RESPONSE" | jq -r '.metrics.token_difference')

echo ""
echo "Similarity score: $SIMILARITY_SCORE"
echo "Token difference: $TOKEN_DIFFERENCE"
echo ""

# 6. Delete prompts
echo "6. Deleting prompts..."
echo ""

DELETE_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "'"$PROMPT_NAME"'"
  }')

echo "Delete Response for $PROMPT_NAME:"
print_json "$DELETE_RESPONSE"
echo ""

DELETE_V2_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/prompts/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "'"$PROMPT_NAME_V2"'"
  }')

echo "Delete Response for $PROMPT_NAME_V2:"
print_json "$DELETE_V2_RESPONSE"
echo ""

echo "Prompt management operations completed successfully."

print_footer