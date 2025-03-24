"""
SynthLang API interface.

This module provides a clean API interface to the SynthLang core functionality.
"""
import logging
from typing import Any, Dict, List, Optional, Union
import os

from src.app.config import USE_SYNTHLANG
from src.app.synthlang.compression import compress_prompt, decompress_prompt
from src.app.synthlang.core import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator,
    PromptOptimizer,
    PromptEvolver,
    PromptClassifier,
    PromptManager,
    TranslationResult,
    GenerationResult,
    OptimizationResult,
    SynthLangSymbols,
    FormatRules
)

# Configure logging
logger = logging.getLogger(__name__)

# Toggle to enable/disable SynthLang from configuration
ENABLE_SYNTHLANG = USE_SYNTHLANG


class SynthLangAPI:
    """API interface for SynthLang functionality."""
    
    def __init__(self, lm: Optional[Any] = None, storage_dir: Optional[str] = None):
        """
        Initialize SynthLang API with optional language model.
        
        Args:
            lm: Optional language model instance
            storage_dir: Optional directory for prompt storage
        """
        self.lm = lm
        self.enabled = ENABLE_SYNTHLANG
        
        # Initialize core modules if enabled
        if self.enabled:
            try:
                self.translator = FrameworkTranslator(lm) if lm else None
                self.generator = SystemPromptGenerator(lm) if lm else None
                self.optimizer = PromptOptimizer(lm) if lm else None
                self.evolver = PromptEvolver(lm) if lm else None
                self.classifier = None  # Initialize on demand with labels
                self.prompt_manager = PromptManager(storage_dir)
                logger.info("SynthLang API initialized with core modules")
            except Exception as e:
                logger.error(f"Failed to initialize SynthLang API: {e}")
                self.enabled = False
        
    def set_enabled(self, enabled: bool) -> None:
        """
        Set whether SynthLang API is enabled.
        
        Args:
            enabled: True to enable SynthLang API, False to disable
        """
        self.enabled = enabled
        logger.info(f"SynthLang API {'enabled' if enabled else 'disabled'}")
    
    def is_enabled(self) -> bool:
        """
        Check if SynthLang API is enabled.
        
        Returns:
            True if SynthLang API is enabled, False otherwise
        """
        return self.enabled
    
    def set_language_model(self, lm: Any) -> None:
        """
        Set the language model for SynthLang API.
        
        Args:
            lm: Language model instance
        """
        if not self.enabled:
            logger.warning("SynthLang API is disabled, not setting language model")
            return
            
        self.lm = lm
        
        # Update language model for core modules
        if hasattr(self, 'translator') and self.translator:
            self.translator.lm = lm
        if hasattr(self, 'generator') and self.generator:
            self.generator.lm = lm
        if hasattr(self, 'optimizer') and self.optimizer:
            self.optimizer.lm = lm
        if hasattr(self, 'evolver') and self.evolver:
            self.evolver.lm = lm
        if hasattr(self, 'classifier') and self.classifier:
            self.classifier.lm = lm
            
        logger.info("Updated language model for SynthLang API")
    
    def compress(self, text: str, use_gzip: bool = False) -> str:
        """
        Compress a prompt using SynthLang.
        
        Args:
            text: The text to compress
            use_gzip: Whether to apply additional gzip compression
            
        Returns:
            The compressed text, or the original text if compression fails
        """
        if not self.enabled:
            return text
            
        return compress_prompt(text, use_gzip)
    
    def decompress(self, text: str) -> str:
        """
        Decompress a prompt using SynthLang.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            The decompressed text, or the original text if decompression fails
        """
        if not self.enabled:
            return text
            
        return decompress_prompt(text)
    
    def translate(self, text: str, instructions: Optional[str] = None) -> TranslationResult:
        """
        Translate natural language to SynthLang format.
        
        Args:
            text: The text to translate
            instructions: Optional custom translation instructions
            
        Returns:
            Dictionary containing translation result
        """
        if not self.enabled or not self.translator or not self.lm:
            logger.warning("SynthLang API is disabled or translator not initialized")
            return {"source": text, "target": text, "explanation": "Translation not available"}
            
        try:
            return self.translator.translate(text, instructions)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {"source": text, "target": text, "explanation": f"Error: {str(e)}"}
    
    def generate(self, task_description: str) -> GenerationResult:
        """
        Generate a system prompt from task description.
        
        Args:
            task_description: Description of the task
            
        Returns:
            Dictionary containing generation result
        """
        if not self.enabled or not self.generator or not self.lm:
            logger.warning("SynthLang API is disabled or generator not initialized")
            return {"prompt": "", "rationale": "Generation not available", "metadata": {}}
            
        try:
            return self.generator.generate(task_description)
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return {"prompt": "", "rationale": f"Error: {str(e)}", "metadata": {}}
    
    def optimize(self, prompt: str, max_iterations: int = 5) -> OptimizationResult:
        """
        Optimize a prompt using SynthLang.
        
        Args:
            prompt: The prompt to optimize
            max_iterations: Maximum optimization iterations
            
        Returns:
            Dictionary containing optimization result
        """
        if not self.enabled or not self.optimizer or not self.lm:
            logger.warning("SynthLang API is disabled or optimizer not initialized")
            return {"optimized": prompt, "improvements": [], "metrics": {}, "original": prompt}
            
        try:
            return self.optimizer.optimize(prompt, max_iterations)
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return {"optimized": prompt, "improvements": [], "metrics": {}, "original": prompt}
    
    def evolve(self, seed_prompt: str, n_generations: int = 10) -> Dict[str, Any]:
        """
        Evolve a prompt using SynthLang.
        
        Args:
            seed_prompt: Initial prompt to evolve from
            n_generations: Number of generations to evolve
            
        Returns:
            Dictionary containing evolution result
        """
        if not self.enabled or not self.evolver or not self.lm:
            logger.warning("SynthLang API is disabled or evolver not initialized")
            return {"best_prompt": seed_prompt, "fitness": {}, "generations": 0}
            
        try:
            return self.evolver.evolve(seed_prompt, n_generations)
        except Exception as e:
            logger.error(f"Evolution error: {e}")
            return {"best_prompt": seed_prompt, "fitness": {}, "generations": 0}
    
    def classify(self, text: str, labels: List[str]) -> Dict[str, Any]:
        """
        Classify a prompt using SynthLang.
        
        Args:
            text: The text to classify
            labels: List of possible classification labels
            
        Returns:
            Dictionary containing classification result
        """
        if not self.enabled or not self.lm:
            logger.warning("SynthLang API is disabled or language model not initialized")
            return {"input": text, "label": "", "explanation": "Classification not available"}
            
        # Initialize classifier if not already initialized or if labels changed
        if not hasattr(self, 'classifier') or not self.classifier or not hasattr(self.classifier, 'labels') or self.classifier.labels != labels:
            try:
                self.classifier = PromptClassifier(self.lm, labels)
                logger.info(f"Initialized classifier with labels: {labels}")
            except Exception as e:
                logger.error(f"Failed to initialize classifier: {e}")
                return {"input": text, "label": "", "explanation": f"Error: {str(e)}"}
            
        try:
            return self.classifier.classify(text)
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {"input": text, "label": "", "explanation": f"Error: {str(e)}"}
    
    def save_prompt(self, name: str, prompt: str, metadata: Optional[Dict] = None) -> None:
        """
        Save a prompt with metadata.
        
        Args:
            name: Name to save prompt under
            prompt: The prompt content
            metadata: Optional metadata about the prompt
        """
        if not self.enabled or not hasattr(self, 'prompt_manager') or not self.prompt_manager:
            logger.warning("SynthLang API is disabled or prompt manager not initialized")
            return
            
        try:
            self.prompt_manager.save(name, prompt, metadata)
            logger.info(f"Saved prompt: {name}")
        except Exception as e:
            logger.error(f"Failed to save prompt: {e}")
    
    def load_prompt(self, name: str) -> Dict[str, Any]:
        """
        Load a saved prompt.
        
        Args:
            name: Name of prompt to load
            
        Returns:
            Dictionary containing prompt data
        """
        if not self.enabled or not hasattr(self, 'prompt_manager') or not self.prompt_manager:
            logger.warning("SynthLang API is disabled or prompt manager not initialized")
            return {"name": name, "prompt": "", "metadata": {}}
            
        try:
            return self.prompt_manager.load(name)
        except FileNotFoundError:
            logger.warning(f"No prompt found with name: {name}")
            return {"name": name, "prompt": "", "metadata": {}}
        except Exception as e:
            logger.error(f"Failed to load prompt: {e}")
            return {"name": name, "prompt": "", "metadata": {}}
    
    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        List all saved prompts.
        
        Returns:
            List of prompt data dictionaries
        """
        if not self.enabled or not hasattr(self, 'prompt_manager') or not self.prompt_manager:
            logger.warning("SynthLang API is disabled or prompt manager not initialized")
            return []
            
        try:
            return self.prompt_manager.list()
        except Exception as e:
            logger.error(f"Failed to list prompts: {e}")
            return []
    
    def delete_prompt(self, name: str) -> bool:
        """
        Delete a saved prompt.
        
        Args:
            name: Name of prompt to delete
            
        Returns:
            True if prompt was deleted, False otherwise
        """
        if not self.enabled or not hasattr(self, 'prompt_manager') or not self.prompt_manager:
            logger.warning("SynthLang API is disabled or prompt manager not initialized")
            return False
            
        try:
            self.prompt_manager.delete(name)
            logger.info(f"Deleted prompt: {name}")
            return True
        except FileNotFoundError:
            logger.warning(f"No prompt found with name: {name}")
            return False
        except Exception as e:
            logger.error(f"Failed to delete prompt: {e}")
            return False
    
    def compare_prompts(self, name1: str, name2: str) -> Dict[str, Any]:
        """
        Compare two saved prompts.
        
        Args:
            name1: First prompt name
            name2: Second prompt name
            
        Returns:
            Dictionary containing comparison results
        """
        if not self.enabled or not hasattr(self, 'prompt_manager') or not self.prompt_manager:
            logger.warning("SynthLang API is disabled or prompt manager not initialized")
            return {"prompts": {}, "metrics": {}, "differences": {}}
            
        try:
            return self.prompt_manager.compare(name1, name2)
        except FileNotFoundError as e:
            logger.warning(f"Prompt comparison failed: {e}")
            return {"prompts": {}, "metrics": {}, "differences": {}}
        except Exception as e:
            logger.error(f"Failed to compare prompts: {e}")
            return {"prompts": {}, "metrics": {}, "differences": {}}


# Create a singleton instance of SynthLangAPI
synthlang_api = SynthLangAPI()