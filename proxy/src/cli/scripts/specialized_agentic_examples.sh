#!/bin/bash

# Specialized Agentic Examples
echo "Specialized SynthLang Agentic Examples"
echo "===================================="

# Create output directory
mkdir -p specialized_examples

# 1. AI Research Assistant
echo -e "\n1. AI Research Assistant Example"
cat << EOF > specialized_examples/research_assistant.md
# AI Research Assistant Template

## Input Pattern
↹ research•topic•constraints
↹ existing•literature•scope
↹ methodology•requirements

## Process Steps
⊕ search => relevant•papers
⊕ analyze => key•findings
⊕ synthesize => insights
⊕ identify => gaps
⊕ formulate => hypotheses

## Output Format
Σ research•summary + insights + recommendations

## Example Usage:
synthlang translate \
  --source "Research the impact of AI on healthcare diagnostics, focusing on the last 5 years of peer-reviewed studies" \
  --framework synthlang
EOF

# 2. Software Architecture Planner
echo -e "\n2. Software Architecture Planner Example"
cat << EOF > specialized_examples/architecture_planner.md
# Software Architecture Planner Template

## Input Pattern
↹ system•requirements•constraints
↹ technical•stack•limitations
↹ scalability•needs

## Process Steps
⊕ analyze => requirements
⊕ design => components
⊕ evaluate => tradeoffs
⊕ optimize => architecture
⊕ document => decisions

## Output Format
Σ architecture•design + rationale + implementation•plan

## Example Usage:
synthlang translate \
  --source "Design a microservices architecture for a high-traffic e-commerce platform with emphasis on scalability and reliability" \
  --framework synthlang
EOF

# 3. Data Science Pipeline Designer
echo -e "\n3. Data Science Pipeline Designer Example"
cat << EOF > specialized_examples/data_science_pipeline.md
# Data Science Pipeline Designer Template

## Input Pattern
↹ data•sources•requirements
↹ analysis•objectives•constraints
↹ performance•metrics

## Process Steps
⊕ ingest => raw•data
⊕ clean => processed•data
⊕ analyze => insights
⊕ model => predictions
⊕ validate => results

## Output Format
Σ pipeline•design + metrics + recommendations

## Example Usage:
synthlang translate \
  --source "Design a real-time data processing pipeline for analyzing customer behavior patterns in an e-commerce platform" \
  --framework synthlang
EOF

# 4. Security Protocol Analyzer
echo -e "\n4. Security Protocol Analyzer Example"
cat << EOF > specialized_examples/security_analyzer.md
# Security Protocol Analyzer Template

## Input Pattern
↹ system•components•vulnerabilities
↹ threat•models•scenarios
↹ security•requirements

## Process Steps
⊕ analyze => attack•vectors
⊕ evaluate => risks
⊕ design => countermeasures
⊕ test => effectiveness
⊕ document => findings

## Output Format
Σ security•assessment + recommendations + implementation•plan

## Example Usage:
synthlang translate \
  --source "Analyze the security protocols of a cloud-based financial system and provide hardening recommendations" \
  --framework synthlang
EOF

# 5. Product Strategy Optimizer
echo -e "\n5. Product Strategy Optimizer Example"
cat << EOF > specialized_examples/product_optimizer.md
# Product Strategy Optimizer Template

## Input Pattern
↹ market•data•trends
↹ competitor•analysis•insights
↹ customer•feedback•metrics

## Process Steps
⊕ analyze => market•position
⊕ identify => opportunities
⊕ evaluate => strategies
⊕ prioritize => initiatives
⊕ plan => execution

## Output Format
Σ strategy•recommendations + roadmap + success•metrics

## Example Usage:
synthlang translate \
  --source "Develop a product strategy for expanding into the enterprise market segment while maintaining current customer satisfaction" \
  --framework synthlang
EOF

# Process each example
for example in specialized_examples/*.md; do
  echo -e "\nProcessing example: $example"
  
  # Extract example usage
  EXAMPLE=$(grep -A 1 "Example Usage:" "$example" | tail -n 1)
  
  # Execute the example
  eval "$EXAMPLE"
  
  # Evolve the result
  PROMPT=$(grep -A 1 "Example Usage:" "$example" | tail -n 1 | sed 's/.*--source "\(.*\)" .*/\1/')
  
  echo -e "\nEvolving the example..."
  synthlang evolve \
    --seed "$PROMPT" \
    --generations 3 \
    --population 4
    
  echo -e "\nOptimizing the result..."
  synthlang optimize \
    --prompt "$PROMPT"
done

# Generate combined report
echo -e "\nGenerating combined report..."

cat << EOF > specialized_examples/combined_report.md
# Specialized Agentic Examples Report

## Overview
This report presents specialized templates and examples for different domains, demonstrating the versatility of SynthLang in handling complex, domain-specific tasks.

## Templates and Results
$(cat specialized_examples/*.md)

## Usage Patterns
1. Domain-Specific Input
   - Define clear context and constraints
   - Specify domain-specific requirements
   - Include relevant metrics

2. Specialized Processing
   - Use domain-appropriate operations
   - Include validation steps
   - Maintain semantic consistency

3. Structured Output
   - Format results for domain context
   - Include relevant metrics
   - Provide actionable insights

## Best Practices
1. Template Customization
   - Adapt to domain requirements
   - Include specialized metrics
   - Use domain-specific terminology

2. Process Optimization
   - Focus on domain-specific efficiency
   - Include validation checkpoints
   - Maintain quality standards

3. Output Formatting
   - Match domain expectations
   - Include required metrics
   - Provide actionable insights

## Next Steps
1. Template Refinement
   - Gather domain feedback
   - Optimize for specific use cases
   - Expand template library

2. Process Enhancement
   - Improve efficiency
   - Add specialized features
   - Enhance validation

3. Integration
   - Connect with domain tools
   - Automate workflows
   - Enhance monitoring
EOF

echo -e "\nSpecialized Examples Complete!"
echo "Results available in specialized_examples/combined_report.md"
