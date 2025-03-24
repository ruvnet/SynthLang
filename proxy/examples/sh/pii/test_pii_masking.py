import sys
import os
import logging

# Add the proxy directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Import the security module
try:
    from src.app.security import mask_pii, PII_PATTERNS
    print("Successfully imported security module")
except ImportError as e:
    print(f"Error importing security module: {e}")
    sys.exit(1)

# Test if the PII masking function works
def test_pii_masking(text):
    print("\n=== Testing PII Masking Function ===")
    print(f"Number of PII patterns defined: {len(PII_PATTERNS)}")
    
    # Print the patterns
    print("\nPII patterns defined:")
    for i, (pattern, placeholder) in enumerate(PII_PATTERNS):
        print(f"{i+1}. {pattern.pattern} -> {placeholder}")
    
    # Test the masking function
    print("\nApplying PII masking to text...")
    masked_text = mask_pii(text)
    
    print("\nOriginal text:")
    print(text)
    
    print("\nMasked text:")
    print(masked_text)
    
    # Check if any PII was masked
    if masked_text != text:
        print("\nResult: PII masking is FUNCTIONAL ✓")
        print("PII was successfully detected and masked.")
    else:
        print("\nResult: PII masking is NOT FUNCTIONAL ✗")
        print("No PII was masked in the text.")
    
    # Check each pattern individually
    print("\nTesting each pattern individually:")
    for i, (pattern, placeholder) in enumerate(PII_PATTERNS):
        matches = pattern.findall(text)
        if matches:
            print(f"{i+1}. {placeholder}: {len(matches)} matches found - {matches}")
        else:
            print(f"{i+1}. {placeholder}: No matches found")

# Get the text from command line argument
if len(sys.argv) > 1:
    test_pii_masking(sys.argv[1])
else:
    print("No text provided. Please provide text with PII to test.")
    sys.exit(1)
