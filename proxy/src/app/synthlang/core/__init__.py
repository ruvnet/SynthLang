"""
SynthLang core module.

This module defines core SynthLang symbols and format rules used for
compression and other operations.
"""
import os
from enum import Enum
from typing import List, Dict, Any, Set

# Import and expose core classes
from .module import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator,
    PromptOptimizer,
    PromptEvolver,
    PromptClassifier,
    PromptManager,
    TranslationResult,
    GenerationResult,
    OptimizationResult
)


class SynthLangSymbols:
    """
    SynthLang symbols used for compression and representation.
    
    These symbols are used to represent common patterns in a more
    concise way, reducing token usage when communicating with LLMs.
    """
    # Core symbols
    INPUT = "↹"
    PROCESS = "⊕"
    OUTPUT = "Σ"
    JOIN = "•"
    TRANSFORM = "=>"
    
    # Additional symbols
    CONDITION = "?"
    ITERATION = "@"
    LOOP = "#"
    OR = "|"
    AND = "&"
    NOT = "!"
    
    # Mathematical symbols
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    GREATER = ">"
    LESS = "<"
    POWER = "^"
    EQUAL = "="
    
    # Extended symbols from the documentation
    SUBSET = "⊂"
    FLOW = "→"
    EQUIVALENCE = "≡"
    THEREFORE = "∴"
    FORALL = "∀"
    EXISTS = "∃"
    
    @classmethod
    def get_all_symbols(cls) -> Dict[str, str]:
        """Get all SynthLang symbols as a dictionary."""
        return {
            name: value for name, value in vars(cls).items()
            if not name.startswith('_') and isinstance(value, str)
        }
    
    @classmethod
    def get_symbol_by_name(cls, name: str) -> str:
        """Get a symbol by its name."""
        return getattr(cls, name, None)


class FormatRules:
    """
    SynthLang format rules for compression and representation.
    
    These rules define how SynthLang text should be formatted and
    what patterns are allowed in the compressed representation.
    """
    # Maximum line length for SynthLang format
    MAX_LINE_LENGTH = 30
    
    # Valid mathematical operators
    VALID_OPERATORS = {
        "+", "-", "*", "/", ">", "<", "^", "="
    }
    
    # Valid symbols for SynthLang format
    VALID_SYMBOLS = set(SynthLangSymbols.get_all_symbols().values())
    
    # Rules for SynthLang format
    RULES = [
        "Use ONLY these symbols: ↹ (input), ⊕ (process), Σ (output)",
        "NO quotes, arrows, or descriptions",
        "Use • to join related items",
        "Use => for transformations",
        "Maximum 30 characters per line",
        "Use mathematical operators (+, >, <, ^)",
        "Break complex tasks into steps"
    ]
    
    @classmethod
    def get_rules_text(cls) -> str:
        """Get the rules as a formatted text."""
        return "\n".join([f"{i+1}. {rule}" for i, rule in enumerate(cls.RULES)])
    
    @classmethod
    def is_valid_symbol(cls, symbol: str) -> bool:
        """Check if a symbol is valid in SynthLang format."""
        return symbol in cls.VALID_SYMBOLS or symbol in cls.VALID_OPERATORS
    
    @classmethod
    def is_valid_line(cls, line: str) -> bool:
        """Check if a line is valid in SynthLang format."""
        return len(line) <= cls.MAX_LINE_LENGTH


class CompressionConfig:
    """
    Configuration for SynthLang compression.
    
    This class provides configuration options for the compression
    system, with defaults that can be overridden by environment
    variables.
    """
    # Default compression settings
    DEFAULT_ENABLE_SYNTHLANG = True
    DEFAULT_COMPRESSION_LEVEL = "medium"  # low, medium, high
    DEFAULT_USE_GZIP = False
    DEFAULT_MAX_LINE_LENGTH = 30
    
    # Environment variable names
    ENV_ENABLE_SYNTHLANG = "USE_SYNTHLANG"
    ENV_COMPRESSION_LEVEL = "SYNTHLANG_COMPRESSION_LEVEL"
    ENV_USE_GZIP = "SYNTHLANG_USE_GZIP"
    ENV_MAX_LINE_LENGTH = "SYNTHLANG_MAX_LINE_LENGTH"
    
    @classmethod
    def get_enable_synthlang(cls) -> bool:
        """Get whether SynthLang compression is enabled."""
        env_value = os.environ.get(cls.ENV_ENABLE_SYNTHLANG)
        if env_value is not None:
            return env_value.lower() in ("1", "true", "yes", "on")
        return cls.DEFAULT_ENABLE_SYNTHLANG
    
    @classmethod
    def get_compression_level(cls) -> str:
        """Get the compression level."""
        env_value = os.environ.get(cls.ENV_COMPRESSION_LEVEL)
        if env_value is not None and env_value.lower() in ("low", "medium", "high"):
            return env_value.lower()
        return cls.DEFAULT_COMPRESSION_LEVEL
    
    @classmethod
    def get_use_gzip(cls) -> bool:
        """Get whether to use gzip compression."""
        env_value = os.environ.get(cls.ENV_USE_GZIP)
        if env_value is not None:
            return env_value.lower() in ("1", "true", "yes", "on")
        return cls.DEFAULT_USE_GZIP
    
    @classmethod
    def get_max_line_length(cls) -> int:
        """Get the maximum line length."""
        env_value = os.environ.get(cls.ENV_MAX_LINE_LENGTH)
        if env_value is not None and env_value.isdigit():
            return int(env_value)
        return cls.DEFAULT_MAX_LINE_LENGTH
    
    @classmethod
    def get_pipeline_for_level(cls, level: str = None) -> List[str]:
        """
        Get the compression pipeline for a given compression level.
        
        Args:
            level: Compression level (low, medium, high)
                  If None, uses the configured level
                  
        Returns:
            List of compressor names to use in the pipeline
        """
        if level is None:
            level = cls.get_compression_level()
            
        if level == "low":
            return ["basic", "abbreviation"]
        elif level == "medium":
            return ["basic", "abbreviation", "vowel"]
        elif level == "high":
            return ["basic", "abbreviation", "vowel", "symbol", "logarithmic"]
        else:
            # Default to medium if an invalid level is provided
            return ["basic", "abbreviation", "vowel"]