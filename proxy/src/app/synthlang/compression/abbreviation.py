"""
Abbreviation compressor for SynthLang.

This module implements a compressor that replaces common words with abbreviations.
"""
import re
import logging
from typing import Dict, Any, List, Tuple, Pattern

from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class AbbreviationCompressor(BaseCompressor):
    """
    Compressor that replaces common words with abbreviations.
    
    This compressor maintains a dictionary of common words and their abbreviations,
    and replaces occurrences of these words in the text.
    """
    
    def __init__(self):
        """Initialize the abbreviation compressor with common abbreviations."""
        # Common words and their abbreviations
        self.abbreviations = {
            "the": "t",
            "and": "&",
            "with": "w/",
            "without": "w/o",
            "information": "info",
            "application": "app",
            "example": "ex",
            "function": "fn",
            "implementation": "impl",
            "configuration": "config",
            "database": "db",
            "message": "msg",
            "response": "resp",
            "request": "req",
            "error": "err",
            "document": "doc",
            "parameter": "param",
            "argument": "arg",
            "return": "ret",
            "value": "val",
            "variable": "var",
            "number": "num",
            "string": "str",
            "boolean": "bool",
            "integer": "int",
            "array": "arr",
            "object": "obj",
            "property": "prop",
            "method": "meth",
            "class": "cls",
            "interface": "iface",
            "module": "mod",
            "package": "pkg",
            "library": "lib",
            "framework": "fwk",
            "environment": "env",
            "development": "dev",
            "production": "prod",
            "testing": "test",
            "authentication": "auth",
            "authorization": "authz",
            "management": "mgmt",
            "performance": "perf",
            "optimization": "opt",
            "integration": "integ",
            "functionality": "func",
            "capability": "cap",
            "requirement": "req",
            "specification": "spec",
            "documentation": "docs",
            "reference": "ref",
            "instance": "inst",
            "execution": "exec",
            "operation": "op",
            "processing": "proc",
            "calculation": "calc",
            "validation": "valid",
            "verification": "verif",
            "generation": "gen",
            "transformation": "transform",
            "conversion": "conv",
            "translation": "trans",
            "serialization": "serial",
            "deserialization": "deserial",
            "encryption": "encrypt",
            "decryption": "decrypt",
            "compression": "compress",
            "decompression": "decompress",
        }
        
        # Build reverse mapping for decompression
        self.reverse_abbreviations = {v: k for k, v in self.abbreviations.items()}
        
        # Compile regex patterns for better performance
        self.patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> List[Tuple[Pattern, str]]:
        """
        Compile regex patterns for abbreviations.
        
        Returns:
            List of tuples (pattern, replacement)
        """
        patterns = []
        for word, abbrev in self.abbreviations.items():
            # Use word boundaries to avoid partial replacements
            pattern = re.compile(r'\b' + word + r'\b', re.IGNORECASE)
            patterns.append((pattern, abbrev))
        return patterns
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text by replacing common words with abbreviations.
        
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
            
            # Apply each abbreviation
            for pattern, replacement in self.patterns:
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
            
            logger.debug(f"Abbreviation compression: {len(text)} -> {len(compressed)} chars "
                        f"({metrics['compression_ratio']:.2f} ratio, {replacements} replacements)")
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            logger.error(f"Abbreviation compression error: {e}")
            return self._create_error_result(text, f"Abbreviation compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text by expanding abbreviations.
        
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
            
            # Apply each reverse abbreviation
            for abbrev, word in self.reverse_abbreviations.items():
                # Use word boundaries to avoid partial replacements
                pattern = re.compile(r'\b' + re.escape(abbrev) + r'\b')
                # Count replacements for metrics
                new_text, count = pattern.subn(word, decompressed)
                replacements += count
                decompressed = new_text
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0,
                "replacements": replacements
            }
            
            logger.debug(f"Abbreviation decompression: {len(text)} -> {len(decompressed)} chars "
                        f"({metrics['expansion_ratio']:.2f} ratio, {replacements} replacements)")
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            logger.error(f"Abbreviation decompression error: {e}")
            return self._create_error_result(text, f"Abbreviation decompression error: {e}")