"""
SynthLang core module.

This module imports and re-exports the core modules from the CLI implementation.
"""
import sys
import os
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Add the CLI directory to the Python path to import the core modules
cli_path = Path(__file__).parent.parent.parent.parent.parent / "cli"
if cli_path.exists() and str(cli_path) not in sys.path:
    sys.path.append(str(cli_path))
    logger.debug(f"Added CLI path to Python path: {cli_path}")

# Import core modules from CLI
try:
    from cli.synthlang.core import (
        SynthLangModule,
        FrameworkTranslator,
        SystemPromptGenerator,
        PromptOptimizer,
        PromptEvolver,
        PromptManager,
        PromptClassifier,
        TranslationResult,
        GenerationResult,
        OptimizationResult,
        SynthLangSymbols,
        FormatRules
    )

    __all__ = [
        'SynthLangModule',
        'FrameworkTranslator',
        'SystemPromptGenerator',
        'PromptOptimizer',
        'PromptEvolver',
        'PromptManager',
        'PromptClassifier',
        'TranslationResult',
        'GenerationResult',
        'OptimizationResult',
        'SynthLangSymbols',
        'FormatRules'
    ]
    
    logger.debug("Successfully imported SynthLang core modules from CLI")
except ImportError as e:
    logger.debug(f"Using fallback SynthLang core modules: {e}")
    # Define empty classes as fallbacks
    class SynthLangModule:
        """Fallback SynthLangModule class."""
        def __init__(self, *args, **kwargs):
            logger.debug("Using fallback SynthLangModule")
    
    class FrameworkTranslator(SynthLangModule):
        """Fallback FrameworkTranslator class."""
        def translate(self, *args, **kwargs):
            logger.debug("Using fallback FrameworkTranslator")
            return {"source": "", "target": "", "explanation": "Core modules not available"}
    
    class SystemPromptGenerator(SynthLangModule):
        """Fallback SystemPromptGenerator class."""
        def generate(self, *args, **kwargs):
            logger.debug("Using fallback SystemPromptGenerator")
            return {"prompt": "", "rationale": "", "metadata": {}}
    
    class PromptOptimizer(SynthLangModule):
        """Fallback PromptOptimizer class."""
        def optimize(self, *args, **kwargs):
            logger.debug("Using fallback PromptOptimizer")
            return {"optimized": "", "improvements": [], "metrics": {}, "original": ""}
    
    class PromptEvolver(SynthLangModule):
        """Fallback PromptEvolver class."""
        def evolve(self, *args, **kwargs):
            logger.debug("Using fallback PromptEvolver")
            return {"best_prompt": "", "fitness": {}, "generations": 0}
    
    class PromptManager(SynthLangModule):
        """Fallback PromptManager class."""
        def save(self, *args, **kwargs):
            logger.debug("Using fallback PromptManager")
    
    class PromptClassifier(SynthLangModule):
        """Fallback PromptClassifier class."""
        def classify(self, *args, **kwargs):
            logger.debug("Using fallback PromptClassifier")
            return {"label": "", "explanation": "Core modules not available"}
    
    # Define fallback type dictionaries
    TranslationResult = dict
    GenerationResult = dict
    OptimizationResult = dict
    
    # Define fallback symbols
    class SynthLangSymbols:
        """Fallback SynthLangSymbols class."""
        INPUT = "↹"
        PROCESS = "⊕"
        OUTPUT = "Σ"
        JOIN = "•"
        TRANSFORM = "=>"
    
    class FormatRules:
        """Fallback FormatRules class."""
        MAX_LINE_LENGTH = 30
        VALID_OPERATORS = ["+", "-", "*", "/", ">", "<", "^"]
    
    __all__ = [
        'SynthLangModule',
        'FrameworkTranslator',
        'SystemPromptGenerator',
        'PromptOptimizer',
        'PromptEvolver',
        'PromptManager',
        'PromptClassifier',
        'TranslationResult',
        'GenerationResult',
        'OptimizationResult',
        'SynthLangSymbols',
        'FormatRules'
    ]