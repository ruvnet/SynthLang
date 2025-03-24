#!/bin/bash

# Basic Translation Examples
echo "Basic SynthLang Translation Examples"
echo "==================================="

# Simple translation
echo -e "\n1. Simple Translation:"
synthlang translate \
  --source "Generate a summary of the text" \
  --framework synthlang

# Translation with metrics
echo -e "\n2. Translation with Metrics:"
synthlang translate \
  --source "Analyze customer feedback and provide insights" \
  --framework synthlang \
  --show-metrics

# Multiple translations
echo -e "\n3. Multiple Translations:"
PROMPTS=(
  "Write a blog post about AI"
  "Create a marketing email"
  "Analyze sales data"
)

for prompt in "${PROMPTS[@]}"; do
  echo -e "\nTranslating: $prompt"
  synthlang translate \
    --source "$prompt" \
    --framework synthlang \
    --show-metrics
done
