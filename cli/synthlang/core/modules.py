"""DSPy module implementations for SynthLang."""
from typing import Any, Dict

import dspy
from dspy.signatures import Signature
from dspy.signatures.field import InputField, OutputField

class TranslateSignature(Signature):
    """Signature for framework translation."""
    source = InputField(desc="Source code to translate")
    target = OutputField(desc="Translated code in target language")
    explanation = OutputField(desc="Explanation of translation changes")

    def __init__(self):
        super().__init__()
        self.instructions = (
            "Translate source code from JavaScript to Python. "
            "Convert JavaScript syntax, idioms, and built-in functions to their Python equivalents. "
            "For example:\n"
            "- Replace console.log() with print()\n"
            "- Convert function declarations to def statements\n"
            "- Adjust indentation to Python style\n"
            "- Remove semicolons and curly braces\n"
            "- Convert camelCase to snake_case where appropriate\n"
            "Provide the translated Python code and explain the key changes made."
        )

class GenerateSignature(Signature):
    """Signature for system prompt generation."""
    task = InputField(desc="Task description")
    prompt = OutputField(desc="Generated system prompt")
    rationale = OutputField(desc="Design rationale")
    metadata = OutputField(desc="Additional metadata")

    def __init__(self):
        super().__init__()
        self.instructions = (
            "Generate a system prompt from a task description. "
            "Input: task description. "
            "Output: prompt, rationale, and metadata."
        )

class SynthLangModule(dspy.Module):
    """Base module for SynthLang DSPy implementations."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize module with language model.
        
        Args:
            api_key: OpenAI API key
            model: Model identifier
        """
        super().__init__()
        self.lm = dspy.LM(model=model, api_key=api_key)
        dspy.configure(lm=self.lm)

class FrameworkTranslator(SynthLangModule):
    """Translates code between different frameworks."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize translator module.
        
        Args:
            api_key: OpenAI API key
            model: Model identifier
        """
        super().__init__(api_key, model)
        self.predictor = dspy.Predict(TranslateSignature)

    def forward(self, source_code: str) -> Dict[str, Any]:
        """Translate source code to target framework.
        
        Args:
            source_code: Source code to translate
            
        Returns:
            Dictionary containing:
                - source: Original source code
                - target: Translated code
                - explanation: Translation explanation
                
        Raises:
            ValueError: If source code is empty or whitespace
        """
        if not source_code or source_code.isspace():
            raise ValueError("Source code cannot be empty or whitespace")

        # Generate translation
        with dspy.context(lm=self.lm):
            result = self.predictor(source=source_code)

        return {
            "source": source_code,
            "target": str(result.target),
            "explanation": str(result.explanation)
        }

    def translate(self, source_code: str) -> Dict[str, Any]:
        """Translate source code using forward method."""
        return self.forward(source_code)

class SystemPromptGenerator(SynthLangModule):
    """Generates system prompts from task descriptions."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize generator module.
        
        Args:
            api_key: OpenAI API key
            model: Model identifier
        """
        super().__init__(api_key, model)
        self.predictor = dspy.Predict(GenerateSignature)

    def forward(self, task_description: str) -> Dict[str, Any]:
        """Generate a system prompt from task description.
        
        Args:
            task_description: Description of the task
            
        Returns:
            Dictionary containing:
                - prompt: Generated system prompt
                - rationale: Design rationale
                - metadata: Additional metadata
                
        Raises:
            ValueError: If task description is empty or whitespace
        """
        if not task_description or task_description.isspace():
            raise ValueError("Task description cannot be empty or whitespace")

        # Generate prompt
        with dspy.context(lm=self.lm):
            result = self.predictor(task=task_description)

        return {
            "prompt": str(result.prompt),
            "rationale": str(result.rationale),
            "metadata": dict(result.metadata)
        }

    def generate(self, task_description: str) -> Dict[str, Any]:
        """Generate prompt using forward method."""
        return self.forward(task_description)
