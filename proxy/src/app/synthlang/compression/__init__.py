"""
SynthLang compression module.

This module provides a modular system for text compression and decompression
to reduce token usage when communicating with LLMs.
"""
import os
import logging
from typing import Dict, List, Optional, Any, Union

from src.app.synthlang.core import CompressionConfig

# Configure logging
logger = logging.getLogger(__name__)

# Global flag to enable/disable SynthLang compression
ENABLE_SYNTHLANG = CompressionConfig.get_enable_synthlang()

# Import base classes
from .base import BaseCompressor, CompressionResult, CompressorRegistry

# Create a global registry for compressors
registry = CompressorRegistry()

# Import and register compressors
from .basic import BasicCompressor
registry.register("basic", BasicCompressor)

from .abbreviation import AbbreviationCompressor
registry.register("abbreviation", AbbreviationCompressor)

from .vowel import VowelRemovalCompressor
registry.register("vowel", VowelRemovalCompressor)

from .symbol import SymbolCompressor
registry.register("symbol", SymbolCompressor)

from .gzip import GzipCompressor
registry.register("gzip", GzipCompressor)

from .logarithmic import LogarithmicSymbolicCompressor
registry.register("logarithmic", LogarithmicSymbolicCompressor)


def set_synthlang_enabled(enabled: bool) -> None:
    """
    Set whether SynthLang is enabled.
    
    Args:
        enabled: True to enable SynthLang, False to disable
    """
    global ENABLE_SYNTHLANG
    ENABLE_SYNTHLANG = enabled
    logger.info(f"SynthLang {'enabled' if enabled else 'disabled'}")


def is_synthlang_available() -> bool:
    """
    Check if SynthLang compression is available.
    
    Returns:
        True if SynthLang compression is available, False otherwise
    """
    return ENABLE_SYNTHLANG


def compress_prompt(text: str, use_gzip: bool = False, pipeline: Optional[List[str]] = None) -> str:
    """
    Compress a prompt using a pipeline of compression strategies.
    
    Args:
        text: The text to compress
        use_gzip: Whether to apply additional gzip compression (default: False)
        pipeline: List of compressor names to use in the pipeline
                 If None, uses the pipeline for the configured compression level
                 
    Returns:
        The compressed text, or the original text if compression fails
    """
    if not ENABLE_SYNTHLANG:
        return text
        
    if not text:
        return text
        
    # Use default pipeline if none provided
    if pipeline is None:
        pipeline = CompressionConfig.get_pipeline_for_level()
        
    # Add gzip to the pipeline if requested
    if use_gzip and "gzip" not in pipeline:
        pipeline.append("gzip")
        
    try:
        compressed = text
        metrics = {}
        
        # Apply each compressor in the pipeline
        for compressor_name in pipeline:
            compressor_class = registry.get(compressor_name)
            if not compressor_class:
                logger.warning(f"Compressor '{compressor_name}' not found in registry")
                continue
                
            compressor = compressor_class()
            result = compressor.compress(compressed)
            
            if result.success:
                compressed = result.text
                metrics[compressor_name] = result.metrics
            else:
                logger.warning(f"Compression with '{compressor_name}' failed: {result.error}")
                
        logger.info(f"Compressed text from {len(text)} to {len(compressed)} chars using pipeline: {pipeline}")
        return compressed
        
    except Exception as e:
        logger.error(f"Error during compression: {e}")
        return text


def decompress_prompt(text: str, pipeline: Optional[List[str]] = None) -> str:
    """
    Decompress a prompt using a pipeline of decompression strategies.
    
    Args:
        text: The compressed text to decompress
        pipeline: List of compressor names to use in the pipeline (in reverse order)
                 If None, tries to auto-detect the compression methods used
                 
    Returns:
        The decompressed text, or the original text if decompression fails
    """
    if not ENABLE_SYNTHLANG:
        return text
        
    if not text:
        return text
        
    try:
        # Check if gzip compression was used
        if text.startswith("gz:") and "gzip" not in (pipeline or []):
            # Decompress gzip first
            gzip_compressor = GzipCompressor()
            result = gzip_compressor.decompress(text)
            if result.success:
                text = result.text
                # If a pipeline was provided, continue with it
                # Otherwise, try to decompress the result with auto-detection
                if pipeline is None:
                    return decompress_prompt(text)
            else:
                logger.warning(f"Gzip decompression failed: {result.error}")
                
        # Use default pipeline in reverse if none provided
        if pipeline is None:
            # Try to auto-detect the compression methods used
            # This is a simple heuristic and may not always work
            pipeline = []
            
            # Check for symbol compression
            from src.app.synthlang.core import SynthLangSymbols
            symbols = SynthLangSymbols.get_all_symbols().values()
            if any(symbol in text for symbol in symbols):
                pipeline.append("symbol")
                
            # Check for vowel removal (if many words are missing vowels)
            vowel_pattern = r'\b[bcdfghjklmnpqrstvwxyz]{3,}\b'
            import re
            if re.search(vowel_pattern, text):
                pipeline.append("vowel")
                
            # Always include abbreviation and basic as fallbacks
            pipeline.append("abbreviation")
            pipeline.append("basic")
            
            # Reverse the pipeline for decompression
            pipeline = list(reversed(pipeline))
            
        decompressed = text
        metrics = {}
        
        # Apply each decompressor in the pipeline
        for compressor_name in pipeline:
            compressor_class = registry.get(compressor_name)
            if not compressor_class:
                logger.warning(f"Decompressor '{compressor_name}' not found in registry")
                continue
                
            compressor = compressor_class()
            result = compressor.decompress(decompressed)
            
            if result.success:
                decompressed = result.text
                metrics[compressor_name] = result.metrics
            else:
                logger.warning(f"Decompression with '{compressor_name}' failed: {result.error}")
                
        logger.info(f"Decompressed text from {len(text)} to {len(decompressed)} chars using pipeline: {pipeline}")
        return decompressed
        
    except Exception as e:
        logger.error(f"Error during decompression: {e}")
        return text