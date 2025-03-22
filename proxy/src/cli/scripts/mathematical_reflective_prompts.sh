#!/bin/bash

# Mathematical Reflective Prompts Generator
echo "Mathematical Reflective Prompts Generator"
echo "======================================="

# Create output directory
mkdir -p math_prompts

# 1. Set Theory Based Prompts
cat << EOF > math_prompts/set_theory_prompts.md
# Set Theory Reflective Prompts

## Union and Intersection
\`A ∪ B\` and \`A ∩ B\`

### Reflective Pattern
↹ problem•domains•constraints
⊕ identify => common•elements
⊕ analyze => unique•aspects
⊕ synthesize => unified•solution
Σ integrated•approach + shared•insights

### Example Prompt
"Consider two different approaches to solving this problem. How might we combine their strengths (union) while identifying their common successful elements (intersection)?"

## Power Set
\`P(A) = {x | x ⊆ A}\`

### Reflective Pattern
↹ solution•space•constraints
⊕ enumerate => possibilities
⊕ analyze => subsets
⊕ evaluate => combinations
Σ comprehensive•analysis + feasibility•matrix

### Example Prompt
"What are all possible combinations of approaches we could take? How do these subsets of solutions interact with each other?"

## Complement
\`A' = {x ∈ U | x ∉ A}\`

### Reflective Pattern
↹ current•approach•limitations
⊕ identify => gaps
⊕ explore => alternatives
⊕ analyze => completeness
Σ holistic•perspective + blind•spots
EOF

# 2. Category Theory Based Prompts
cat << EOF > math_prompts/category_theory_prompts.md
# Category Theory Reflective Prompts

## Functors
\`F: C → D\`

### Reflective Pattern
↹ domain•codomain•mapping
⊕ preserve => structure
⊕ transform => concepts
⊕ maintain => relationships
Σ transformed•insight + preserved•properties

### Example Prompt
"How can we translate this solution from one context to another while preserving its essential properties?"

## Natural Transformations
\`η: F ⇒ G\`

### Reflective Pattern
↹ approaches•methods•transitions
⊕ compare => strategies
⊕ identify => transformations
⊕ validate => coherence
Σ systematic•evolution + consistency•check
EOF

# 3. Abstract Algebra Based Prompts
cat << EOF > math_prompts/abstract_algebra_prompts.md
# Abstract Algebra Reflective Prompts

## Group Actions
\`G × X → X\`

### Reflective Pattern
↹ transformations•symmetries•invariants
⊕ identify => patterns
⊕ analyze => operations
⊕ preserve => structure
Σ systematic•approach + invariant•properties

### Example Prompt
"What patterns remain constant as we apply different transformations to our approach?"

## Ring Structure
\`(R, +, ×)\`

### Reflective Pattern
↹ operations•interactions•composition
⊕ combine => methods
⊕ distribute => resources
⊕ verify => closure
Σ integrated•framework + operational•rules
EOF

# 4. Topology Based Prompts
cat << EOF > math_prompts/topology_prompts.md
# Topology Reflective Prompts

## Continuity
\`f: X → Y\` is continuous

### Reflective Pattern
↹ transitions•changes•preservation
⊕ identify => connections
⊕ maintain => continuity
⊕ analyze => boundaries
Σ smooth•transition + preserved•properties

### Example Prompt
"How can we ensure our solution remains robust under small perturbations or changes in conditions?"

## Homeomorphism
\`f: X → Y\` is bijective and bicontinuous

### Reflective Pattern
↹ transformations•equivalences•preservation
⊕ map => structure
⊕ preserve => properties
⊕ verify => reversibility
Σ equivalent•perspective + structural•insight
EOF

# 5. Complex Analysis Based Prompts
cat << EOF > math_prompts/complex_analysis_prompts.md
# Complex Analysis Reflective Prompts

## Residue Theorem
\`∮_C f(z)dz = 2πi ∑Res(f,ak)\`

### Reflective Pattern
↹ local•global•interactions
⊕ analyze => singularities
⊕ integrate => effects
⊕ synthesize => global•view
Σ comprehensive•understanding + local•insights

### Example Prompt
"How do local decisions and singular points in our approach contribute to the overall solution?"

## Analytic Continuation
\`f(z)\` extends uniquely

### Reflective Pattern
↹ partial•solution•constraints
⊕ extend => domain
⊕ preserve => consistency
⊕ validate => uniqueness
Σ complete•solution + coherence•check
EOF

# Generate Combined Report
cat << EOF > math_prompts/reflective_patterns.md
# Mathematical Reflective Patterns

## Overview
This document presents a collection of reflective patterns derived from fundamental mathematical concepts. Each pattern provides a structured approach to problem-solving and reflection.

## Pattern Structure
- Input (↹): Context and constraints
- Process (⊕): Transformation steps
- Output (Σ): Results and insights

## Mathematical Frameworks
$(cat math_prompts/*.md)

## Application Guidelines

### Pattern Selection
1. Identify the type of reflection needed:
   - Structure preservation (Category Theory)
   - Completeness analysis (Set Theory)
   - Transformation analysis (Abstract Algebra)
   - Continuity and connection (Topology)
   - Local-global relationships (Complex Analysis)

### Pattern Application
1. Context Definition
   - Clearly specify the domain
   - Identify constraints
   - Define objectives

2. Process Execution
   - Follow transformation steps
   - Maintain mathematical properties
   - Verify consistency

3. Output Analysis
   - Validate results
   - Check coherence
   - Ensure completeness

### Best Practices
1. Property Preservation
   - Maintain essential structure
   - Preserve important relationships
   - Ensure consistency

2. Transformation Clarity
   - Clear mapping definitions
   - Well-defined steps
   - Verifiable results

3. Completeness
   - Cover all cases
   - Address edge conditions
   - Validate assumptions

## Next Steps
1. Pattern Refinement
   - Collect usage feedback
   - Refine transformations
   - Expand examples

2. Framework Extension
   - Add new patterns
   - Develop combinations
   - Create variations

3. Application Development
   - Create specific instances
   - Document case studies
   - Build pattern library
EOF

echo "Mathematical Reflective Prompts Generated!"
echo "Results available in math_prompts/"
