"""Prompt evolution module using genetic algorithms and self-play tournaments."""
import random
from typing import Any, Dict, List, Optional

import dspy

from .base import SynthLangModule
from .types import SynthLangSymbols

class PromptEvolver(SynthLangModule):
    """Evolves prompts using genetic algorithms and self-play tournaments."""

    def __init__(self, lm: Any, population_size: int = 5, mutation_rate: float = 0.3,
                 tournament_size: int = 3, fitness_type: str = 'hybrid', test_cases: Optional[List[Dict]] = None):
        """Initialize evolver module.
        
        Args:
            lm: Language model instance
            population_size: Size of population per generation
            mutation_rate: Rate of mutation between generations (0-1)
            tournament_size: Number of prompts competing in each tournament
            fitness_type: Type of fitness function to use
            test_cases: Optional test cases for task-based fitness
        """
        super().__init__(lm)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.fitness_type = fitness_type
        self.test_cases = test_cases
        
    def _generate_variant(self, prompt: str) -> str:
        """Generate a variant of the prompt through mutation."""
        class MutateSignature(dspy.Signature):
            """Signature for prompt mutation."""
            prompt = dspy.InputField()
            mutated = dspy.OutputField(desc="Mutated version of the prompt following SynthLang format")
            
        mutator = dspy.Predict(MutateSignature)
        
        with dspy.context(lm=self.lm):
            result = mutator(
                prompt=f"""Modify this prompt into SynthLang format with ONE mutation:

Current prompt:
{prompt}

Required format:
↹ input•type
⊕ process => result
Σ output + metrics

Rules:
1. Must start with ↹ for input
2. Use ⊕ for each process step
3. End with Σ for output
4. Join related items with •
5. Use => for transformations
6. Use +, >, <, ^ for operations
7. Keep each line under 30 chars
8. No quotes or descriptions

Example mutations:
1. Add processing step:
   ↹ data•sales
   ⊕ filter>Q1 => subset
   ⊕ analyze => insights
   Σ report + trends

2. Combine steps:
   ↹ data•source
   ⊕ process•analyze => result
   Σ output + metrics

3. Split step:
   ↹ input•stream
   ⊕ validate => clean
   ⊕ transform => final
   Σ result + stats"""
            )
            # Handle both string and object responses
            if hasattr(result, 'mutated'):
                return str(result.mutated).strip()
            else:
                return str(result).strip()
            
    def _calculate_fitness(self, prompt: str) -> Dict[str, float]:
        """Calculate fitness scores for a prompt."""
        # Clarity score based on symbol usage
        clarity = sum(1 for sym in [SynthLangSymbols.INPUT, SynthLangSymbols.PROCESS, SynthLangSymbols.OUTPUT] 
                     if sym in prompt) / 3.0
                     
        # Specificity score based on operators and joins
        specificity = (
            prompt.count("•") * 0.2 +  # Joins
            prompt.count("=>") * 0.2 +  # Transforms
            sum(1 for op in ["+", "-", "*", "/", ">", "<", "^"] if op in prompt) * 0.1
        )
        
        # Task completion score if test cases provided
        task_score = 0.0
        if self.test_cases:
            successes = 0
            for test in self.test_cases:
                class EvalSignature(dspy.Signature):
                    """Signature for prompt evaluation."""
                    prompt = dspy.InputField()
                    test_input = dspy.InputField()
                    expected = dspy.InputField()
                    matches = dspy.OutputField(desc="Whether the prompt would produce the expected output (yes/no)")
                    
                evaluator = dspy.Predict(EvalSignature)
                
                with dspy.context(lm=self.lm):
                    result = evaluator(
                        prompt=prompt,
                        test_input=test['input'],
                        expected=test['expected']
                    )
                    # Handle both string and object responses
                    matches = str(result.matches if hasattr(result, 'matches') else result).lower()
                    if "yes" in matches:
                        successes += 1
            task_score = successes / len(self.test_cases)
            
        # Calculate overall fitness based on type
        if self.fitness_type == 'clarity':
            overall = clarity
        elif self.fitness_type == 'specificity':
            overall = specificity
        elif self.fitness_type == 'task':
            overall = task_score if self.test_cases else clarity
        else:  # hybrid
            weights = [0.3, 0.3, 0.4] if self.test_cases else [0.5, 0.5, 0.0]
            overall = (clarity * weights[0] + 
                      specificity * weights[1] + 
                      task_score * weights[2])
            
        return {
            'clarity': clarity,
            'specificity': specificity,
            'task_score': task_score,
            'overall': overall
        }
        
    def _tournament_select(self, population: List[Dict]) -> Dict:
        """Select best prompt from a tournament."""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        return max(tournament, key=lambda x: x['fitness']['overall'])
        
    def evolve(self, seed_prompt: str, n_generations: int = 10) -> Dict[str, Any]:
        """Evolve prompts through multiple generations.
        
        Args:
            seed_prompt: Initial prompt to evolve from
            n_generations: Number of generations to evolve
            
        Returns:
            Dictionary containing:
                - best_prompt: Best evolved prompt
                - fitness: Fitness scores
                - generations: Number of generations completed
                - total_variants: Total variants created
                - successful_mutations: Count of successful mutations
                - tournament_winners: Count of tournament winners
                - lineage: Full evolutionary history
        """
        # Initialize population with seed prompt
        population = [{'prompt': seed_prompt, 'fitness': self._calculate_fitness(seed_prompt)}]
        
        # Statistics tracking
        stats = {
            'total_variants': 0,
            'successful_mutations': 0,
            'tournament_winners': 0,
            'lineage': [{
                'generation': 0,
                'population': [{'prompt': p['prompt'], 'fitness': p['fitness']} for p in population]
            }]
        }
        
        # Evolution loop
        for gen in range(n_generations):
            # Generate variants
            new_population = []
            while len(new_population) < self.population_size:
                parent = self._tournament_select(population)
                stats['tournament_winners'] += 1
                
                # Try mutation
                if random.random() < self.mutation_rate:
                    variant = self._generate_variant(parent['prompt'])
                    stats['total_variants'] += 1
                    
                    # Calculate fitness and add if better
                    variant_fitness = self._calculate_fitness(variant)
                    if variant_fitness['overall'] > parent['fitness']['overall']:
                        new_population.append({'prompt': variant, 'fitness': variant_fitness})
                        stats['successful_mutations'] += 1
                    else:
                        new_population.append(parent)
                else:
                    new_population.append(parent)
                    
            # Update population
            population = new_population
            
            # Record lineage
            stats['lineage'].append({
                'generation': gen + 1,
                'population': [{'prompt': p['prompt'], 'fitness': p['fitness']} for p in population]
            })
            
        # Find best prompt
        best = max(population, key=lambda x: x['fitness']['overall'])
        
        return {
            'best_prompt': best['prompt'],
            'fitness': best['fitness'],
            'generations': n_generations,
            **stats
        }
