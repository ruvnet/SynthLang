# PII Masking Examples

This directory contains examples and tests for the PII masking functionality in SynthLang.

## Overview

PII (Personally Identifiable Information) masking is a security feature that replaces sensitive information with placeholders to protect user privacy. SynthLang includes a PII masking implementation that can:

1. Mask PII before sending to LLMs
2. Mask PII in logs and database records

## Test Results

Our testing has revealed the following:

### PII Masking Function

The `mask_pii()` function in `src/app/security.py` works correctly when called directly:

- It successfully detects and masks various types of PII including:
  - Email addresses
  - Phone numbers
  - Social Security Numbers
  - Credit card numbers
  - IP addresses
  - Dates
  - Street addresses
  - Passport numbers

### API Integration

However, our integration testing shows that:

- The PII masking function is not being called in the API request/response flow
- The `X-Mask-PII-Before-LLM` header is not being honored
- PII is visible in the compressed messages sent to the LLM

## Example Scripts

This directory contains the following example scripts:

1. `01_basic_pii_masking.sh`: Demonstrates basic PII masking in text
2. `02_pii_masking_before_llm.sh`: Shows how to use the `X-Mask-PII-Before-LLM` header
3. `03_pii_masking_in_logs.sh`: Illustrates PII masking in logs using the `X-Mask-PII-In-Logs` header
4. `04_combined_pii_masking.sh`: Demonstrates a combination of PII masking techniques
5. `04_combined_pii_masking_debug.sh`: Shows detailed debug output for PII masking
6. `test_pii_masking.sh`: Tests the PII masking function directly
7. `test_pii_integration.sh`: Tests the integration of PII masking with the API
8. `implement_pii_masking.py`: Provides a guide for implementing PII masking in the API

## Test Scripts

### `test_pii_masking.sh`

This script tests the PII masking function directly by:

1. Importing the `mask_pii()` function from `src/app/security.py`
2. Applying it to a text containing various types of PII
3. Comparing the original and masked text
4. Testing each PII pattern individually

### `test_pii_integration.sh`

This script tests the integration of PII masking with the API by:

1. Making API requests with and without the `X-Mask-PII-Before-LLM` header
2. Examining the debug information in the response
3. Checking if PII is visible in the compressed messages

### `implement_pii_masking.py`

This script provides a comprehensive guide for implementing PII masking in the API:

1. Handling PII masking headers in the API endpoints
2. Applying PII masking after compression but before sending to the LLM
3. Configuring logging to mask PII in log messages
4. Testing the implementation

## Configuration

PII masking is configurable through environment variables:

- `MASK_PII_BEFORE_LLM`: Controls whether PII is masked before sending to LLMs (default: `0`)
- `MASK_PII_IN_LOGS`: Controls whether PII is masked in logs (default: `1`)

## Implementation Status

The PII masking functionality is partially implemented:

- ✅ The PII detection and masking function works correctly
- ✅ Configuration options are available
- ❌ Integration with the API flow is incomplete
- ❌ The `X-Mask-PII-Before-LLM` header is not being honored

## Recommendations

To fully implement PII masking, the following changes are needed:

1. Modify the API flow to apply PII masking after compression but before sending to the LLM
2. Ensure the `X-Mask-PII-Before-LLM` header is honored
3. Implement proper logging to verify PII masking in logs

See the `implement_pii_masking.py` script for detailed implementation guidance.

## Usage

To run all examples:

```bash
./run_all_examples.sh
```

To run a specific example:

```bash
./01_basic_pii_masking.sh
```

To test the PII masking function:

```bash
./test_pii_masking.sh
```

To test the API integration:

```bash
./test_pii_integration.sh
```

To view the implementation guide:

```bash
python implement_pii_masking.py