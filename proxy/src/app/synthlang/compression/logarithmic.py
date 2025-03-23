"""
Logarithmic symbolic compressor for SynthLang.

This module implements an advanced compressor that uses logarithmic
symbolic compression techniques from the SynthLang CLI.
"""
import re
import logging
import math
from typing import Dict, Any, List, Tuple, Pattern, Set

from src.app.synthlang.core import SynthLangSymbols, FormatRules
from .base import BaseCompressor, CompressionResult

# Configure logging
logger = logging.getLogger(__name__)


class LogarithmicSymbolicCompressor(BaseCompressor):
    """
    Advanced compressor that uses logarithmic symbolic compression.
    
    This compressor applies more aggressive compression techniques based on
    the SynthLang CLI's symbolic representation, including:
    - Breaking text into logical chunks
    - Replacing common phrases with symbols
    - Applying logarithmic compression to repetitive patterns
    - Formatting text in a more compact representation
    """
    
    def __init__(self, max_line_length: int = 30, min_chunk_size: int = 50):
        """
        Initialize the logarithmic symbolic compressor.
        
        Args:
            max_line_length: Maximum line length for formatted output
            min_chunk_size: Minimum chunk size for breaking text
        """
        self.max_line_length = max_line_length
        self.min_chunk_size = min_chunk_size
        
        # Get symbols from SynthLangSymbols
        self.symbols = SynthLangSymbols.get_all_symbols()
        
        # Common phrases to replace with symbols
        self.phrase_replacements = [
            # Input-related phrases
            (r'\binput data\b', f"{self.symbols['INPUT']}data"),
            (r'\bdata input\b', f"{self.symbols['INPUT']}data"),
            (r'\buser input\b', f"{self.symbols['INPUT']}user"),
            (r'\bsystem input\b', f"{self.symbols['INPUT']}system"),
            (r'\bfile input\b', f"{self.symbols['INPUT']}file"),
            (r'\bdatabase\b', "db"),
            
            # Process-related phrases
            (r'\bprocess data\b', f"{self.symbols['PROCESS']}data"),
            (r'\banalyze data\b', f"{self.symbols['PROCESS']}data"),
            (r'\bcompute results\b', f"{self.symbols['PROCESS']}results"),
            (r'\bcalculate values\b', f"{self.symbols['PROCESS']}values"),
            (r'\btransform input\b', f"{self.symbols['PROCESS']}input"),
            
            # Output-related phrases
            (r'\boutput results\b', f"{self.symbols['OUTPUT']}results"),
            (r'\bgenerate output\b', f"{self.symbols['OUTPUT']}"),
            (r'\breturn results\b', f"{self.symbols['OUTPUT']}results"),
            (r'\bdisplay output\b', f"{self.symbols['OUTPUT']}display"),
            (r'\bwrite to file\b', f"{self.symbols['OUTPUT']}file"),
            
            # Common programming terms
            (r'\bfunction\b', "fn"),
            (r'\bvariable\b', "var"),
            (r'\bparameter\b', "param"),
            (r'\bargument\b', "arg"),
            (r'\bobject\b', "obj"),
            (r'\barray\b', "arr"),
            (r'\bstring\b', "str"),
            (r'\bnumber\b', "num"),
            (r'\bboolean\b', "bool"),
            (r'\binteger\b', "int"),
            (r'\bfloat\b', "float"),
            (r'\bdouble\b', "dbl"),
            (r'\bcharacter\b', "char"),
            (r'\bclass\b', "cls"),
            (r'\bmethod\b', "meth"),
            (r'\bproperty\b', "prop"),
            (r'\battribute\b', "attr"),
            (r'\binstance\b', "inst"),
            (r'\bimplementation\b', "impl"),
            
            # Common domain-specific terms
            (r'\bnatural language processing\b', "NLP"),
            (r'\bmachine learning\b', "ML"),
            (r'\bartificial intelligence\b', "AI"),
            (r'\bdeep learning\b', "DL"),
            (r'\bneural network\b', "NN"),
            (r'\bdatabase management system\b', "DBMS"),
            (r'\bapplication programming interface\b', "API"),
            (r'\bgraphical user interface\b', "GUI"),
            (r'\bcommand line interface\b', "CLI"),
            (r'\boperating system\b', "OS"),
            
            # Logical operators and relationships
            (r'\band\b', self.symbols['JOIN']),
            (r'\bor\b', self.symbols['OR']),
            (r'\bnot\b', self.symbols['NOT']),
            (r'\bif\b', self.symbols['CONDITION']),
            (r'\belse\b', self.symbols['OR']),
            (r'\bfor\b', self.symbols['LOOP']),
            (r'\bwhile\b', self.symbols['LOOP']),
            (r'\bforeach\b', self.symbols['LOOP']),
            (r'\biterate\b', self.symbols['ITERATION']),
            (r'\brepeat\b', self.symbols['ITERATION']),
            
            # Mathematical operations
            (r'\bplus\b', self.symbols['PLUS']),
            (r'\bminus\b', self.symbols['MINUS']),
            (r'\btimes\b', self.symbols['MULTIPLY']),
            (r'\bdivided by\b', self.symbols['DIVIDE']),
            (r'\bgreater than\b', self.symbols['GREATER']),
            (r'\bless than\b', self.symbols['LESS']),
            (r'\bequal to\b', self.symbols['EQUAL']),
            (r'\bpower of\b', self.symbols['POWER']),
            
            # Transformations
            (r'\bto\b', self.symbols['TRANSFORM']),
            (r'\binto\b', self.symbols['TRANSFORM']),
            (r'\bfrom\b', self.symbols['TRANSFORM']),
            (r'\bconvert\b', self.symbols['TRANSFORM']),
            (r'\btransform\b', self.symbols['TRANSFORM']),
            
            # Extended symbols from documentation
            (r'\bsubset of\b', self.symbols['SUBSET']),
            (r'\bincluded in\b', self.symbols['SUBSET']),
            (r'\bpart of\b', self.symbols['SUBSET']),
            (r'\bcontained in\b', self.symbols['SUBSET']),
            
            (r'\bflow\b', self.symbols['FLOW']),
            (r'\bsequence\b', self.symbols['FLOW']),
            (r'\bsteps\b', self.symbols['FLOW']),
            (r'\bpipeline\b', self.symbols['FLOW']),
            
            (r'\bis defined as\b', self.symbols['EQUIVALENCE']),
            (r'\bis equivalent to\b', self.symbols['EQUIVALENCE']),
            (r'\bmeans\b', self.symbols['EQUIVALENCE']),
            (r'\bis the same as\b', self.symbols['EQUIVALENCE']),
            
            (r'\btherefore\b', self.symbols['THEREFORE']),
            (r'\bhence\b', self.symbols['THEREFORE']),
            (r'\bconsequently\b', self.symbols['THEREFORE']),
            (r'\bas a result\b', self.symbols['THEREFORE']),
            
            (r'\bfor all\b', self.symbols['FORALL']),
            (r'\ball\b', self.symbols['FORALL']),
            (r'\bevery\b', self.symbols['FORALL']),
            (r'\beach\b', self.symbols['FORALL']),
            
            (r'\bthere exists\b', self.symbols['EXISTS']),
            (r'\bsome\b', self.symbols['EXISTS']),
            (r'\bat least one\b', self.symbols['EXISTS']),
            (r'\bexists\b', self.symbols['EXISTS']),
        ]
        
        # Compile regex patterns for better performance
        self.compiled_patterns = [(re.compile(pattern), replacement) 
                                 for pattern, replacement in self.phrase_replacements]
        
        # Build reverse mappings for decompression
        self.reverse_patterns = []
        for pattern, replacement in self.phrase_replacements:
            # Extract the word from the pattern (remove \b markers)
            word = pattern.replace(r'\b', '')
            # Skip patterns with special regex characters
            if not any(c in word for c in '.^$*+?{}[]\\|('):
                self.reverse_patterns.append((re.compile(re.escape(replacement)), word))
    
    def _apply_phrase_replacements(self, text: str) -> Tuple[str, int]:
        """
        Apply phrase replacements to text.
        
        Args:
            text: The text to process
            
        Returns:
            Tuple of (processed text, number of replacements)
        """
        processed = text
        replacements = 0
        
        # Apply each pattern
        for pattern, replacement in self.compiled_patterns:
            # Count replacements
            new_text, count = pattern.subn(replacement, processed)
            replacements += count
            processed = new_text
        
        return processed, replacements
    
    def _break_into_chunks(self, text: str) -> List[str]:
        """
        Break text into logical chunks.
        
        Args:
            text: The text to break into chunks
            
        Returns:
            List of text chunks
        """
        # Split by sentences or paragraphs
        chunks = []
        
        # First try to split by paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        
        for paragraph in paragraphs:
            # If paragraph is short enough, add it as is
            if len(paragraph) <= self.min_chunk_size:
                chunks.append(paragraph)
                continue
                
            # Otherwise, split by sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            current_chunk = ""
            for sentence in sentences:
                # If adding this sentence would make the chunk too long, start a new chunk
                if len(current_chunk) + len(sentence) > self.min_chunk_size and current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = sentence
                else:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
            
            # Add the last chunk if it's not empty
            if current_chunk:
                chunks.append(current_chunk)
        
        return chunks
    
    def _format_text(self, text: str) -> str:
        """
        Format text with line breaks for better readability.
        
        Args:
            text: The text to format
            
        Returns:
            Formatted text with line breaks
        """
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # If adding this word would make the line too long, start a new line
            if len(current_line) + len(word) + 1 > self.max_line_length and current_line:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
        
        # Add the last line if it's not empty
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
    
    def _calculate_logarithmic_factor(self, original: str, compressed: str) -> float:
        """
        Calculate the logarithmic compression factor.
        
        Args:
            original: The original text
            compressed: The compressed text
            
        Returns:
            Logarithmic compression factor (0-1)
        """
        if not original or not compressed:
            return 0.0
            
        # Calculate the compression ratio
        ratio = len(compressed) / len(original)
        
        # Apply logarithmic scaling to get a factor between 0 and 1
        # A lower ratio (better compression) results in a higher factor
        if ratio >= 1.0:
            return 0.0
        
        # Use logarithmic scaling to emphasize small improvements
        factor = -math.log(ratio) / 5.0  # Normalize to a reasonable range
        
        # Clamp to [0, 1]
        return min(max(factor, 0.0), 1.0)
    
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text using logarithmic symbolic compression.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            # Break text into chunks
            chunks = self._break_into_chunks(text)
            
            # Process each chunk
            processed_chunks = []
            total_replacements = 0
            
            for chunk in chunks:
                # Apply phrase replacements
                processed, replacements = self._apply_phrase_replacements(chunk)
                total_replacements += replacements
                
                # Format the processed chunk
                formatted = self._format_text(processed)
                
                processed_chunks.append(formatted)
            
            # Join the processed chunks
            compressed = "\n".join(processed_chunks)
            
            # Calculate the logarithmic factor
            logarithmic_factor = self._calculate_logarithmic_factor(text, compressed)
            
            # Calculate metrics
            metrics = {
                "original_length": len(text),
                "compressed_length": len(compressed),
                "compression_ratio": len(compressed) / len(text) if len(text) > 0 else 1.0,
                "replacements": total_replacements,
                "logarithmic_factor": logarithmic_factor
            }
            
            logger.info(f"Logarithmic compression: {len(text)} -> {len(compressed)} chars "
                       f"({metrics['compression_ratio']:.2f} ratio, {logarithmic_factor:.2f} log factor)")
            
            return self._create_success_result(compressed, metrics)
        except Exception as e:
            logger.error(f"Logarithmic compression error: {e}")
            return self._create_error_result(text, f"Logarithmic compression error: {e}")
    
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text that was compressed with logarithmic symbolic compression.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the decompressed text and metrics
        """
        if not text:
            return self._create_success_result(text)
        
        try:
            # Join lines (remove line breaks added during formatting)
            decompressed = text.replace("\n", " ")
            
            # Apply reverse phrase replacements
            replacements = 0
            
            # Apply each reverse pattern
            for pattern, replacement in self.reverse_patterns:
                # Count replacements
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
            
            logger.info(f"Logarithmic decompression: {len(text)} -> {len(decompressed)} chars "
                       f"({metrics['expansion_ratio']:.2f} expansion ratio)")
            
            return self._create_success_result(decompressed, metrics)
        except Exception as e:
            logger.error(f"Logarithmic decompression error: {e}")
            return self._create_error_result(text, f"Logarithmic decompression error: {e}")