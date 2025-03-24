"""
Simple test script for SynthLang compression module.
"""
import sys
import os
import logging

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Import the compression module
from src.app.synthlang.compression import (
    compress_prompt,
    decompress_prompt,
    registry,
    BaseCompressor,
    SymbolCompressor,
    GzipCompressor,
    VowelRemovalCompressor,
    AbbreviationCompressor
)

def print_separator():
    print("-" * 80)

def test_compression(text, use_gzip=False, pipeline=None):
    print(f"Original text ({len(text)} chars):")
    print(text)
    print()
    
    # Compress the text
    compressed = compress_prompt(text, use_gzip=use_gzip, pipeline=pipeline)
    print(f"Compressed text ({len(compressed)} chars):")
    print(compressed)
    print()
    
    # Calculate compression ratio
    ratio = len(compressed) / len(text) if len(text) > 0 else 1.0
    print(f"Compression ratio: {ratio:.2f} ({(1-ratio)*100:.1f}% reduction)")
    print()
    
    # Decompress the text
    decompressed = decompress_prompt(compressed)
    print(f"Decompressed text ({len(decompressed)} chars):")
    print(decompressed)
    print()
    
    return compressed, decompressed

def main():
    # Test text samples
    samples = [
        "This is a simple test of the SynthLang compression system.",
        
        "The quick brown fox jumps over the lazy dog. This pangram contains all letters of the English alphabet.",
        
        """SynthLang is a framework for natural language processing and generation.
It provides tools for compressing and optimizing prompts to reduce token usage when working with large language models.
The compression algorithms use various techniques including abbreviation, vowel removal, and symbolic representation."""
    ]
    
    # Test with different samples
    for i, sample in enumerate(samples):
        print(f"\n\n{'-' * 30} SAMPLE {i+1} {'-' * 30}")
        compressed, decompressed = test_compression(sample)
        print_separator()

if __name__ == "__main__":
    main()