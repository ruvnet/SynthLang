"""Classification module using DSPy."""
import json
from typing import Any, Dict, List, Optional

from .base import SynthLangModule
from .finetune import PromptFinetuner

class PromptClassifier(SynthLangModule):
    """Classifies prompts using DSPy."""

    def __init__(self, lm: Any, labels: List[str], bootstrap_examples: Optional[List[Dict]] = None):
        """Initialize classifier module.
        
        Args:
            lm: Language model instance
            labels: List of possible classification labels
            bootstrap_examples: Optional examples for bootstrapping
        """
        super().__init__(lm)
        self.finetuner = PromptFinetuner(
            lm=lm,
            labels=labels,
            examples=bootstrap_examples
        )
        
    def train(self, train_data: List[Dict]) -> Dict[str, Any]:
        """Train the classifier on examples.
        
        Args:
            train_data: List of training examples with input, label, and optional explanation
            
        Returns:
            Dictionary containing training metrics
        """
        return self.finetuner.train(train_data)
        
    def classify(self, text: str) -> Dict[str, Any]:
        """Classify a piece of text.
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary containing classification result
        """
        return self.finetuner.classify(text)
        
    def batch_classify(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Classify multiple texts.
        
        Args:
            texts: List of texts to classify
            
        Returns:
            List of classification results
        """
        return self.finetuner.batch_classify(texts)
        
    def evaluate(self, test_data: List[Dict]) -> Dict[str, float]:
        """Evaluate classifier on test data.
        
        Args:
            test_data: List of test examples with input and label
            
        Returns:
            Dictionary containing evaluation metrics
        """
        return self.finetuner.evaluate(test_data)
        
    def save(self, path: str) -> None:
        """Save classifier state.
        
        Args:
            path: Path to save state to
        """
        self.finetuner.save(path)
            
    def load(self, path: str) -> None:
        """Load classifier state.
        
        Args:
            path: Path to load state from
        """
        self.finetuner.load(path)
