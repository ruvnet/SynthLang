#!/bin/bash

# Classification Examples
echo "SynthLang Classification Examples"
echo "================================"

# Define common labels
LABELS="analysis,generation,summarization,creation"

# Create test prompts directory
mkdir -p test_prompts

# Basic classification
echo -e "\n1. Basic Classification:"
synthlang classify predict \
  --text "Generate a summary of the quarterly sales performance" \
  --labels "$LABELS"

# Multiple prompts classification
echo -e "\n2. Multiple Classifications:"
PROMPTS=(
  "Write a blog post about AI"
  "Analyze customer feedback"
  "Create a marketing email"
)

for prompt in "${PROMPTS[@]}"; do
  echo -e "\nClassifying: $prompt"
  synthlang classify predict \
    --text "$prompt" \
    --labels "$LABELS"
done

# Train a classifier
echo -e "\n3. Training a Custom Classifier:"
# Create training data
cat << EOF > test_prompts/training_data.json
{
  "examples": [
    {
      "text": "Analyze sales data",
      "label": "analysis"
    },
    {
      "text": "Generate a report",
      "label": "generation"
    }
  ]
}
EOF

synthlang classify train \
  --train-data "test_prompts/training_data.json" \
  --labels "$LABELS" \
  --save-model "test_prompts/classifier.model"

# Use trained classifier
echo -e "\n4. Using Trained Classifier:"
synthlang classify predict \
  --text "Analyze sales data and generate insights" \
  --labels "$LABELS" \
  --model "test_prompts/classifier.model"

# Complex prompt classification
echo -e "\n5. Complex Prompt Classification:"
COMPLEX_PROMPT="Analyze customer feedback data from multiple sources including social media mentions, customer support tickets, and satisfaction surveys. Generate sentiment scores for each channel and create a detailed report."
synthlang classify predict \
  --text "$COMPLEX_PROMPT" \
  --labels "$LABELS"

# Cleanup
rm -r test_prompts
