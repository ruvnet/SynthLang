#!/bin/bash

# Pipeline Examples - Combining Multiple Commands
echo "SynthLang Pipeline Examples"
echo "=========================="

# Example 1: Translate then Optimize
echo -e "\n1. Translate and Optimize Pipeline:"
echo -e "Step 1: Translating prompt..."
TRANSLATED=$(synthlang translate \
  --source "Generate a summary of the quarterly sales performance" \
  --framework synthlang)

echo -e "\nStep 2: Optimizing translated prompt..."
echo "$TRANSLATED" | synthlang optimize --prompt -

# Example 2: Multiple Translations with Classification
echo -e "\n2. Translation and Classification Pipeline:"
PROMPTS=(
  "Write a blog post about AI"
  "Analyze customer feedback"
  "Create a marketing email"
)

for prompt in "${PROMPTS[@]}"; do
  echo -e "\nProcessing: $prompt"
  echo -e "Step 1: Translating..."
  synthlang translate \
    --source "$prompt" \
    --framework synthlang \
    --show-metrics

  echo -e "\nStep 2: Classifying..."
  synthlang classify predict \
    --text "$prompt" \
    --labels "analysis,generation,summarization,creation"
done

# Example 3: Evolution and Optimization Pipeline
echo -e "\n3. Evolution and Optimization Pipeline:"
echo -e "Step 1: Evolving prompt..."
synthlang evolve \
  --seed "Analyze sales data and create insights" \
  --generations 5 \
  --population 4

echo -e "\nStep 2: Optimizing evolved prompt..."
synthlang optimize \
  --prompt "Analyze sales data and create insights with evolved patterns"

# Example 4: Complex Multi-step Pipeline
echo -e "\n4. Complex Multi-step Pipeline:"
PROMPT="Analyze customer feedback and generate insights"

echo -e "Step 1: Initial translation..."
synthlang translate \
  --source "$PROMPT" \
  --framework synthlang \
  --show-metrics

echo -e "\nStep 2: Classification..."
synthlang classify predict \
  --text "$PROMPT" \
  --labels "analysis,generation,summarization,creation"

echo -e "\nStep 3: Evolution..."
synthlang evolve \
  --seed "$PROMPT" \
  --generations 3 \
  --population 4

echo -e "\nStep 4: Final optimization..."
synthlang optimize --prompt "$PROMPT"
