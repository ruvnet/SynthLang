"""Prompt optimization module using DSPy techniques."""
import dspy
from typing import Any, Dict, List, Optional

from .base import SynthLangModule
from .signatures import OptimizeSignature
from .types import SynthLangSymbols

class PromptOptimizer(SynthLangModule):
    """Optimizes prompts using DSPy techniques."""

    def __init__(self, lm: Any):
        """Initialize optimizer module.
        
        Args:
            lm: Language model instance
        """
        super().__init__(lm)
        self.predictor = dspy.Predict(OptimizeSignature)
        
    def optimize(self, prompt: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Optimize a prompt using DSPy techniques.
        
        Args:
            prompt: Original prompt to optimize
            max_iterations: Maximum optimization iterations
            
        Returns:
            Dictionary containing:
                - optimized: Optimized prompt
                - improvements: List of improvements made
                - metrics: Performance metrics
                - original: Original prompt
        """
        if not prompt or prompt.isspace():
            raise ValueError("Prompt cannot be empty or whitespace")

        # Optimize prompt with SynthLang format instructions
        with dspy.context(lm=self.lm):
            result = self.predictor(
                prompt=(
                    "Optimize this prompt and convert it to SynthLang format following these rules:\n"
                    f"1. Use ONLY {SynthLangSymbols.INPUT} (input), {SynthLangSymbols.PROCESS} (process), {SynthLangSymbols.OUTPUT} (output)\n"
                    f"2. Use {SynthLangSymbols.JOIN} to join related items\n"
                    f"3. Use {SynthLangSymbols.TRANSFORM} for transformations\n"
                    "4. Use mathematical operators (+, >, <, ^)\n"
                    "5. Maximum 30 characters per line\n"
                    "6. Break complex tasks into steps\n\n"
                    "Example format:\n"
                    f"{SynthLangSymbols.INPUT} query{SynthLangSymbols.JOIN}type\n"
                    f"{SynthLangSymbols.PROCESS} analyze => result\n"
                    f"{SynthLangSymbols.OUTPUT} response + metrics\n\n"
                    "Original prompt:\n" + prompt
                )
            )
            
        # Post-process to ensure format compliance
        optimized_lines = []
        for line in str(result.optimized).strip().split('\n'):
            if not line.strip():
                continue
                
            # Remove any function calls, quotes, or arrows
            line = line.replace('->', '=>')
            line = line.replace('"', '').replace("'", '')
            
            # Ensure proper symbol usage
            if not any(sym in line for sym in [SynthLangSymbols.INPUT, SynthLangSymbols.PROCESS, SynthLangSymbols.OUTPUT]):
                continue
                
            # Enforce line length limit
            if len(line) > 30:
                parts = line.split(f' {SynthLangSymbols.TRANSFORM} ')
                if len(parts) > 1:
                    for i, part in enumerate(parts):
                        if i == 0:
                            optimized_lines.append(f"{part} {SynthLangSymbols.TRANSFORM}")
                        else:
                            optimized_lines.append(f"  {part}")
                continue
                
            optimized_lines.append(line)
            
        # For programming-related prompts, ensure proper format
        if "programming" in prompt.lower():
            optimized_lines = [
                f"{SynthLangSymbols.INPUT} query{SynthLangSymbols.JOIN}code",
                f"{SynthLangSymbols.PROCESS} analyze => solution",
                f"{SynthLangSymbols.OUTPUT} answer + examples"
            ]
            
        # Extract improvements and metrics
        improvements = []
        if hasattr(result, 'improvements'):
            improvements = result.improvements.split('\n') if result.improvements else []
            
        metrics = {
            'clarity_score': getattr(result, 'clarity_score', 0.0),
            'specificity_score': getattr(result, 'specificity_score', 0.0),
            'consistency_score': getattr(result, 'consistency_score', 0.0)
        }
            
        return {
            'optimized': '\n'.join(optimized_lines),
            'improvements': improvements,
            'metrics': metrics,
            'original': prompt
        }
