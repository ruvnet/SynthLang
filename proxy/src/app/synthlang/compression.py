"""
SynthLang compression module.

This module provides functions for text compression and decompression
to reduce token usage when communicating with LLMs.

This is a compatibility layer that redirects to the new modular compression system.
"""
import logging
from typing import Optional, List

# Import from the new modular system
from src.app.synthlang.compression import (
    set_synthlang_enabled as _set_synthlang_enabled,
    is_synthlang_available as _is_synthlang_available,
    compress_prompt as _compress_prompt,
    decompress_prompt as _decompress_prompt,
    ENABLE_SYNTHLANG
)

# Configure logging
logger = logging.getLogger(__name__)


def set_synthlang_enabled(enabled: bool) -> None:
    """
    Set whether SynthLang is enabled.
    
    Args:
        enabled: True to enable SynthLang, False to disable
    """
    _set_synthlang_enabled(enabled)
    logger.info(f"SynthLang {'enabled' if enabled else 'disabled'}")


def is_synthlang_available() -> bool:
    """
    Check if SynthLang compression is available.
    
    Returns:
        True if SynthLang compression is available, False otherwise
    """
    return _is_synthlang_available()


def compress_text(text: str) -> str:
    """
    Compress text by removing redundant characters and using abbreviations.
    
    This is a compatibility function that uses the new modular system.
    
    Args:
        text: The text to compress
        
    Returns:
        The compressed text
    """
    # Use the new system with a specific pipeline for backward compatibility
    pipeline = ["basic", "abbreviation", "vowel"]
    return _compress_prompt(text, use_gzip=False, pipeline=pipeline)


def decompress_text(text: str) -> str:
    """
    Decompress text by expanding abbreviations.
    
    This is a compatibility function that uses the new modular system.
    
    Args:
        text: The compressed text to decompress
        
    Returns:
        The decompressed text (best effort)
    """
    # Use the new system with a specific pipeline for backward compatibility
    pipeline = ["vowel", "abbreviation", "basic"]
    return _decompress_prompt(text, pipeline=pipeline)


def compress_prompt(text: str, use_gzip: bool = False) -> str:
    """
    Compress a prompt with optional gzip compression.
    
    Args:
        text: The text to compress
        use_gzip: Whether to apply additional gzip compression (default: False)
        
    Returns:
        The compressed text, or the original text if compression fails
        
    Benefits of gzip compression:
        - Further reduces token count for very large prompts
        - Provides better compression for repetitive text patterns
        - Reduces API costs for large batch processing
        - Useful for storing compressed prompts in databases
    """
    return _compress_prompt(text, use_gzip=use_gzip)


def decompress_prompt(text: str) -> str:
    """
    Decompress a prompt, with automatic gzip decompression if needed.
    
    Args:
        text: The compressed text to decompress
        
    Returns:
        The decompressed text, or the original text if decompression fails
    """
    return _decompress_prompt(text)