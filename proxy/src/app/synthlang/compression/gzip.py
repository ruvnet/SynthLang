"""
Gzip compressor for SynthLang.

This module implements a compressor that uses gzip compression and base64 encoding
to achieve high compression ratios for large texts.
"""
import gzip
import base64
import logging
from typing import Dict, Any

from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class GzipCompressor(BaseCompressor):
    """
    Compressor that uses gzip compression and base64 encoding.
    
    This compressor is typically used as the last step in a compression pipeline
    for large texts, as it can achieve high compression ratios but produces
    binary data that needs to be encoded as text.
    """
    
    def __init__(self, compression_level: int = 9):
        """
        Initialize the gzip compressor.
        
        Args:
            compression_level: Gzip compression level (1-9, 9 being highest)
        """
        self.compression_level = compression_level
        self.prefix = "gz:"  # Prefix to identify gzip-compressed text
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text using gzip and base64 encoding.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            # Compress with gzip
            compressed_bytes = gzip.compress(text.encode('utf-8'), compresslevel=self.compression_level)
            
            # Encode with base64
            encoded = base64.b64encode(compressed_bytes).decode('ascii')
            
            # Add prefix to identify gzip-compressed text
            result = f"{self.prefix}{encoded}"
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "compressed_length": len(result),
                "compression_ratio": len(result) / len(text) if len(text) > 0 else 1.0,
                "compression_level": self.compression_level
            }
            
            logger.debug(f"Gzip compression: {len(text)} -> {len(result)} chars "
                        f"({metrics['compression_ratio']:.2f} ratio)")
            
            return self._create_success_result(result, metrics)
        except Exception as e:
            logger.error(f"Gzip compression error: {e}")
            return self._create_error_result(text, f"Gzip compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text that was compressed with gzip and base64 encoding.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the decompressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        # Check if this is gzip-compressed text
        if not text.startswith(self.prefix):
            # Not gzip-compressed, return as is
            return self._create_success_result(text)
        
        try:
            # Remove prefix
            encoded = text[len(self.prefix):]
            
            # Decode base64
            compressed_bytes = base64.b64decode(encoded)
            
            # Decompress gzip
            decompressed = gzip.decompress(compressed_bytes).decode('utf-8')
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0
            }
            
            logger.debug(f"Gzip decompression: {len(text)} -> {len(decompressed)} chars "
                        f"({metrics['expansion_ratio']:.2f} ratio)")
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            logger.error(f"Gzip decompression error: {e}")
            return self._create_error_result(text, f"Gzip decompression error: {e}")