#!/bin/bash

# Advanced Translation Examples
echo "Advanced SynthLang Translation Examples"
echo "====================================="

# Complex prompt with multiple operations
echo -e "\n1. Complex Translation:"
synthlang translate \
  --source "Analyze customer feedback data, generate sentiment scores, identify key themes, and create a summary report with recommendations" \
  --framework synthlang \
  --show-metrics

# Translation with custom parameters
echo -e "\n2. Translation with Custom Parameters:"
synthlang translate \
  --source "Create a detailed market analysis report based on sales data, competitor information, and customer surveys" \
  --framework synthlang \
  --show-metrics

# Batch processing from file
echo -e "\n3. Batch Processing from File:"
# Create a temporary file with prompts
cat << EOF > temp_prompts.txt
Optimize the website conversion rate using A/B testing data
Generate quarterly financial forecasts using historical data
Create personalized product recommendations based on user behavior
EOF

while IFS= read -r prompt; do
  echo -e "\nProcessing: $prompt"
  synthlang translate \
    --source "$prompt" \
    --framework synthlang \
    --show-metrics
done < temp_prompts.txt

# Cleanup
rm temp_prompts.txt

# Complex nested operations
echo -e "\n4. Complex Nested Operations:"
synthlang translate \
  --source "Analyze customer support tickets, categorize by priority and department, calculate response times, identify bottlenecks, and suggest process improvements" \
  --framework synthlang \
  --show-metrics

# Multi-step analysis
echo -e "\n5. Multi-step Analysis:"
synthlang translate \
  --source "Extract key metrics from sales data, perform trend analysis, identify seasonal patterns, calculate growth rates, and generate future projections" \
  --framework synthlang \
  --show-metrics
