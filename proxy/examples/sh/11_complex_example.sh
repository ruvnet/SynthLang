#!/bin/bash

# Complex example
# This script demonstrates a complex scenario combining multiple features

# Load environment variables
if [ -f "../../.env" ]; then
    export $(grep -v '^#' ../../.env | xargs)
elif [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if API_KEY is set
if [ -z "$API_KEY" ]; then
    echo "Error: API_KEY not found in environment variables"
    echo "Please run: python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env"
    exit 1
fi

echo "=== Complex Example ==="
echo "This example demonstrates a complex scenario combining multiple features:"
echo "1. Using a system message to set the assistant's behavior"
echo "2. Having a multi-turn conversation"
echo "3. Triggering a tool via natural language pattern detection"
echo "4. Using streaming for real-time responses"
echo ""

# Make the API request for the first turn
echo "TURN 1: Initial question about AI and weather"
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant with expertise in AI and technology. You can also provide weather information when asked."},
      {"role": "user", "content": "What are the main approaches to artificial intelligence?"}
    ]
  }' | jq '.choices[0].message.content' -r

echo ""
echo "TURN 2: Follow-up question about weather (should trigger weather tool)"
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant with expertise in AI and technology. You can also provide weather information when asked."},
      {"role": "user", "content": "What are the main approaches to artificial intelligence?"},
      {"role": "assistant", "content": "The main approaches to artificial intelligence include:\n\n1. **Machine Learning**: Systems that learn from data rather than following explicit programming. This includes supervised learning, unsupervised learning, and reinforcement learning.\n\n2. **Deep Learning**: A subset of machine learning using neural networks with many layers (deep neural networks) to analyze various factors of data.\n\n3. **Natural Language Processing**: Focuses on enabling computers to understand, interpret, and generate human language.\n\n4. **Computer Vision**: Enables machines to interpret and make decisions based on visual input.\n\n5. **Expert Systems**: Rule-based systems that capture human expertise in a specific domain.\n\n6. **Robotics**: Combines AI with physical machines to perform tasks in the physical world.\n\n7. **Symbolic AI**: Based on high-level symbolic representations of problems, logic, and search.\n\n8. **Evolutionary Computation**: Inspired by biological evolution, using mechanisms like mutation, selection, and reproduction.\n\nEach approach has its strengths and limitations, and modern AI systems often combine multiple approaches."},
      {"role": "user", "content": "Thanks! Now, what is the weather in London?"}
    ],
    "stream": true
  }'

echo ""
echo ""
echo "=== Example Completed ==="