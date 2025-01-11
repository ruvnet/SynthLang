# SynthLang Evolution System

## Introduction

The SynthLang Evolution System is an advanced prompt optimization framework that combines genetic algorithms with self-play tournaments to evolve and improve prompts in the SynthLang format. Drawing inspiration from PAPILLON and DSPy, it uses evolutionary computation principles to iteratively refine prompts while maintaining strict adherence to SynthLang's symbolic notation and format rules.

## Benefits

1. **Automated Optimization**
   - Reduces manual prompt engineering effort
   - Systematically explores prompt variations
   - Maintains format consistency while evolving

2. **Multi-objective Optimization**
   - Balances multiple fitness criteria:
     - Clarity: Symbol usage and structure
     - Specificity: Operator and join usage
     - Task Completion: Test case performance

3. **Verifiable Results**
   - Test case validation
   - Fitness metrics tracking
   - Evolution history logging

## Novel Features

1. **SynthLang-Aware Mutations**
   - Symbol-preserving mutations (↹, ⊕, Σ)
   - Format-compliant transformations
   - Operator-aware modifications

2. **Hybrid Fitness Functions**
   - Combines structural and functional metrics
   - Weighted scoring system
   - Adaptive fitness calculation

3. **Tournament Selection**
   - Self-play competition between prompts
   - Survival of the fittest mechanics
   - Population diversity maintenance

## Technical Details

### Architecture

```python
class PromptEvolver:
    def __init__(self, lm, population_size, mutation_rate, tournament_size, 
                 fitness_type, test_cases):
        # Initialize evolution parameters
        
    def _generate_variant(self, prompt):
        # Generate mutations while preserving format
        
    def _calculate_fitness(self, prompt):
        # Multi-objective fitness calculation
        
    def _tournament_select(self, population):
        # Tournament selection process
        
    def evolve(self, seed_prompt, n_generations):
        # Main evolution loop
```

### Mutation Types

1. **Add Processing Step**
   ```
   Before:
   ↹ data•sales
   ⊕ analyze => insights
   Σ report
   
   After:
   ↹ data•sales
   ⊕ filter>Q1 => subset
   ⊕ analyze => insights
   Σ report
   ```

2. **Combine Steps**
   ```
   Before:
   ↹ data•source
   ⊕ validate => clean
   ⊕ analyze => insights
   Σ report
   
   After:
   ↹ data•source
   ⊕ validate•analyze => insights
   Σ report
   ```

3. **Split Step**
   ```
   Before:
   ↹ input•stream
   ⊕ process => result
   Σ output
   
   After:
   ↹ input•stream
   ⊕ validate => clean
   ⊕ transform => result
   Σ output
   ```

### Fitness Calculation

```python
def calculate_fitness(prompt):
    # Clarity (symbol usage)
    clarity = sum(sym in prompt for sym in [↹, ⊕, Σ]) / 3.0
    
    # Specificity (operators and joins)
    specificity = (
        prompt.count("•") * 0.2 +    # Joins
        prompt.count("=>") * 0.2 +   # Transforms
        sum(op in prompt for op in ["+", ">", "<", "^"]) * 0.1
    )
    
    # Task completion (if test cases provided)
    task_score = evaluate_test_cases(prompt)
    
    # Overall fitness
    weights = [0.3, 0.3, 0.4]  # Configurable weights
    return (clarity * weights[0] + 
            specificity * weights[1] + 
            task_score * weights[2])
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `seed` | Required | Initial prompt to evolve |
| `generations` | 10 | Number of evolution cycles |
| `population` | 5 | Size of prompt population |
| `mutation_rate` | 0.3 | Probability of mutation (0-1) |
| `tournament_size` | 3 | Number of prompts per tournament |
| `fitness` | "hybrid" | Fitness function type |
| `save_lineage` | False | Save evolution history |
| `test_cases` | None | Path to test cases file |

## Usage Examples

1. **Basic Evolution**
   ```bash
   synthlang evolve \
       --seed "↹ data•sales\n⊕ analyze => insights\nΣ report" \
       --generations 5 \
       --population 3
   ```

2. **Task-Specific Evolution**
   ```bash
   synthlang evolve \
       --seed "↹ feedback•customer\n⊕ analyze => sentiment\nΣ report" \
       --generations 10 \
       --population 5 \
       --fitness task \
       --test-cases tests/sentiment.json
   ```

3. **Advanced Evolution with History**
   ```bash
   synthlang evolve \
       --seed "↹ data•source\n⊕ process => result\nΣ output" \
       --generations 20 \
       --population 8 \
       --mutation-rate 0.4 \
       --tournament-size 4 \
       --fitness hybrid \
       --save-lineage
   ```

## Test Cases Format

```json
{
    "test_cases": [
        {
            "input": "analyze sales data for Q1",
            "expected": "↹ data•sales\n⊕ filter>Q1 => analyze\nΣ insights + trends"
        },
        {
            "input": "summarize customer feedback",
            "expected": "↹ feedback•customer\n⊕ sentiment>0 => pos\n⊕ sentiment<0 => neg\nΣ summary + metrics"
        }
    ]
}
```

## Evolution Metrics

The system tracks various metrics during evolution:

1. **Fitness Scores**
   - Clarity (0-1): Symbol usage effectiveness
   - Specificity (0-2): Operator and join utilization
   - Task Completion (0-1): Test case success rate
   - Overall (0-1): Weighted combination

2. **Evolution Statistics**
   - Generations completed
   - Total variants created
   - Successful mutations
   - Tournament winners

3. **Lineage Tracking**
   - Complete evolution history
   - Population snapshots
   - Fitness progression

## Best Practices

1. **Seed Prompts**
   - Start with valid SynthLang format
   - Include essential operations
   - Keep initial complexity moderate

2. **Evolution Parameters**
   - Adjust based on task complexity
   - Use larger populations for diverse solutions
   - Increase generations for thorough exploration

3. **Test Cases**
   - Cover key functionality
   - Include edge cases
   - Maintain format consistency

4. **Fitness Selection**
   - Use "hybrid" for general optimization
   - Choose "task" for specific requirements
   - Select "clarity" for format refinement
