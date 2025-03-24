"""
Test script for SynthLang compression strategies.

This script demonstrates the different compression strategies available
in the modular compression system, including the new logarithmic symbolic
compression from the SynthLang CLI.
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
    AbbreviationCompressor,
    BasicCompressor,
    LogarithmicSymbolicCompressor
)

# Import the core module for compression config
from src.app.synthlang.core import CompressionConfig

def print_separator():
    print("-" * 80)

def test_individual_compressors(text):
    """Test each compression strategy individually."""
    print("\nTesting individual compressors:")
    print_separator()
    
    compressors = {
        "Basic": BasicCompressor(),
        "Abbreviation": AbbreviationCompressor(),
        "VowelRemoval": VowelRemovalCompressor(),
        "Symbol": SymbolCompressor(),
        "Logarithmic": LogarithmicSymbolicCompressor(),
        "Gzip": GzipCompressor()
    }
    
    for name, compressor in compressors.items():
        print(f"\n{name} Compressor:")
        result = compressor.compress(text)
        if result.success:
            print(f"Compressed ({len(result.text)} chars): {result.text[:100]}{'...' if len(result.text) > 100 else ''}")
            print(f"Metrics: {result.metrics}")
            
            # Test decompression
            decomp_result = compressor.decompress(result.text)
            if decomp_result.success:
                print(f"Decompressed ({len(decomp_result.text)} chars): {decomp_result.text[:100]}{'...' if len(decomp_result.text) > 100 else ''}")
            else:
                print(f"Decompression failed: {decomp_result.error}")
        else:
            print(f"Compression failed: {result.error}")
        
        print_separator()

def test_custom_pipelines(text):
    """Test different compression pipelines."""
    print("\nTesting custom compression pipelines:")
    print_separator()
    
    pipelines = [
        ("Basic", ["basic"]),
        ("Abbreviation only", ["abbreviation"]),
        ("Vowel removal only", ["vowel"]),
        ("Symbol only", ["symbol"]),
        ("Logarithmic only", ["logarithmic"]),
        ("Abbreviation + Vowel", ["abbreviation", "vowel"]),
        ("Abbreviation + Symbol", ["abbreviation", "symbol"]),
        ("Abbreviation + Logarithmic", ["abbreviation", "logarithmic"]),
        ("Full pipeline", ["basic", "abbreviation", "vowel", "symbol"]),
        ("Full pipeline + Logarithmic", ["basic", "abbreviation", "vowel", "symbol", "logarithmic"]),
        ("Full pipeline + Logarithmic + Gzip", ["basic", "abbreviation", "vowel", "symbol", "logarithmic", "gzip"])
    ]
    
    for name, pipeline in pipelines:
        print(f"\n{name} Pipeline:")
        compressed = compress_prompt(text, pipeline=pipeline)
        ratio = len(compressed) / len(text) if len(text) > 0 else 1.0
        print(f"Compressed ({len(compressed)} chars): {compressed[:100]}{'...' if len(compressed) > 100 else ''}")
        print(f"Compression ratio: {ratio:.2f} ({(1-ratio)*100:.1f}% reduction)")
        
        # Test decompression for non-gzip pipelines
        if "gzip" not in pipeline:
            decompressed = decompress_prompt(compressed, pipeline=list(reversed(pipeline)))
            print(f"Decompressed ({len(decompressed)} chars): {decompressed[:100]}{'...' if len(decompressed) > 100 else ''}")
        
        print_separator()

def test_compression_levels(text):
    """Test the predefined compression levels."""
    print("\nTesting predefined compression levels:")
    print_separator()
    
    levels = ["low", "medium", "high"]
    
    for level in levels:
        print(f"\n{level.capitalize()} Compression Level:")
        pipeline = CompressionConfig.get_pipeline_for_level(level)
        print(f"Pipeline: {pipeline}")
        
        compressed = compress_prompt(text, pipeline=pipeline)
        ratio = len(compressed) / len(text) if len(text) > 0 else 1.0
        print(f"Compressed ({len(compressed)} chars): {compressed[:100]}{'...' if len(compressed) > 100 else ''}")
        print(f"Compression ratio: {ratio:.2f} ({(1-ratio)*100:.1f}% reduction)")
        
        # Test decompression
        decompressed = decompress_prompt(compressed, pipeline=list(reversed(pipeline)))
        print(f"Decompressed ({len(decompressed)} chars): {decompressed[:100]}{'...' if len(decompressed) > 100 else ''}")
        
        print_separator()

def main():
    # Test text
    text = """SynthLang is a framework for natural language processing and generation.
It provides tools for compressing and optimizing prompts to reduce token usage when working with large language models.
The compression algorithms use various techniques including abbreviation, vowel removal, and symbolic representation.
Input data and process algorithms to output results efficiently."""
    
    print(f"Original text ({len(text)} chars):")
    print(text)
    print()
    
    # Test individual compressors
    test_individual_compressors(text)
    
    # Test custom pipelines
    test_custom_pipelines(text)
    
    # Test compression levels
    test_compression_levels(text)
    
    # Test with a more complex example that will benefit from logarithmic compression
    complex_text = """
The system should extract customer feedback data from the database, analyze sentiment scores,
and generate a summary report with key insights. If the sentiment score is greater than 0.7,
categorize as positive feedback. If the sentiment score is less than 0.3, categorize as negative feedback.
Otherwise, categorize as neutral feedback. For each category, calculate the average score and identify
the top 5 most frequent keywords. The final output should include:
- Overall sentiment distribution
- Trend analysis over time
- Key topic extraction
- Actionable recommendations based on negative feedback
- Strengths identified from positive feedback

The implementation should use natural language processing techniques for text analysis,
machine learning models for sentiment prediction, and data visualization components for the report.
"""
    
    print("\n\n" + "=" * 40 + " COMPLEX EXAMPLE " + "=" * 40)
    print(f"\nOriginal complex text ({len(complex_text)} chars):")
    print(complex_text)
    print()
    
    # Test logarithmic compression specifically on the complex example
    print("\nLogarithmic Compression on Complex Example:")
    logarithmic = LogarithmicSymbolicCompressor()
    result = logarithmic.compress(complex_text)
    if result.success:
        print(f"Compressed ({len(result.text)} chars):")
        print(result.text)
        print(f"\nCompression ratio: {result.metrics['compression_ratio']:.2f} "
              f"({(1-result.metrics['compression_ratio'])*100:.1f}% reduction)")
        print(f"Logarithmic factor: {result.metrics['logarithmic_factor']:.2f}")
        
        # Test decompression
        decomp_result = logarithmic.decompress(result.text)
        if decomp_result.success:
            print(f"\nDecompressed ({len(decomp_result.text)} chars):")
            print(decomp_result.text)
        else:
            print(f"\nDecompression failed: {decomp_result.error}")
    else:
        print(f"Compression failed: {result.error}")
    
    print_separator()
    
    # Test high compression level on the complex example
    print("\nHigh Compression Level on Complex Example:")
    high_pipeline = CompressionConfig.get_pipeline_for_level("high")
    compressed = compress_prompt(complex_text, pipeline=high_pipeline)
    ratio = len(compressed) / len(complex_text) if len(complex_text) > 0 else 1.0
    print(f"Compressed ({len(compressed)} chars):")
    print(compressed)
    print(f"\nCompression ratio: {ratio:.2f} ({(1-ratio)*100:.1f}% reduction)")
    
    # Test decompression
    decompressed = decompress_prompt(compressed, pipeline=list(reversed(high_pipeline)))
    print(f"\nDecompressed ({len(decompressed)} chars):")
    print(decompressed)
    
    print_separator()

if __name__ == "__main__":
    main()