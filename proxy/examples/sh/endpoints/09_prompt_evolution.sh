#!/bin/bash

# Prompt Evolution Example
# This script demonstrates how to use the prompt evolution endpoint

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

print_header "Prompt Evolution Example"
echo "This example demonstrates how to evolve a prompt using genetic algorithms."
echo "The evolve endpoint takes a seed prompt and improves it through multiple generations."
echo "This creates highly optimized prompts through an evolutionary process."
echo ""

# Define the seed prompt
SEED_PROMPT=${1:-"Write code to sort an array"}

# Define evolution parameters
N_GENERATIONS=${2:-10}
POPULATION_SIZE=${3:-8}
MUTATION_RATE=${4:-0.1}

echo "Seed prompt: $SEED_PROMPT"
echo "Number of generations: $N_GENERATIONS"
echo "Population size: $POPULATION_SIZE"
echo "Mutation rate: $MUTATION_RATE"
echo ""

# Make the API request
echo "Making request to ${API_BASE_URL}/v1/synthlang/evolve..."
echo "This may take some time as it runs through multiple generations..."
echo ""

RESPONSE=$(curl -s -X POST \
  "${API_BASE_URL}/v1/synthlang/evolve" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "seed_prompt": "'"$SEED_PROMPT"'",
    "n_generations": '"$N_GENERATIONS"',
    "population_size": '"$POPULATION_SIZE"',
    "mutation_rate": '"$MUTATION_RATE"'
  }')

echo "Response:"
print_json "$RESPONSE"

# Extract and display the evolved prompt
SEED_PROMPT=$(echo "$RESPONSE" | jq -r '.seed_prompt')
BEST_PROMPT=$(echo "$RESPONSE" | jq -r '.best_prompt')
GENERATIONS=$(echo "$RESPONSE" | jq -r '.generations')
POPULATION_SIZE=$(echo "$RESPONSE" | jq -r '.population_size')
MUTATION_RATE=$(echo "$RESPONSE" | jq -r '.mutation_rate')
CLARITY=$(echo "$RESPONSE" | jq -r '.fitness.clarity')
SPECIFICITY=$(echo "$RESPONSE" | jq -r '.fitness.specificity')
COMPLETENESS=$(echo "$RESPONSE" | jq -r '.fitness.completeness')
OVERALL=$(echo "$RESPONSE" | jq -r '.fitness.overall')

# Extract evolution path
EVOLUTION_PATH=$(echo "$RESPONSE" | jq -r '.evolution_path | map("Generation " + (.generation|tostring) + ": Best fitness = " + (.best_fitness|tostring) + ", Average fitness = " + (.average_fitness|tostring)) | join("\n- ")')

echo ""
echo "Seed prompt: $SEED_PROMPT"
echo ""
echo "Best evolved prompt:"
echo "------------------------------------------------------------------------------"
echo "$BEST_PROMPT"
echo "------------------------------------------------------------------------------"
echo ""
echo "Evolution parameters:"
echo "- Generations: $GENERATIONS"
echo "- Population size: $POPULATION_SIZE"
echo "- Mutation rate: $MUTATION_RATE"
echo ""
echo "Fitness scores:"
echo "- Clarity: $CLARITY"
echo "- Specificity: $SPECIFICITY"
echo "- Completeness: $COMPLETENESS"
echo "- Overall: $OVERALL"
echo ""
echo "Evolution path:"
echo "- $EVOLUTION_PATH"

print_footer