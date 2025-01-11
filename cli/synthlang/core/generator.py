"""System prompt generator module implementation."""
import dspy
from datetime import datetime
from typing import Any

from .base import SynthLangModule
from .signatures import GenerateSignature
from .types import GenerationResult, SynthLangSymbols

class SystemPromptGenerator(SynthLangModule):
    """Generates system prompts from task descriptions."""

    def __init__(self, lm: Any):
        """Initialize generator module.
        
        Args:
            lm: Language model instance
        """
        super().__init__(lm)
        self.predictor = dspy.Predict(GenerateSignature)

    def forward(self, task_description: str) -> GenerationResult:
        """Generate a system prompt from task description.
        
        Args:
            task_description: Description of the task
            
        Returns:
            Dictionary containing:
                - prompt: Generated system prompt in SynthLang format
                - rationale: Design rationale
                - metadata: Additional metadata
                
        Raises:
            ValueError: If task description is empty or whitespace
        """
        if not task_description or task_description.isspace():
            raise ValueError("Task description cannot be empty or whitespace")

        # Generate prompt with SynthLang format instructions
        with dspy.context(lm=self.lm):
            result = self.predictor(
                task=(
                    "Convert this task into a SynthLang format system prompt following these rules:\n"
                    f"1. Use ONLY {SynthLangSymbols.INPUT} (input), {SynthLangSymbols.PROCESS} (process), {SynthLangSymbols.OUTPUT} (output)\n"
                    f"2. Use {SynthLangSymbols.JOIN} to join related items\n"
                    f"3. Use {SynthLangSymbols.TRANSFORM} for transformations\n"
                    "4. Use mathematical operators (+, >, <, ^)\n"
                    "5. Maximum 30 characters per line\n"
                    "6. Break complex tasks into steps\n\n"
                    "Task: " + task_description
                )
            )

        # Post-process to ensure format compliance
        prompt_lines = []
        for line in str(result.prompt).strip().split('\n'):
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
                            prompt_lines.append(f"{part} {SynthLangSymbols.TRANSFORM}")
                        else:
                            prompt_lines.append(f"  {part}")
                continue
                
            prompt_lines.append(line)

        # Ensure metadata is a dictionary with required fields
        metadata = {
            "model": "gpt-4o-mini",
            "timestamp": datetime.now().isoformat(),
            "task_type": "system_prompt_generation",
            "format": "synthlang"
        }

        return {
            "prompt": '\n'.join(prompt_lines),
            "rationale": str(result.rationale),
            "metadata": metadata
        }

    def generate(self, task_description: str) -> GenerationResult:
        """Generate prompt using forward method."""
        return self.forward(task_description)
