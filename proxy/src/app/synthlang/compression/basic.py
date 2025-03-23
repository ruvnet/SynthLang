"""
Basic compressor for SynthLang.

This module implements a basic compressor that normalizes whitespace
and removes redundant characters.
"""
import re
import logging
from typing import Dict, Any

from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class BasicCompressor(BaseCompressor):
    """
    Basic compressor that normalizes whitespace and removes redundant characters.
    
    This is the simplest compressor and is typically used as the first step
    in a compression pipeline.
    """
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text by normalizing whitespace and removing redundant characters.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            # Normalize whitespace
            compressed = re.sub(r'\s+', ' ', text.strip())
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0
            }
            
            logger.debug(f"Basic compression: {len(text)} -> {len(compressed)} chars "
                        f"({metrics['compression_ratio']:.2f} ratio)")
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            logger.error(f"Basic compression error: {e}")
            return self._create_error_result(text, f"Basic compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text (no-op for BasicCompressor).
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the original text
        """
        # BasicCompressor doesn't actually modify the text in a way that needs decompression
        return self._create_success_result(text)