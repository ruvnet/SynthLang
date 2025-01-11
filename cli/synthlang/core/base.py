"""Base module for SynthLang DSPy implementations."""
from typing import Any
import dspy

class SynthLangModule(dspy.Module):
    """Base module for SynthLang DSPy implementations."""
    
    def __init__(self, lm: Any):
        """Initialize module with language model.
        
        Args:
            lm: DSPy language model instance
        """
        super().__init__()
        self.lm = lm
        dspy.configure(lm=self.lm)
