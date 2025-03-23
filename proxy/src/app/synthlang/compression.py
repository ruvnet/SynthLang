"""
SynthLang compression module.

This module provides functions for text compression and decompression
to reduce token usage when communicating with LLMs.
"""
import logging
import gzip
import base64
import re
from typing import Optional
from src.app.config import USE_SYNTHLANG

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
    Check if SynthLang compression is available.
    
    Returns:
        True if SynthLang compression is available, False otherwise
    """
    return ENABLE_SYNTHLANG


def compress_text(text: str) -> str:
    """
    Compress text by removing redundant characters and using abbreviations.
    
    This is a simple implementation that:
    1. Removes redundant whitespace
    2. Shortens common words and phrases
    3. Uses abbreviations
    4. Removes vowels from some words
    
    Args:
        text: The text to compress
        
    Returns:
        The compressed text
    """
    if not text:
        return text
    
    # Step 1: Remove redundant whitespace
    compressed = re.sub(r'\s+', ' ', text.strip())
    
    # Step 2: Common word replacements
    replacements = {
        'the ': 't ',
        ' the ': ' t ',
        'and ': '& ',
        ' and ': ' & ',
        'with ': 'w/ ',
        ' with ': ' w/ ',
        'without ': 'w/o ',
        ' without ': ' w/o ',
        'information': 'info',
        'application': 'app',
        'example': 'ex',
        'function': 'fn',
        'implementation': 'impl',
        'configuration': 'config',
        'database': 'db',
        'message': 'msg',
        'response': 'resp',
        'request': 'req',
        'error': 'err',
        'document': 'doc',
        'parameter': 'param',
        'argument': 'arg',
        'return': 'ret',
        'value': 'val',
        'variable': 'var',
        'number': 'num',
        'string': 'str',
        'boolean': 'bool',
        'integer': 'int',
        'array': 'arr',
        'object': 'obj',
        'property': 'prop',
        'method': 'meth',
        'class': 'cls',
        'interface': 'iface',
        'module': 'mod',
        'package': 'pkg',
        'library': 'lib',
        'framework': 'fwk',
        'environment': 'env',
        'development': 'dev',
        'production': 'prod',
        'testing': 'test',
        'authentication': 'auth',
        'authorization': 'authz',
        'configuration': 'config',
        'management': 'mgmt',
        'performance': 'perf',
        'optimization': 'opt',
        'implementation': 'impl',
        'integration': 'integ',
        'functionality': 'func',
        'capability': 'cap',
        'requirement': 'req',
        'specification': 'spec',
        'documentation': 'docs',
        'reference': 'ref',
        'example': 'ex',
        'instance': 'inst',
        'execution': 'exec',
        'operation': 'op',
        'processing': 'proc',
        'calculation': 'calc',
        'validation': 'valid',
        'verification': 'verif',
        'generation': 'gen',
        'transformation': 'transform',
        'conversion': 'conv',
        'translation': 'trans',
        'serialization': 'serial',
        'deserialization': 'deserial',
        'encryption': 'encrypt',
        'decryption': 'decrypt',
        'compression': 'compress',
        'decompression': 'decompress',
    }
    
    for original, replacement in replacements.items():
        compressed = compressed.replace(original, replacement)
    
    # Step 3: Remove vowels from some words (basic)
    # This is a very simple approach - in a real implementation we'd be more careful
    words = compressed.split()
    for i, word in enumerate(words):
        if len(word) > 3 and word.lower() not in ['the', 'and', 'with', 'that']:
            # Remove vowels except first letter
            if word[0].lower() in 'aeiou':
                new_word = word[0] + re.sub(r'[aeiou]', '', word[1:], flags=re.IGNORECASE)
            else:
                new_word = re.sub(r'[aeiou]', '', word, flags=re.IGNORECASE)
            
            # Only use if it actually saved space and kept at least half the word
            if len(new_word) < len(word) and len(new_word) >= len(word) // 2:
                words[i] = new_word
    
    compressed = ' '.join(words)
    
    logger.info(f"Compressed text from {len(text)} to {len(compressed)} chars")
    return compressed


def decompress_text(text: str) -> str:
    """
    Decompress text by expanding abbreviations.
    
    Since our compression is very basic, we can't fully recover the original text.
    This function attempts to expand some common abbreviations but won't perfectly restore
    the original text.
    
    Args:
        text: The compressed text to decompress
        
    Returns:
        The decompressed text (best effort)
    """
    if not text:
        return text
    
    # Expand common abbreviations
    expansions = {
        ' t ': ' the ',
        't ': 'the ',
        ' & ': ' and ',
        '& ': 'and ',
        ' w/ ': ' with ',
        'w/ ': 'with ',
        ' w/o ': ' without ',
        'w/o ': 'without ',
        'info': 'information',
        'app': 'application',
        'ex': 'example',
        'fn': 'function',
        'impl': 'implementation',
        'config': 'configuration',
        'db': 'database',
        'msg': 'message',
        'resp': 'response',
        'req': 'request',
        'err': 'error',
        'doc': 'document',
        'param': 'parameter',
        'arg': 'argument',
        'ret': 'return',
        'val': 'value',
        'var': 'variable',
        'num': 'number',
        'str': 'string',
        'bool': 'boolean',
        'int': 'integer',
        'arr': 'array',
        'obj': 'object',
        'prop': 'property',
        'meth': 'method',
        'cls': 'class',
        'iface': 'interface',
        'mod': 'module',
        'pkg': 'package',
        'lib': 'library',
        'fwk': 'framework',
        'env': 'environment',
        'dev': 'development',
        'prod': 'production',
        'test': 'testing',
        'auth': 'authentication',
        'authz': 'authorization',
        'config': 'configuration',
        'mgmt': 'management',
        'perf': 'performance',
        'opt': 'optimization',
        'impl': 'implementation',
        'integ': 'integration',
        'func': 'functionality',
        'cap': 'capability',
        'req': 'requirement',
        'spec': 'specification',
        'docs': 'documentation',
        'ref': 'reference',
        'ex': 'example',
        'inst': 'instance',
        'exec': 'execution',
        'op': 'operation',
        'proc': 'processing',
        'calc': 'calculation',
        'valid': 'validation',
        'verif': 'verification',
        'gen': 'generation',
        'transform': 'transformation',
        'conv': 'conversion',
        'trans': 'translation',
        'serial': 'serialization',
        'deserial': 'deserialization',
        'encrypt': 'encryption',
        'decrypt': 'decryption',
        'compress': 'compression',
        'decompress': 'decompression',
    }
    
    decompressed = text
    for abbrev, expanded in expansions.items():
        decompressed = decompressed.replace(abbrev, expanded)
    
    logger.info(f"Decompressed text from {len(text)} to {len(decompressed)} chars")
    return decompressed


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
    if not text or not ENABLE_SYNTHLANG:
        return text  # No compression if disabled or empty text
    
    try:
        # Compress the text using our implementation
        compressed = compress_text(text)
        
        # If compression returned empty string or failed, return original
        if not compressed:
            logger.warning("Compression returned empty result")
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
                
                logger.info(f"Compressed text from {len(text)} to {len(compressed)} chars, "
                           f"then to {len(final_compressed)} chars with gzip")
                return final_compressed
            except Exception as e:
                logger.error(f"Gzip compression failed: {e}")
                # Fall back to regular compression
                return compressed
        
        return compressed
    except Exception as e:
        logger.error(f"Unexpected error during compression: {e}")
        return text


def decompress_prompt(text: str) -> str:
    """
    Decompress a prompt, with automatic gzip decompression if needed.
    
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
        # Decompress the text using our implementation
        decompressed = decompress_text(text)
        
        # If decompression returned empty string or failed, return original
        if not decompressed:
            logger.warning("Decompression returned empty result")
            return text
        
        return decompressed
    except Exception as e:
        logger.error(f"Unexpected error during decompression: {e}")
        return text