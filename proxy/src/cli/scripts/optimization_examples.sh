#!/bin/bash

# Optimization Examples
echo "SynthLang Optimization Examples"
echo "=============================="

# Create test prompts
mkdir -p test_prompts

# Basic prompt
cat << EOF > test_prompts/basic_prompt.txt
Generate a comprehensive analysis of the quarterly sales data, including revenue trends, 
top-performing products, regional performance metrics, and year-over-year growth comparisons. 
Provide detailed insights and actionable recommendations for improving sales performance in 
underperforming regions.
EOF

# Complex prompt
cat << EOF > test_prompts/complex_prompt.txt
Analyze customer feedback data from multiple sources including social media mentions, 
customer support tickets, and satisfaction surveys. Generate sentiment scores for each channel, 
identify recurring themes and pain points, evaluate trend changes over time, and create a 
detailed report with specific recommendations for improving customer satisfaction across all 
touchpoints. Include statistical significance of findings and prioritize recommendations based 
on potential impact and implementation effort.
EOF

# Basic optimization
echo -e "\n1. Basic Optimization:"
BASIC_PROMPT=$(cat test_prompts/basic_prompt.txt)
synthlang optimize --prompt "$BASIC_PROMPT"

# Advanced optimization
echo -e "\n2. Advanced Optimization:"
COMPLEX_PROMPT=$(cat test_prompts/complex_prompt.txt)
synthlang optimize --prompt "$COMPLEX_PROMPT"

# Batch optimization
echo -e "\n3. Batch Optimization:"
for file in test_prompts/*.txt; do
  echo -e "\nOptimizing: $file"
  PROMPT=$(cat "$file")
  synthlang optimize --prompt "$PROMPT"
done

# Additional examples
echo -e "\n4. Short Prompt Optimization:"
synthlang optimize --prompt "Generate a summary of the quarterly sales performance"

echo -e "\n5. Medium Prompt Optimization:"
synthlang optimize --prompt "Analyze customer feedback from social media and create a report with key insights and recommendations"

# Cleanup
rm -r test_prompts
