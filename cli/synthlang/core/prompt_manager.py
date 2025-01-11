"""Prompt management module for storing and retrieving evolved prompts."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import SynthLangModule

class PromptManager(SynthLangModule):
    """Manages storage and retrieval of evolved prompts."""

    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize prompt manager.
        
        Args:
            storage_dir: Optional directory for prompt storage.
                       Defaults to ~/.synthlang/prompts/
        """
        super().__init__(None)  # No LM needed for storage operations
        self.storage_dir = Path(storage_dir or os.path.expanduser("~/.synthlang/prompts"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_prompt_path(self, name: str) -> Path:
        """Get full path for a prompt file."""
        return self.storage_dir / f"{name}.json"
        
    def save(self, name: str, prompt: str, metadata: Optional[Dict] = None) -> None:
        """Save a prompt with metadata.
        
        Args:
            name: Name to save prompt under
            prompt: The prompt content
            metadata: Optional metadata about the prompt
        """
        path = self._get_prompt_path(name)
        
        # Prepare prompt data
        data = {
            "name": name,
            "prompt": prompt,
            "metadata": {
                **(metadata or {}),
                "created": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
        
        # Save to file
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self, name: str) -> Dict[str, Any]:
        """Load a saved prompt.
        
        Args:
            name: Name of prompt to load
            
        Returns:
            Dictionary containing prompt data
            
        Raises:
            FileNotFoundError: If prompt doesn't exist
        """
        path = self._get_prompt_path(name)
        
        if not path.exists():
            raise FileNotFoundError(f"No prompt found with name: {name}")
            
        with open(path) as f:
            return json.load(f)
            
    def list(self) -> List[Dict[str, Any]]:
        """List all saved prompts.
        
        Returns:
            List of prompt data dictionaries
        """
        prompts = []
        for path in self.storage_dir.glob("*.json"):
            with open(path) as f:
                prompts.append(json.load(f))
        return prompts
        
    def delete(self, name: str) -> None:
        """Delete a saved prompt.
        
        Args:
            name: Name of prompt to delete
            
        Raises:
            FileNotFoundError: If prompt doesn't exist
        """
        path = self._get_prompt_path(name)
        
        if not path.exists():
            raise FileNotFoundError(f"No prompt found with name: {name}")
            
        path.unlink()
        
    def compare(self, name1: str, name2: str) -> Dict[str, Any]:
        """Compare two saved prompts.
        
        Args:
            name1: First prompt name
            name2: Second prompt name
            
        Returns:
            Dictionary containing comparison results
            
        Raises:
            FileNotFoundError: If either prompt doesn't exist
        """
        prompt1 = self.load(name1)
        prompt2 = self.load(name2)
        
        # Compare metadata
        metadata1 = prompt1.get("metadata", {})
        metadata2 = prompt2.get("metadata", {})
        
        return {
            "prompts": {
                name1: prompt1["prompt"],
                name2: prompt2["prompt"]
            },
            "metrics": {
                name1: {
                    "fitness": metadata1.get("fitness", {
                        "clarity": 0.0,
                        "specificity": 0.0,
                        "task_score": 0.0,
                        "overall": 0.0
                    }),
                    "generations": metadata1.get("generations", 0),
                    "created": metadata1.get("created"),
                    "evolution_metrics": metadata1.get("evolution_metrics", {})
                },
                name2: {
                    "fitness": metadata2.get("fitness", {
                        "clarity": 0.0,
                        "specificity": 0.0,
                        "task_score": 0.0,
                        "overall": 0.0
                    }),
                    "generations": metadata2.get("generations", 0),
                    "created": metadata2.get("created"),
                    "evolution_metrics": metadata2.get("evolution_metrics", {})
                }
            },
            "differences": {
                "fitness": abs(
                    float(metadata1.get("fitness", {}).get("overall", 0.0)) - 
                    float(metadata2.get("fitness", {}).get("overall", 0.0))
                ),
                "generations": abs(
                    metadata1.get("generations", 0) - 
                    metadata2.get("generations", 0)
                )
            }
        }
