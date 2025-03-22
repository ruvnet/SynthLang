#!/bin/bash

# Creative Examples for SynthLang CLI
echo "Creative SynthLang Examples"
echo "=========================="

# 1. Academic Paper Generator Pipeline
echo -e "\n1. Academic Paper Generator:"
PAPER_SECTIONS=(
  "Introduction to quantum computing principles"
  "Analysis of quantum algorithms"
  "Comparison of quantum hardware platforms"
  "Future implications for cryptography"
)

for section in "${PAPER_SECTIONS[@]}"; do
  echo -e "\nProcessing section: $section"
  # Translate to formal academic style
  echo "Step 1: Translating to academic format..."
  synthlang translate \
    --source "$section" \
    --framework synthlang \
    --show-metrics

  # Evolve to improve academic rigor
  echo "Step 2: Evolving academic content..."
  synthlang evolve \
    --seed "$section" \
    --generations 3 \
    --population 4
done

# 2. Poetry Style Transformer
echo -e "\n2. Poetry Style Transformer:"
POEM="Gentle waves crash upon the shore, under moonlit skies forevermore"

echo -e "\nTransforming to Haiku style..."
synthlang translate \
  --source "$POEM" \
  --framework synthlang

echo -e "\nTransforming to Sonnet style..."
synthlang translate \
  --source "$POEM" \
  --framework synthlang

# 3. Code Documentation Generator
echo -e "\n3. Code Documentation Generator:"
CODE_SNIPPETS=(
  "function calculateMetrics(data) { return data.map(x => x * 2) }"
  "class DataProcessor { constructor() { this.cache = new Map() } }"
)

for snippet in "${CODE_SNIPPETS[@]}"; do
  echo -e "\nGenerating documentation for: $snippet"
  synthlang translate \
    --source "Generate comprehensive documentation for: $snippet" \
    --framework synthlang
done

# 4. Recipe Transformer
echo -e "\n4. Recipe Transformer:"
RECIPE="Classic chocolate chip cookies with butter and brown sugar"

echo "Original Recipe:"
echo "$RECIPE"

echo -e "\nTransforming to Vegan version..."
synthlang translate \
  --source "Convert to vegan: $RECIPE" \
  --framework synthlang

echo -e "\nTransforming to Gluten-free version..."
synthlang translate \
  --source "Convert to gluten-free: $RECIPE" \
  --framework synthlang

# 5. Music Theory Analyzer
echo -e "\n5. Music Theory Analyzer:"
COMPOSITIONS=(
  "C major scale with seventh chords"
  "Blues progression in A minor"
  "Jazz improvisation over II-V-I"
)

for comp in "${COMPOSITIONS[@]}"; do
  echo -e "\nAnalyzing: $comp"
  synthlang translate \
    --source "Analyze music theory concepts in: $comp" \
    --framework synthlang
done

# 6. Legal Document Simplifier
echo -e "\n6. Legal Document Simplifier:"
LEGAL_TEXT="The party of the first part hereby agrees to transfer ownership"

echo "Original Legal Text:"
echo "$LEGAL_TEXT"

echo -e "\nSimplifying..."
synthlang translate \
  --source "Simplify legal language: $LEGAL_TEXT" \
  --framework synthlang

# 7. Emotional Intelligence Analyzer
echo -e "\n7. Emotional Intelligence Analyzer:"
CONVERSATIONS=(
  "I'm really disappointed with the project outcome"
  "Your presentation was excellent, great job!"
  "I'm not sure I understand your perspective"
)

for conv in "${CONVERSATIONS[@]}"; do
  echo -e "\nAnalyzing emotional context: $conv"
  synthlang translate \
    --source "Analyze emotional subtext and suggest empathetic responses" \
    --framework synthlang
done

# 8. Historical Style Converter
echo -e "\n8. Historical Style Converter:"
MODERN_TEXT="Send me an email with the project updates"

echo "Converting to different historical periods..."
PERIODS=(
  "Victorian Era"
  "Renaissance"
  "Ancient Rome"
)

for period in "${PERIODS[@]}"; do
  echo -e "\nConverting to $period style:"
  synthlang translate \
    --source "Convert to $period style: $MODERN_TEXT" \
    --framework synthlang
done

# 9. Cross-Cultural Communication Adapter
echo -e "\n9. Cross-Cultural Communication Adapter:"
MESSAGE="We need to reschedule the meeting"

echo "Adapting for different cultural contexts..."
CULTURES=(
  "Japanese business culture"
  "Brazilian business culture"
  "German business culture"
)

for culture in "${CULTURES[@]}"; do
  echo -e "\nAdapting for $culture:"
  synthlang translate \
    --source "Adapt message for $culture: $MESSAGE" \
    --framework synthlang
done

# 10. Scientific Paper Hypothesis Generator
echo -e "\n10. Scientific Paper Hypothesis Generator:"
TOPICS=(
  "Impact of meditation on brain plasticity"
  "Correlation between gut bacteria and mood"
  "Effects of microplastics on marine ecosystems"
)

for topic in "${TOPICS[@]}"; do
  echo -e "\nGenerating hypotheses for: $topic"
  synthlang translate \
    --source "Generate testable scientific hypotheses for: $topic" \
    --framework synthlang
  
  echo -e "\nEvolving hypotheses..."
  synthlang evolve \
    --seed "$topic" \
    --generations 3 \
    --population 4
done
