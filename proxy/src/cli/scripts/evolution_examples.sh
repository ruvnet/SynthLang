#!/bin/bash

# Evolution Examples
echo "SynthLang Evolution Examples"
echo "==========================="

# Create test prompts directory
mkdir -p test_prompts

# Basic evolution
echo -e "\n1. Basic Evolution:"
synthlang evolve \
  --seed "Generate a summary of the quarterly sales performance" \
  --generations 5 \
  --population 4

# Advanced evolution with more parameters
echo -e "\n2. Advanced Evolution with Custom Parameters:"
synthlang evolve \
  --seed "Analyze customer feedback and provide insights" \
  --generations 10 \
  --population 6 \
  --mutation-rate 0.4 \
  --tournament-size 3 \
  --fitness hybrid

# Evolution with test cases
echo -e "\n3. Evolution with Test Cases:"
# Create test cases file
cat << EOF > test_prompts/test_cases.json
{
  "test_cases": [
    {
      "input": "Q4 2023 sales data",
      "expected_output": "Sales performance analysis with key metrics"
    }
  ]
}
EOF

synthlang evolve \
  --seed "Analyze sales data and generate performance report" \
  --generations 8 \
  --population 5 \
  --test-cases "test_prompts/test_cases.json" \
  --fitness task

# Evolution with lineage tracking
echo -e "\n4. Evolution with Lineage Tracking:"
synthlang evolve \
  --seed "Write a blog post about AI technology trends" \
  --generations 6 \
  --population 4 \
  --save-lineage

# Evolution with prompt saving
echo -e "\n5. Evolution with Prompt Saving:"
synthlang evolve \
  --seed "Create a marketing strategy based on customer data" \
  --generations 5 \
  --population 4 \
  --save-prompt "marketing_strategy"

# Cleanup
rm -r test_prompts
