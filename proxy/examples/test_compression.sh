#!/bin/bash
# Test script for SynthLang compression module

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== SynthLang Compression Test ===${NC}"
echo

# Change to the project root directory
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Create a temporary Python script for testing
TMP_SCRIPT=$(mktemp)
cat > "$TMP_SCRIPT" << 'EOF'
import sys
import logging
import os

# Add the proxy directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from proxy.src.app.synthlang.compression import (
    compress_prompt,
    decompress_prompt,
    registry,
    BaseCompressor,
    SymbolCompressor,
    GzipCompressor,
    VowelRemovalCompressor,
    AbbreviationCompressor
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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

def test_individual_compressors(text):
    print("Testing individual compressors:")
    print_separator()
    
    compressors = {
        "Basic": BasicCompressor(),
        "Abbreviation": AbbreviationCompressor(),
        "VowelRemoval": VowelRemovalCompressor(),
        "Symbol": SymbolCompressor(),
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
    print("\nTesting custom compression pipelines:")
    print_separator()
    
    pipelines = [
        ("Basic", ["basic"]),
        ("Abbreviation only", ["abbreviation"]),
        ("Vowel removal only", ["vowel"]),
        ("Symbol only", ["symbol"]),
        ("Abbreviation + Vowel", ["abbreviation", "vowel"]),
        ("Abbreviation + Symbol", ["abbreviation", "symbol"]),
        ("Full pipeline", ["basic", "abbreviation", "vowel", "symbol"]),
        ("Full pipeline + Gzip", ["basic", "abbreviation", "vowel", "symbol", "gzip"])
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

def main():
    # Test text samples
    samples = [
        "This is a simple test of the SynthLang compression system.",
        
        "The quick brown fox jumps over the lazy dog. This pangram contains all letters of the English alphabet.",
        
        """SynthLang is a framework for natural language processing and generation.
It provides tools for compressing and optimizing prompts to reduce token usage when working with large language models.
The compression algorithms use various techniques including abbreviation, vowel removal, and symbolic representation.""",
        
        """function calculateTotal(items) {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}"""
    ]
    
    # Test with different samples
    for i, sample in enumerate(samples):
        print(f"\n\n{'-' * 30} SAMPLE {i+1} {'-' * 30}")
        compressed, decompressed = test_compression(sample)
        print_separator()
    
    # Test with a longer sample for individual compressors and pipelines
    long_sample = samples[2]  # Use the third sample which is longer
    test_individual_compressors(long_sample)
    test_custom_pipelines(long_sample)

if __name__ == "__main__":
    main()
EOF

# Run the test script
echo -e "${YELLOW}Running compression tests...${NC}"
python3 "$TMP_SCRIPT"

# Clean up
rm "$TMP_SCRIPT"

echo
echo -e "${GREEN}Compression tests completed!${NC}"