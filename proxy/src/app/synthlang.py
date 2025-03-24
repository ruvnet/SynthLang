"""
SynthLang integration module.

This module provides functions for integrating with the SynthLang CLI
for prompt compression and decompression.
"""
import subprocess
import logging
import gzip
import base64
from typing import Optional
from app.config import USE_SYNTHLANG

# Configure logging
logger = logging.getLogger(__name__)

# Toggle to enable/disable SynthLang from configuration
ENABLE_SYNTHLANG = USE_SYNTHLANG


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
    Check if SynthLang CLI is available.
    
    Returns:
        True if SynthLang CLI is available, False otherwise
    """
    if not ENABLE_SYNTHLANG:
        return False
    
    try:
        # Try to run a simple SynthLang command
        result = subprocess.run(
            ["synthlang", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("SynthLang CLI is not available")
        return False


def compress_prompt(text: str, use_gzip: bool = False) -> str:
    """
    Compress a prompt using SynthLang CLI with optional gzip compression.
    
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
    if not text or not ENABLE_SYNTHLANG:
        return text  # No compression if disabled or empty text
    
    try:
        # Run the synthlang CLI to compress the text
        proc = subprocess.run(
            ["synthlang", "compress"],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        compressed = proc.stdout.strip()
        
        # If compression returned empty string or failed, return original
        if not compressed:
            logger.warning("SynthLang compression returned empty result")
            return text
        
        # Apply additional gzip compression if requested
        if use_gzip and compressed:
            try:
                # Convert to bytes, compress with gzip, then encode as base64 string
                compressed_bytes = compressed.encode('utf-8')
                gzipped = gzip.compress(compressed_bytes)
                b64_compressed = base64.b64encode(gzipped).decode('ascii')
                
                # Add a prefix to indicate this is gzipped
                final_compressed = f"gz:{b64_compressed}"
                
                logger.info(f"Compressed text from {len(text)} to {len(compressed)} chars with SynthLang, "
                           f"then to {len(final_compressed)} chars with gzip")
                return final_compressed
            except Exception as e:
                logger.error(f"Gzip compression failed: {e}")
                # Fall back to regular SynthLang compression
                logger.info(f"Compressed text from {len(text)} to {len(compressed)} characters")
                return compressed
        
        logger.info(f"Compressed text from {len(text)} to {len(compressed)} characters")
        return compressed
    except subprocess.TimeoutExpired:
        logger.error("SynthLang compression timed out")
        return text
    except subprocess.CalledProcessError as e:
        logger.error(f"SynthLang compression error: {e}, stderr: {e.stderr}")
        return text
    except Exception as e:
        logger.error(f"Unexpected error during SynthLang compression: {e}")
        return text


def decompress_prompt(text: str) -> str:
    """
    Decompress a prompt using SynthLang CLI, with automatic gzip decompression if needed.
    
    Args:
        text: The compressed text to decompress
        
    Returns:
        The decompressed text, or the original text if decompression fails
    """
    if not text or not ENABLE_SYNTHLANG:
        return text  # No decompression if disabled or empty text
    
    # Check if this is a gzipped compressed text
    if text.startswith("gz:"):
        try:
            # Extract the base64 encoded gzipped data
            b64_data = text[3:]  # Skip the "gz:" prefix
            gzipped = base64.b64decode(b64_data)
            decompressed_bytes = gzip.decompress(gzipped)
            text = decompressed_bytes.decode('utf-8')
            logger.info(f"Decompressed gzipped text from {len(b64_data)} to {len(text)} characters")
        except Exception as e:
            logger.error(f"Gzip decompression failed: {e}")
            # Continue with regular decompression if gzip fails
    
    try:
        # Run the synthlang CLI to decompress the text
        proc = subprocess.run(
            ["synthlang", "decompress"],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        decompressed = proc.stdout.strip()
        
        # If decompression returned empty string or failed, return original
        if not decompressed:
            logger.warning("SynthLang decompression returned empty result")
            return text
        
        logger.info(f"Decompressed text from {len(text)} to {len(decompressed)} characters")
        return decompressed
    except subprocess.TimeoutExpired:
        logger.error("SynthLang decompression timed out")
        return text
    except subprocess.CalledProcessError as e:
        logger.error(f"SynthLang decompression error: {e}, stderr: {e.stderr}")
        return text
    except Exception as e:
        logger.error(f"Unexpected error during SynthLang decompression: {e}")
        return text