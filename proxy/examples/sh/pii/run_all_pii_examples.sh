#!/bin/bash

# Run All PII Masking Examples
# This script runs all the PII masking examples in sequence

echo "=== Running All PII Masking Examples ==="
echo ""

# Check if we're in the right directory
if [ ! -f "01_basic_pii_masking.sh" ]; then
    echo "Error: PII example scripts not found in current directory."
    echo "Please run this script from the proxy/examples/sh/pii directory."
    exit 1
fi

# Make sure all scripts are executable
chmod +x *.sh

# Run each example with a pause between them
echo "Running example 1: Basic PII Masking"
./01_basic_pii_masking.sh
echo ""
echo "Press Enter to continue to the next example..."
read

echo "Running example 2: PII Masking Before LLM"
./02_pii_masking_before_llm.sh
echo ""
echo "Press Enter to continue to the next example..."
read

echo "Running example 3: PII Masking in Logs"
./03_pii_masking_in_logs.sh
echo ""
echo "Press Enter to continue to the next example..."
read

echo "Running example 4: Combined PII Masking"
./04_combined_pii_masking.sh
echo ""

echo "=== All PII Masking Examples Completed ==="