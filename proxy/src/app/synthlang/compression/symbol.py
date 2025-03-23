"""
Symbol compressor for SynthLang.

This module implements a compressor that uses SynthLang symbols to represent
common patterns in a more concise way.
"""
import re
import logging
from typing import Dict, Any, List, Tuple, Pattern

from src.app.synthlang.core import SynthLangSymbols
from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class SymbolCompressor(BaseCompressor):
    """
    Compressor that uses SynthLang symbols to represent common patterns.
    
    This compressor replaces common patterns with SynthLang symbols to
    reduce token usage when communicating with LLMs.
    """
    
    def __init__(self):
        """Initialize the symbol compressor with SynthLang symbols."""
        # Get symbols from SynthLangSymbols
        self.input_symbol = SynthLangSymbols.INPUT
        self.process_symbol = SynthLangSymbols.PROCESS
        self.output_symbol = SynthLangSymbols.OUTPUT
        self.join_symbol = SynthLangSymbols.JOIN
        self.transform_symbol = SynthLangSymbols.TRANSFORM
        
        # Common patterns to replace with symbols
        self.patterns = [
            # Input patterns
            (r'\binput\b', self.input_symbol),
            (r'\bdata\b', self.input_symbol),
            (r'\bsource\b', self.input_symbol),
            (r'\bfeed\b', self.input_symbol),
            (r'\bstream\b', self.input_symbol),
            
            # Process patterns
            (r'\bprocess\b', self.process_symbol),
            (r'\banalyze\b', self.process_symbol),
            (r'\btransform\b', self.process_symbol),
            (r'\bcompute\b', self.process_symbol),
            (r'\bcalculate\b', self.process_symbol),
            
            # Output patterns
            (r'\boutput\b', self.output_symbol),
            (r'\bresult\b', self.output_symbol),
            (r'\bgenerate\b', self.output_symbol),
            (r'\bproduce\b', self.output_symbol),
            (r'\breturn\b', self.output_symbol),
            
            # Join patterns
            (r'\band\b', self.join_symbol),
            (r'\bwith\b', self.join_symbol),
            (r'\bplus\b', self.join_symbol),
            (r'\bcombined\b', self.join_symbol),
            
            # Transform patterns
            (r'\bto\b', self.transform_symbol),
            (r'\binto\b', self.transform_symbol),
            (r'\bbecome\b', self.transform_symbol),
            (r'\bconvert\b', self.transform_symbol),
        ]
        
        # Compile regex patterns for better performance
        self.compiled_patterns = [(re.compile(pattern), replacement) 
                                 for pattern, replacement in self.patterns]
        
        # Build reverse mappings for decompression
        self.reverse_patterns = []
        for pattern, symbol in self.patterns:
            # Extract the word from the pattern (remove \b markers)
            word = pattern.replace(r'\b', '')
            self.reverse_patterns.append((re.compile(re.escape(symbol)), word))
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text by replacing common patterns with SynthLang symbols.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            compressed = text
            replacements = 0
            
            # Apply each pattern
            for pattern, replacement in self.compiled_patterns:
                # Count replacements for metrics
                new_text, count = pattern.subn(replacement, compressed)
                replacements += count
                compressed = new_text
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "replacements": replacements
            }
            
            logger.debug(f"Symbol compression: {len(text)} -> {len(compressed)} chars "
                        f"({metrics['compression_ratio']:.2f} ratio, {replacements} replacements)")
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            logger.error(f"Symbol compression error: {e}")
            return self._create_error_result(text, f"Symbol compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text by expanding SynthLang symbols to words.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the decompressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            decompressed = text
            replacements = 0
            
            # Apply each reverse pattern
            for pattern, replacement in self.reverse_patterns:
                # Count replacements for metrics
                new_text, count = pattern.subn(replacement, decompressed)
                replacements += count
                decompressed = new_text
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0,
                "replacements": replacements
            }
            
            logger.debug(f"Symbol decompression: {len(text)} -> {len(decompressed)} chars "
                        f"({metrics['expansion_ratio']:.2f} ratio, {replacements} replacements)")
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            logger.error(f"Symbol decompression error: {e}")
            return self._create_error_result(text, f"Symbol decompression error: {e}")