#!/bin/bash

# Agent Tools Example
# This script demonstrates how to use the agent tools endpoints

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Agent Tools Example"
echo "This example demonstrates how to list and call agent tools directly."
echo "The tools endpoints allow you to view available tools and call them without going through chat completions."
echo "This is useful for testing tools or integrating them into custom workflows."
echo ""

# 1. List available tools
echo "1. Listing available tools..."
echo ""

TOOLS_RESPONSE=$(curl -s -X GET \
  "${API_BASE_URL}/v1/tools" \
  -H "Authorization: Bearer $API_KEY")

echo "Tools Response:"
print_json "$TOOLS_RESPONSE"

# Extract and display tool information
TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | jq -r '.count')

echo ""
echo "Available Tools ($TOOL_COUNT):"
echo "$TOOLS_RESPONSE" | jq -r '.tools[] | "- " + .name + ": " + .description + " (Required role: " + .required_role + ")"'
echo ""

# 2. Call the calculator tool
echo "2. Calling the calculator tool..."
echo ""

# Define the expression to calculate
EXPRESSION="2+2*5"

echo "Expression to calculate: $EXPRESSION"
echo ""

CALCULATOR_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/tools/call" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "tool": "calculator",
    "parameters": {
      "expression": "'"$EXPRESSION"'"
    }
  }')

echo "Calculator Response:"
print_json "$CALCULATOR_RESPONSE"

# Extract and display calculation results
RESULT=$(echo "$CALCULATOR_RESPONSE" | jq -r '.result.value')
STEPS=$(echo "$CALCULATOR_RESPONSE" | jq -r '.result.steps | join("\n- ")')
EXECUTION_TIME=$(echo "$CALCULATOR_RESPONSE" | jq -r '.execution_time')

echo ""
echo "Calculation Results:"
echo "Expression: $EXPRESSION"
echo "Result: $RESULT"
echo "Steps:"
echo "- $STEPS"
echo "Execution time: $EXECUTION_TIME ms"
echo ""

# 3. Call the weather tool
echo "3. Calling the weather tool..."
echo ""

# Define the location for weather
LOCATION="New York"

echo "Location: $LOCATION"
echo ""

WEATHER_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/tools/call" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "tool": "weather",
    "parameters": {
      "location": "'"$LOCATION"'"
    }
  }')

echo "Weather Response:"
print_json "$WEATHER_RESPONSE"

# Extract and display weather results
if echo "$WEATHER_RESPONSE" | jq -e '.result' > /dev/null; then
    TEMPERATURE=$(echo "$WEATHER_RESPONSE" | jq -r '.result.temperature')
    CONDITIONS=$(echo "$WEATHER_RESPONSE" | jq -r '.result.conditions')
    HUMIDITY=$(echo "$WEATHER_RESPONSE" | jq -r '.result.humidity')
    WIND_SPEED=$(echo "$WEATHER_RESPONSE" | jq -r '.result.wind_speed')
    
    echo ""
    echo "Weather for $LOCATION:"
    echo "- Temperature: $TEMPERATURE"
    echo "- Conditions: $CONDITIONS"
    echo "- Humidity: $HUMIDITY"
    echo "- Wind Speed: $WIND_SPEED"
else
    echo ""
    echo "Weather tool returned an error or unexpected response format."
fi
echo ""

# 4. Try calling a tool with chat completions
echo "4. Using a tool through chat completions..."
echo ""

CHAT_TOOL_RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Calculate 15% of 85.50"}
    ],
    "max_tokens": 150
  }')

echo "Chat Completions Response (with tool detection):"
print_json "$CHAT_TOOL_RESPONSE"

# Extract and display the assistant's message
ASSISTANT_MESSAGE=$(echo "$CHAT_TOOL_RESPONSE" | jq -r '.choices[0].message.content')
FINISH_REASON=$(echo "$CHAT_TOOL_RESPONSE" | jq -r '.choices[0].finish_reason')

echo ""
echo "Assistant's response:"
echo "$ASSISTANT_MESSAGE"
echo ""
echo "Finish reason: $FINISH_REASON"
echo "If finish_reason is 'tool_invocation', the calculator tool was automatically detected and used."

print_footer