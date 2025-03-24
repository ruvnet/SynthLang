#!/bin/bash

# Domain-Specific Examples for SynthLang CLI
echo "Domain-Specific SynthLang Examples"
echo "================================="

# 1. Medical Report Generator
echo -e "\n1. Medical Report Generator:"
SYMPTOMS=(
  "Persistent headache with visual disturbances"
  "Shortness of breath during physical activity"
  "Joint pain and morning stiffness"
)

for symptom in "${SYMPTOMS[@]}"; do
  echo -e "\nAnalyzing symptom: $symptom"
  # Convert to medical terminology
  echo "Step 1: Converting to medical format..."
  synthlang translate \
    --source "$symptom" \
    --framework synthlang

  # Generate differential diagnosis
  echo "Step 2: Generating differential diagnosis..."
  synthlang evolve \
    --seed "Generate differential diagnosis for: $symptom" \
    --generations 3 \
    --population 4
done

# 2. Financial Market Analysis
echo -e "\n2. Financial Market Analysis:"
MARKET_DATA=(
  "Bitcoin price movements in Q1 2024"
  "S&P 500 sector rotation patterns"
  "Emerging markets currency trends"
)

for data in "${MARKET_DATA[@]}"; do
  echo -e "\nAnalyzing: $data"
  synthlang translate \
    --source "Perform technical and fundamental analysis of: $data" \
    --framework synthlang
done

# 3. Environmental Impact Assessment
echo -e "\n3. Environmental Impact Assessment:"
PROJECTS=(
  "Solar farm construction in desert ecosystem"
  "Offshore wind turbine installation"
  "Urban waste management facility"
)

for project in "${PROJECTS[@]}"; do
  echo -e "\nAssessing impact of: $project"
  synthlang translate \
    --source "Analyze environmental impact of: $project" \
    --framework synthlang
done

# 4. Architectural Design Patterns
echo -e "\n4. Architectural Design Patterns:"
BUILDINGS=(
  "Sustainable high-rise office building"
  "Mixed-use development with green spaces"
  "Historic building renovation"
)

for building in "${BUILDINGS[@]}"; do
  echo -e "\nGenerating design patterns for: $building"
  synthlang translate \
    --source "Generate architectural patterns for: $building" \
    --framework synthlang
done

# 5. Sports Strategy Analysis
echo -e "\n5. Sports Strategy Analysis:"
SCENARIOS=(
  "Fourth quarter basketball plays"
  "Soccer defensive formations"
  "Tennis serve patterns"
)

for scenario in "${SCENARIOS[@]}"; do
  echo -e "\nAnalyzing strategy: $scenario"
  synthlang translate \
    --source "Analyze and optimize strategy for: $scenario" \
    --framework synthlang
done

# 6. Educational Curriculum Designer
echo -e "\n6. Educational Curriculum Designer:"
SUBJECTS=(
  "Advanced calculus for high school"
  "Environmental science for middle school"
  "Creative writing workshop"
)

for subject in "${SUBJECTS[@]}"; do
  echo -e "\nDesigning curriculum for: $subject"
  synthlang translate \
    --source "Design comprehensive curriculum for: $subject" \
    --framework synthlang
done

# 7. UX/UI Pattern Generator
echo -e "\n7. UX/UI Pattern Generator:"
INTERFACES=(
  "Mobile banking app navigation"
  "E-commerce checkout flow"
  "Social media content feed"
)

for interface in "${INTERFACES[@]}"; do
  echo -e "\nGenerating UX patterns for: $interface"
  synthlang translate \
    --source "Generate user interface patterns for: $interface" \
    --framework synthlang
done

# 8. Psychological Assessment Framework
echo -e "\n8. Psychological Assessment Framework:"
BEHAVIORS=(
  "Social anxiety in group settings"
  "Work-related stress patterns"
  "Learning style preferences"
)

for behavior in "${BEHAVIORS[@]}"; do
  echo -e "\nDeveloping assessment for: $behavior"
  synthlang translate \
    --source "Create psychological assessment framework for: $behavior" \
    --framework synthlang
done

# 9. Agricultural Planning System
echo -e "\n9. Agricultural Planning System:"
SCENARIOS=(
  "Crop rotation for organic farming"
  "Precision irrigation scheduling"
  "Pest management strategies"
)

for scenario in "${SCENARIOS[@]}"; do
  echo -e "\nGenerating agricultural plan for: $scenario"
  synthlang translate \
    --source "Develop agricultural management plan for: $scenario" \
    --framework synthlang
done

# 10. Space Mission Planning
echo -e "\n10. Space Mission Planning:"
MISSIONS=(
  "Mars sample return mission"
  "Lunar base establishment"
  "Asteroid mining operation"
)

for mission in "${MISSIONS[@]}"; do
  echo -e "\nDeveloping mission plan for: $mission"
  synthlang translate \
    --source "Create detailed space mission plan for: $mission" \
    --framework synthlang
  
  echo -e "\nOptimizing mission parameters..."
  synthlang optimize \
    --prompt "Optimize resource allocation and timeline for: $mission"
done
