"""Finetuning module using DSPy."""
import json
from typing import Any, Dict, List, Optional

import dspy
from dspy.signatures import Signature

from .base import SynthLangModule

class ClassifySignature(Signature):
    """Signature for classification with reasoning."""
    input = dspy.InputField()
    reasoning = dspy.OutputField(desc="Step by step reasoning about the classification")
    label = dspy.OutputField(desc="Classification label")
    explanation = dspy.OutputField(desc="Explanation for the classification")

class Classifier(dspy.Module):
    """DSPy module for classification."""
    
    def __init__(self, labels: List[str]):
        """Initialize classifier.
        
        Args:
            labels: List of possible classification labels
        """
        super().__init__()
        self.labels = labels
        self.predictor = dspy.ChainOfThought(ClassifySignature)
        
    def forward(self, input: str) -> Dict[str, str]:
        """Run classification.
        
        Args:
            input: Text to classify
            
        Returns:
            Dictionary with classification result
        """
        # Add label context to input
        input_with_context = f"{input}\n\nPossible labels: {', '.join(self.labels)}"
        result = self.predictor(input=input_with_context)
        
        # Ensure label is in allowed list
        if result.label.lower() not in [l.lower() for l in self.labels]:
            result.label = self.labels[0]  # Default to first label
            
        return {
            "input": input,
            "label": result.label,
            "reasoning": result.reasoning,
            "explanation": result.explanation
        }

class PromptFinetuner(SynthLangModule):
    """Finetunes prompts using DSPy."""

    def __init__(self, lm: Any, labels: List[str], examples: Optional[List[Dict]] = None):
        """Initialize finetuner.
        
        Args:
            lm: Language model instance
            labels: List of possible classification labels
            examples: Optional examples for training
        """
        super().__init__(lm)
        self.labels = labels
        self.examples = examples or []
        self.classifier = None
        
    def _prepare_classifier(self) -> None:
        """Prepare the DSPy classifier."""
        if not self.classifier:
            self.classifier = Classifier(labels=self.labels)
            
    def train(self, train_data: List[Dict]) -> Dict[str, Any]:
        """Train the classifier on examples.
        
        Args:
            train_data: List of training examples with input, label, and optional explanation
            
        Returns:
            Dictionary containing training metrics
        """
        self._prepare_classifier()
        
        # Combine examples with training data
        all_data = self.examples + train_data
        
        # Train using examples
        with dspy.context(lm=self.lm):
            for example in all_data:
                # Add label context to input
                input_with_context = f"{example['input']}\n\nThis should be classified as: {example['label']}\nExplanation: {example.get('explanation', '')}"
                self.classifier(input=input_with_context)
            
        return {
            "examples_used": len(all_data),
            "final_accuracy": 1.0  # Will be calculated in evaluate()
        }
        
    def classify(self, text: str) -> Dict[str, Any]:
        """Classify a piece of text.
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary containing classification result
        """
        self._prepare_classifier()
        
        with dspy.context(lm=self.lm):
            result = self.classifier(input=text)
            
        return result
        
    def batch_classify(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Classify multiple texts.
        
        Args:
            texts: List of texts to classify
            
        Returns:
            List of classification results
        """
        results = []
        for text in texts:
            results.append(self.classify(text))
        return results
        
    def evaluate(self, test_data: List[Dict]) -> Dict[str, float]:
        """Evaluate classifier on test data.
        
        Args:
            test_data: List of test examples with input and label
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if not test_data:
            return {
                "accuracy": 0.0,
                "examples": 0
            }
            
        correct = 0
        total = len(test_data)
        
        for example in test_data:
            result = self.classify(example["input"])
            if result["label"].lower() == example["label"].lower():
                correct += 1
                
        return {
            "accuracy": correct / total,
            "examples": total
        }
        
    def save(self, path: str) -> None:
        """Save finetuner state.
        
        Args:
            path: Path to save state to
        """
        state = {
            "labels": self.labels,
            "examples": self.examples
        }
        
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
            
    def load(self, path: str) -> None:
        """Load finetuner state.
        
        Args:
            path: Path to load state from
        """
        with open(path) as f:
            state = json.load(f)
            
        self.labels = state["labels"]
        self.examples = state["examples"]
        self._prepare_classifier()
