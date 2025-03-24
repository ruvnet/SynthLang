"""
Compression strategies for SynthLang.

This module provides various compression strategies that can be used
individually or combined in a pipeline.
"""
import re
import gzip
import base64
import logging
from typing import Dict, Any, List, Tuple, Optional

from src.app.synthlang.core import SynthLangSymbols, FormatRules
from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)

# SynthLang symbols for compression
INPUT_SYMBOL = SynthLangSymbols.INPUT
PROCESS_SYMBOL = SynthLangSymbols.PROCESS
OUTPUT_SYMBOL = SynthLangSymbols.OUTPUT
JOIN_SYMBOL = SynthLangSymbols.JOIN
TRANSFORM_SYMBOL = SynthLangSymbols.TRANSFORM


class BasicCompressor(BaseCompressor):
    """
    Basic compressor that removes redundant whitespace.
    
    This is a simple compressor that just removes extra whitespace
    and normalizes the text.
    """
    
    def compress(self, text: str) -> CompressionResult:
        """Compress by removing redundant whitespace."""
        if not text:
            return self._create_success_result(text)
        
        try:
            # Remove redundant whitespace
            compressed = re.sub(r'\s+', ' ', text.strip())
            
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0
            }
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Basic compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """No real decompression for basic whitespace removal."""
        return self._create_success_result(text, {"note": "Basic compression is not reversible"})


class AbbreviationCompressor(BaseCompressor):
    """
    Compressor that replaces common words with abbreviations.
    
    This compressor maintains a dictionary of common words and their
    abbreviations, and replaces them during compression.
    """
    
    def __init__(self):
        """Initialize with default abbreviations."""
        self.abbreviations = {
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
            'management': 'mgmt',
            'performance': 'perf',
            'optimization': 'opt',
            'integration': 'integ',
            'functionality': 'func',
            'capability': 'cap',
            'requirement': 'req',
            'specification': 'spec',
            'documentation': 'docs',
            'reference': 'ref',
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
        
        # Create reverse mapping for decompression
        self.expansions = {v: k for k, v in self.abbreviations.items()}
    
    def compress(self, text: str) -> CompressionResult:
        """Compress by replacing common words with abbreviations."""
        if not text:
            return self._create_success_result(text)
        
        try:
            compressed = text
            for original, replacement in self.abbreviations.items():
                compressed = compressed.replace(original, replacement)
            
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "replacements_applied": sum(text.count(orig) for orig in self.abbreviations)
            }
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Abbreviation compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """Decompress by expanding abbreviations."""
        if not text:
            return self._create_success_result(text)
        
        try:
            decompressed = text
            for abbrev, expanded in self.expansions.items():
                decompressed = decompressed.replace(abbrev, expanded)
            
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0
            }
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Abbreviation decompression error: {e}")


class VowelRemovalCompressor(BaseCompressor):
    """
    Compressor that removes vowels from words.
    
    This compressor removes vowels from words to reduce their length,
    while preserving the first vowel if it's the first letter of the word.
    """
    
    def __init__(self, min_word_length: int = 4, preserve_first_vowel: bool = True):
        """
        Initialize the vowel removal compressor.
        
        Args:
            min_word_length: Minimum word length to apply vowel removal
            preserve_first_vowel: Whether to preserve the first vowel if it's the first letter
        """
        self.min_word_length = min_word_length
        self.preserve_first_vowel = preserve_first_vowel
        self.excluded_words = ['the', 'and', 'with', 'that', 'this', 'for', 'you']
    
    def compress(self, text: str) -> CompressionResult:
        """Compress by removing vowels from words."""
        if not text:
            return self._create_success_result(text)
        
        try:
            words = text.split()
            vowels_removed = 0
            
            for i, word in enumerate(words):
                if len(word) >= self.min_word_length and word.lower() not in self.excluded_words:
                    # Remove vowels with special handling for first letter
                    if self.preserve_first_vowel and word[0].lower() in 'aeiou':
                        new_word = word[0] + re.sub(r'[aeiou]', '', word[1:], flags=re.IGNORECASE)
                    else:
                        new_word = re.sub(r'[aeiou]', '', word, flags=re.IGNORECASE)
                    
                    # Only use if it actually saved space and kept at least half the word
                    if len(new_word) < len(word) and len(new_word) >= len(word) // 2:
                        vowels_removed += len(word) - len(new_word)
                        words[i] = new_word
            
            compressed = ' '.join(words)
            
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "vowels_removed": vowels_removed
            }
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Vowel removal compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Vowel removal is not fully reversible.
        
        This method attempts to restore some common patterns but cannot
        fully restore the original text.
        """
        # Vowel removal is not fully reversible, so we just return the text
        return self._create_success_result(text, {"note": "Vowel removal is not reversible"})


class SymbolCompressor(BaseCompressor):
    """
    Compressor that uses SynthLang symbols for compression.
    
    This compressor uses special symbols to represent common patterns
    and structures in the text, making it more compact.
    """
    
    def __init__(self):
        """Initialize with SynthLang symbols."""
        self.patterns = [
            # Input-process-output patterns
            (r'input\s+(.+?)\s+and\s+process\s+(.+?)\s+to\s+output\s+(.+)', 
             f"{INPUT_SYMBOL} \\1 {PROCESS_SYMBOL} \\2 {TRANSFORM_SYMBOL} \\3"),
            
            # List items with bullets
            (r'(\s*[-•*]\s+.+?\n)+', self._compress_list),
            
            # Key-value pairs
            (r'(\w+):\s+(.+?)(?=\n|$)', f"\\1{JOIN_SYMBOL}\\2"),
            
            # Function calls
            (r'(\w+)\((.+?)\)', f"\\1{PROCESS_SYMBOL}\\2"),
            
            # Paths and URLs
            (r'(https?://[^\s]+)', f"{INPUT_SYMBOL}\\1"),
            (r'(/[\w/.-]+)', f"{JOIN_SYMBOL}\\1"),
            
            # Common programming constructs
            (r'if\s+(.+?)\s+then\s+(.+)', f"?\\1{TRANSFORM_SYMBOL}\\2"),
            (r'for\s+each\s+(.+?)\s+in\s+(.+)', f"@\\1{JOIN_SYMBOL}\\2"),
        ]
    
    def _compress_list(self, match) -> str:
        """Compress a list of bullet points."""
        items = re.findall(r'[-•*]\s+(.+?)(?=\n|$)', match.group(0))
        return f"{INPUT_SYMBOL}[" + f"{JOIN_SYMBOL}".join(items) + "]"
    
    def compress(self, text: str) -> CompressionResult:
        """Compress using SynthLang symbols."""
        if not text:
            return self._create_success_result(text)
        
        try:
            compressed = text
            patterns_applied = 0
            
            for pattern, replacement in self.patterns:
                if callable(replacement):
                    # For custom replacement functions
                    result = re.sub(pattern, replacement, compressed)
                    if result != compressed:
                        patterns_applied += 1
                        compressed = result
                else:
                    # For simple string replacements
                    new_text = re.sub(pattern, replacement, compressed)
                    if new_text != compressed:
                        patterns_applied += 1
                        compressed = new_text
            
            # Break into lines of maximum length for better readability
            if len(compressed) > FormatRules.MAX_LINE_LENGTH:
                lines = []
                current_line = ""
                for word in compressed.split():
                    if len(current_line) + len(word) + 1 <= FormatRules.MAX_LINE_LENGTH:
                        current_line += (" " + word if current_line else word)
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                compressed = "\n".join(lines)
            
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "patterns_applied": patterns_applied
            }
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Symbol compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """Decompress SynthLang symbols."""
        if not text:
            return self._create_success_result(text)
        
        try:
            decompressed = text
            
            # Reverse the patterns
            reverse_patterns = [
                # Input-process-output patterns
                (f"{INPUT_SYMBOL} (.+?) {PROCESS_SYMBOL} (.+?) {TRANSFORM_SYMBOL} (.+)", 
                 "input \\1 and process \\2 to output \\3"),
                
                # List items
                (f"{INPUT_SYMBOL}\\[(.+?)\\]", self._decompress_list),
                
                # Key-value pairs
                (f"(\\w+){JOIN_SYMBOL}(.+?)(?=\\n|$)", "\\1: \\2"),
                
                # Function calls
                (f"(\\w+){PROCESS_SYMBOL}(.+?)", "\\1(\\2)"),
                
                # Paths and URLs
                (f"{INPUT_SYMBOL}(https?://[^\\s]+)", "\\1"),
                (f"{JOIN_SYMBOL}(/[\\w/.-]+)", "\\1"),
                
                # Common programming constructs
                (f"\\?(.+?){TRANSFORM_SYMBOL}(.+)", "if \\1 then \\2"),
                (f"@(.+?){JOIN_SYMBOL}(.+)", "for each \\1 in \\2"),
            ]
            
            for pattern, replacement in reverse_patterns:
                if callable(replacement):
                    # For custom replacement functions
                    decompressed = re.sub(pattern, replacement, decompressed)
                else:
                    # For simple string replacements
                    decompressed = re.sub(pattern, replacement, decompressed)
            
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0
            }
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Symbol decompression error: {e}")
    
    def _decompress_list(self, match) -> str:
        """Decompress a list of items."""
        items = match.group(1).split(JOIN_SYMBOL)
        return "\n".join([f"- {item}" for item in items])


class GzipCompressor(BaseCompressor):
    """
    Compressor that uses gzip for binary compression.
    
    This compressor applies gzip compression to the text and encodes
    the result as base64 for safe transmission.
    """
    
    def __init__(self, prefix: str = "gz:"):
        """
        Initialize the gzip compressor.
        
        Args:
            prefix: Prefix to identify gzipped content
        """
        self.prefix = prefix
    
    def compress(self, text: str) -> CompressionResult:
        """Compress using gzip and base64 encoding."""
        if not text:
            return self._create_success_result(text)
        
        try:
            # Convert to bytes, compress with gzip, then encode as base64 string
            compressed_bytes = text.encode('utf-8')
            gzipped = gzip.compress(compressed_bytes)
            b64_compressed = base64.b64encode(gzipped).decode('ascii')
            
            # Add the prefix to indicate this is gzipped
            final_compressed = f"{self.prefix}{b64_compressed}"
            
            metrics = {
                "original_length": len(text),
                "compressed_length": len(final_compressed),
                "compression_ratio": len(final_compressed) / len(text) if len(text) > 0 else 1.0,
                "binary_size": len(gzipped)
            }
            
            return self._create_success_result(final_compressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Gzip compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """Decompress gzipped content."""
        if not text or not text.startswith(self.prefix):
            return self._create_success_result(text)
        
        try:
            # Extract the base64 encoded gzipped data
            b64_data = text[len(self.prefix):]
            gzipped = base64.b64decode(b64_data)
            decompressed_bytes = gzip.decompress(gzipped)
            decompressed = decompressed_bytes.decode('utf-8')
            
            metrics = {
                "original_length": len(text),
                "decompressed_length": len(decompressed),
                "expansion_ratio": len(decompressed) / len(text) if len(text) > 0 else 1.0,
                "binary_size": len(gzipped)
            }
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            return self._create_error_result(text, f"Gzip decompression error: {e}")