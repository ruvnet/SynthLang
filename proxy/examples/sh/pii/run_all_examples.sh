#!/bin/bash

# Run All PII Masking Examples
# This script runs all the PII masking examples in sequence

echo "=== Running All PII Masking Examples ==="
echo ""

# Make sure all scripts are executable
chmod +x *.sh

# Run each example
echo "1. Running Basic PII Masking Example..."
./01_basic_pii_masking.sh
echo ""

echo "2. Running PII Masking Before LLM Example..."
./02_pii_masking_before_llm.sh
echo ""

echo "3. Running PII Masking In Logs Example..."
./03_pii_masking_in_logs.sh
echo ""

echo "4. Running Combined PII Masking Example..."
./04_combined_pii_masking.sh
echo ""

echo "5. Running PII Masking Function Test..."
./test_pii_masking.sh
echo ""

echo "6. Running PII Masking Integration Test..."
./test_pii_integration.sh
echo ""

echo "7. Displaying PII Masking Implementation Guide..."
python implement_pii_masking.py
echo ""

echo "=== All Examples Completed ==="
echo ""
echo "Summary of Findings:"
echo "1. The PII masking function works correctly when called directly."
echo "2. However, it is not properly integrated with the API flow."
echo "3. The X-Mask-PII-Before-LLM header is not being honored."
echo "4. PII is visible in the compressed messages sent to the LLM."
echo ""
echo "See README.md for more details and recommendations."
echo "The implementation guide (implement_pii_masking.py) provides detailed"
echo "instructions for properly integrating PII masking with the API."