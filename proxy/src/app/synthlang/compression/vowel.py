"""
Vowel removal compressor for SynthLang.

This module implements a compressor that removes vowels from words.
"""
import re
import logging
from typing import Dict, Any, List, Set

from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class VowelRemovalCompressor(BaseCompressor):
    """
    Compressor that removes vowels from words.
    
    This compressor removes vowels from words longer than a specified length,
    optionally preserving the first vowel to maintain readability.
    """
    
    def __init__(self, min_word_length: int = 4, preserve_first_vowel: bool = True):
        """
        Initialize the vowel removal compressor.
        
        Args:
            min_word_length: Minimum word length to apply vowel removal
            preserve_first_vowel: Whether to preserve the first vowel in each word
        """
        self.min_word_length = min_word_length
        self.preserve_first_vowel = preserve_first_vowel
        
        # Set of vowels
        self.vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        
        # Words to exclude from vowel removal (common short words, etc.)
        self.excluded_words = {
            'the', 'and', 'but', 'for', 'nor', 'yet', 'so', 'as', 'at', 'by',
            'if', 'in', 'of', 'off', 'on', 'or', 'to', 'up', 'via', 'is', 'am',
            'are', 'was', 'were', 'be', 'been', 'being', 'do', 'does', 'did',
            'done', 'doing', 'can', 'could', 'may', 'might', 'must', 'shall',
            'should', 'will', 'would', 'has', 'have', 'had', 'having', 'get',
            'gets', 'got', 'gotten', 'getting', 'go', 'goes', 'went', 'gone',
            'going', 'me', 'my', 'mine', 'you', 'your', 'yours', 'he', 'him',
            'his', 'she', 'her', 'hers', 'it', 'its', 'we', 'us', 'our', 'ours',
            'they', 'them', 'their', 'theirs'
        }
    
    def _remove_vowels(self, word: str) -> str:
        """
        Remove vowels from a word.
        
        Args:
            word: The word to remove vowels from
            
        Returns:
            The word with vowels removed
        """
        # Skip short words and excluded words
        if len(word) < self.min_word_length or word.lower() in self.excluded_words:
            return word
        
        # If preserving first vowel, find its position
        first_vowel_pos = -1
        if self.preserve_first_vowel:
            for i, char in enumerate(word):
                if char.lower() in self.vowels:
                    first_vowel_pos = i
                    break
        
        # Remove vowels (except first if preserving)
        result = []
        for i, char in enumerate(word):
            if char.lower() not in self.vowels or i == first_vowel_pos:
                result.append(char)
        
        return ''.join(result)
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text by removing vowels from words.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            # Split text into words and apply vowel removal
            words = re.findall(r'\b\w+\b|\W+', text)
            compressed_words = [self._remove_vowels(word) for word in words]
            compressed = ''.join(compressed_words)
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "min_word_length": self.min_word_length,
                "preserve_first_vowel": self.preserve_first_vowel
            }
            
            logger.debug(f"Vowel removal compression: {len(text)} -> {len(compressed)} chars "
                        f"({metrics['compression_ratio']:.2f} ratio)")
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            logger.error(f"Vowel removal compression error: {e}")
            return self._create_error_result(text, f"Vowel removal compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text (no-op for VowelRemovalCompressor).
        
        Vowel removal is not reversible, so this method returns the input text.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the original text
        """
        # Vowel removal is not reversible, so just return the input
        return self._create_success_result(text, {
            "note": "Vowel removal is not reversible, returning input text"
        })