"""Advanced compression utilities for SynthLang Proxy."""
import base64
import gzip
import hashlib
import json
import re
import time
from typing import Dict, Optional, Tuple, Any, List

from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


def compress_with_gzip(text: str) -> str:
    """Compress text using gzip and encode as base64.
    
    Args:
        text: Text to compress
        
    Returns:
        Base64-encoded compressed text
    """
    compressed = gzip.compress(text.encode("utf-8"))
    return base64.b64encode(compressed).decode("utf-8")


def decompress_with_gzip(compressed_text: str) -> str:
    """Decompress base64-encoded gzipped text.
    
    Args:
        compressed_text: Base64-encoded compressed text
        
    Returns:
        Decompressed text
    """
    compressed = base64.b64decode(compressed_text)
    return gzip.decompress(compressed).decode("utf-8")


def _is_base64(text: str) -> bool:
    """Check if text is base64-encoded.
    
    Args:
        text: Text to check
        
    Returns:
        True if text is base64-encoded, False otherwise
    """
    try:
        # Check if the string contains only base64 characters
        if not re.match(r'^[A-Za-z0-9+/]+={0,2}$', text):
            return False
        
        # Try to decode
        base64.b64decode(text)
        return True
    except Exception:
        return False


def _synthlang_compress(text: str) -> str:
    """Compress text using SynthLang compression algorithm.
    
    This is a simplified implementation that uses common patterns in prompts.
    
    Args:
        text: Text to compress
        
    Returns:
        Compressed text
    """
    # Common replacements for compression
    replacements = [
        ("the ", "↹ "),
        ("and ", "• "),
        ("with ", "⊕ "),
        ("for ", "∀ "),
        ("to ", "→ "),
        ("in ", "∈ "),
        ("of ", "∋ "),
        ("is ", "≡ "),
        ("that ", "⊢ "),
        ("this ", "⊣ "),
        ("should ", "⊨ "),
        ("would ", "⊩ "),
        ("could ", "⊪ "),
        ("will ", "⊫ "),
        ("can ", "⊬ "),
        ("may ", "⊭ "),
        ("must ", "⊮ "),
        ("shall ", "⊯ "),
        ("not ", "¬ "),
        ("all ", "∀ "),
        ("some ", "∃ "),
        ("no ", "∄ "),
        ("every ", "∀ "),
        ("any ", "∃ "),
        ("each ", "∀ "),
        ("many ", "∃ "),
        ("few ", "∃ "),
        ("most ", "∀ "),
        ("several ", "∃ "),
        ("various ", "∃ "),
        ("different ", "≠ "),
        ("similar ", "≈ "),
        ("same ", "≡ "),
        ("equal ", "= "),
        ("equivalent ", "≡ "),
        ("approximately ", "≈ "),
        ("exactly ", "= "),
        ("precisely ", "= "),
        ("about ", "≈ "),
        ("around ", "≈ "),
        ("between ", "↔ "),
        ("among ", "∈ "),
        ("within ", "∈ "),
        ("without ", "∉ "),
        ("outside ", "∉ "),
        ("inside ", "∈ "),
        ("through ", "↝ "),
        ("throughout ", "↝ "),
        ("across ", "↝ "),
        ("along ", "↝ "),
        ("over ", "↑ "),
        ("under ", "↓ "),
        ("above ", "↑ "),
        ("below ", "↓ "),
        ("before ", "← "),
        ("after ", "→ "),
        ("during ", "⊂ "),
        ("while ", "⊂ "),
        ("when ", "⊂ "),
        ("where ", "⊂ "),
        ("why ", "? "),
        ("how ", "? "),
        ("what ", "? "),
        ("which ", "? "),
        ("who ", "? "),
        ("whom ", "? "),
        ("whose ", "? "),
        ("whether ", "? "),
        ("if ", "? "),
        ("unless ", "? "),
        ("until ", "? "),
        ("since ", "? "),
        ("because ", "∵ "),
        ("therefore ", "∴ "),
        ("thus ", "∴ "),
        ("hence ", "∴ "),
        ("so ", "∴ "),
        ("consequently ", "∴ "),
        ("accordingly ", "∴ "),
        ("as a result ", "∴ "),
        ("as such ", "∴ "),
        ("in conclusion ", "∴ "),
        ("in summary ", "∴ "),
        ("in short ", "∴ "),
        ("in brief ", "∴ "),
        ("in essence ", "∴ "),
        ("in other words ", "∴ "),
        ("that is ", "∴ "),
        ("namely ", "∴ "),
        ("specifically ", "∴ "),
        ("particularly ", "∴ "),
        ("especially ", "∴ "),
        ("notably ", "∴ "),
        ("chiefly ", "∴ "),
        ("mainly ", "∴ "),
        ("mostly ", "∴ "),
        ("largely ", "∴ "),
        ("generally ", "∴ "),
        ("usually ", "∴ "),
        ("typically ", "∴ "),
        ("often ", "∴ "),
        ("frequently ", "∴ "),
        ("occasionally ", "∴ "),
        ("rarely ", "∴ "),
        ("seldom ", "∴ "),
        ("never ", "∴ "),
        ("always ", "∴ "),
        ("sometimes ", "∴ "),
    ]
    
    # Apply replacements
    compressed = text
    for pattern, replacement in replacements:
        compressed = compressed.replace(pattern, replacement)
    
    return compressed


def _synthlang_decompress(text: str) -> str:
    """Decompress text using SynthLang decompression algorithm.
    
    Args:
        text: Compressed text
        
    Returns:
        Decompressed text
    """
    # Common replacements for decompression (reverse of compression)
    replacements = [
        ("↹ ", "the "),
        ("• ", "and "),
        ("⊕ ", "with "),
        ("∀ ", "for "),
        ("→ ", "to "),
        ("∈ ", "in "),
        ("∋ ", "of "),
        ("≡ ", "is "),
        ("⊢ ", "that "),
        ("⊣ ", "this "),
        ("⊨ ", "should "),
        ("⊩ ", "would "),
        ("⊪ ", "could "),
        ("⊫ ", "will "),
        ("⊬ ", "can "),
        ("⊭ ", "may "),
        ("⊮ ", "must "),
        ("⊯ ", "shall "),
        ("¬ ", "not "),
        ("∀ ", "all "),
        ("∃ ", "some "),
        ("∄ ", "no "),
        ("≠ ", "different "),
        ("≈ ", "similar "),
        ("= ", "equal "),
        ("↔ ", "between "),
        ("∉ ", "without "),
        ("↝ ", "through "),
        ("↑ ", "over "),
        ("↓ ", "under "),
        ("← ", "before "),
        ("⊂ ", "during "),
        ("? ", "what "),
        ("∵ ", "because "),
        ("∴ ", "therefore "),
    ]
    
    # Apply replacements
    decompressed = text
    for pattern, replacement in replacements:
        decompressed = decompressed.replace(pattern, replacement)
    
    return decompressed


def compress_prompt(prompt: str, use_gzip: bool = False) -> str:
    """Compress prompt using SynthLang compression and optionally gzip.
    
    Args:
        prompt: Prompt to compress
        use_gzip: Whether to use gzip compression
        
    Returns:
        Compressed prompt
    """
    # First apply SynthLang compression
    compressed = _synthlang_compress(prompt)
    
    # Optionally apply gzip compression
    if use_gzip:
        compressed = compress_with_gzip(compressed)
    
    logger.debug(f"Compressed prompt from {len(prompt)} to {len(compressed)} chars")
    return compressed


def decompress_prompt(compressed: str) -> str:
    """Decompress prompt, handling both SynthLang and gzip compression.
    
    Args:
        compressed: Compressed prompt
        
    Returns:
        Decompressed prompt
    """
    # Check if it's gzip compressed (base64 encoded)
    try:
        if _is_base64(compressed):
            decompressed = decompress_with_gzip(compressed)
        else:
            decompressed = compressed
        
        # Apply SynthLang decompression
        decompressed = _synthlang_decompress(decompressed)
        return decompressed
    except Exception as e:
        logger.warning(f"Error decompressing prompt: {str(e)}")
        return compressed  # Return as-is if decompression fails


def get_compression_stats(original: str, compressed: str) -> Dict[str, Any]:
    """Get compression statistics.
    
    Args:
        original: Original text
        compressed: Compressed text
        
    Returns:
        Dictionary with compression statistics
    """
    original_len = len(original)
    compressed_len = len(compressed)
    ratio = compressed_len / original_len if original_len > 0 else 1.0
    savings = 1.0 - ratio
    
    return {
        "original_length": original_len,
        "compressed_length": compressed_len,
        "compression_ratio": ratio,
        "space_savings": savings,
        "space_savings_percent": savings * 100,
    }