# PII Masking

This document describes the Personally Identifiable Information (PII) masking functionality in SynthLang Proxy.

## Overview

PII masking is a security feature that replaces sensitive information with placeholders to protect user privacy. SynthLang includes a PII masking implementation that can:

1. Mask PII before sending to LLMs
2. Mask PII in logs and database records

This helps ensure that sensitive information is not inadvertently exposed to language models or stored in log files.

## Supported PII Types

The PII masking system can detect and mask the following types of information:

- Email addresses
- Phone numbers (various formats)
- Social Security Numbers (SSN)
- Credit card numbers
- IP addresses
- Dates (common formats)
- Street addresses
- Passport numbers

## Configuration

PII masking is configurable through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MASK_PII_BEFORE_LLM` | Controls whether PII is masked before sending to LLMs | `0` (disabled) |
| `MASK_PII_IN_LOGS` | Controls whether PII is masked in logs | `1` (enabled) |

You can set these variables in your `.env` file:

```
MASK_PII_BEFORE_LLM=1
MASK_PII_IN_LOGS=1
```

## API Usage

You can control PII masking on a per-request basis using HTTP headers:

| Header | Description | Values |
|--------|-------------|--------|
| `X-Mask-PII-Before-LLM` | Mask PII before sending to LLM | `0` (disabled) or `1` (enabled) |
| `X-Mask-PII-In-Logs` | Mask PII in logs | `0` (disabled) or `1` (enabled) |

These headers override the default configuration for the specific request.

### Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My email is user@example.com and my phone is 555-123-4567."}
    ]
  }'
```

## Implementation Details

The PII masking functionality is implemented in the `src/app/security.py` module. It uses regular expressions to identify and replace PII with placeholders.

### PII Detection Patterns

The system uses the following regex patterns to detect PII:

```python
PII_PATTERNS = [
    # Email addresses
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '<EMAIL_ADDRESS>'),
    
    # Phone numbers (various formats)
    (re.compile(r'\b\d{10}\b'), '<PHONE_NUMBER>'),  # 10-digit phone number
    (re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # 123-456-7890
    (re.compile(r'\b\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # (123) 456-7890
    (re.compile(r'\b\+\d{1,3}\s*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # +1 123-456-7890
    
    # Social Security Numbers
    (re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'), '<SSN>'),  # 123-45-6789 or 123456789
    
    # Credit Card Numbers
    (re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'), '<CREDIT_CARD>'),  # 1234-5678-9012-3456
    (re.compile(r'\b\d{16}\b'), '<CREDIT_CARD>'),  # 1234567890123456
    
    # IP Addresses
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), '<IP_ADDRESS>'),  # IPv4
    
    # Dates
    (re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'), '<DATE>'),  # MM/DD/YYYY, DD/MM/YYYY
    
    # Street Addresses
    (re.compile(r'\b\d+\s+[A-Za-z0-9\s,]+(?:Avenue|Ave|Street|St|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl)\b', 
                re.IGNORECASE), '<STREET_ADDRESS>'),
    
    # Passport Numbers
    (re.compile(r'\b[A-Z]{1,2}\d{6,9}\b'), '<PASSPORT_NUMBER>')
]
```

### Masking Process

When PII masking is enabled, the system:

1. Identifies PII in the text using regex patterns
2. Replaces the identified PII with appropriate placeholders
3. Logs that PII was detected and masked (if enabled)

## Examples

You can find examples of PII masking in the `/proxy/examples/sh/pii/` directory:

- `01_basic_pii_masking.sh`: Demonstrates basic PII masking in text
- `02_pii_masking_before_llm.sh`: Shows how to use the `X-Mask-PII-Before-LLM` header
- `03_pii_masking_in_logs.sh`: Illustrates PII masking in logs
- `04_combined_pii_masking.sh`: Demonstrates a combination of PII masking techniques
- `test_pii_masking.sh`: Tests the PII masking function directly
- `test_pii_integration.sh`: Tests the integration of PII masking with the API

## Current Status and Recommendations

Based on testing, the PII masking functionality is partially implemented:

- ✅ The PII detection and masking function works correctly when called directly
- ✅ Configuration options are available through environment variables and headers
- ❌ Integration with the API flow is incomplete
- ❌ The `X-Mask-PII-Before-LLM` header is not being honored

To fully implement PII masking, the following changes are needed:

1. Modify the API flow to apply PII masking after compression but before sending to the LLM
2. Ensure the `X-Mask-PII-Before-LLM` header is honored
3. Implement proper logging to verify PII masking in logs

A detailed implementation guide is available in the `/proxy/examples/sh/pii/implement_pii_masking.py` file.

## Best Practices

1. **Enable PII Masking in Production**: Always enable PII masking in production environments to protect sensitive user information.

2. **Test Thoroughly**: Verify that PII masking is working correctly by examining the logs and LLM responses.

3. **Inform Users**: Let users know that PII masking is in place and what types of information are protected.

4. **Regular Updates**: Periodically review and update the PII detection patterns to ensure they catch new formats and types of PII.

5. **Combine with Other Security Measures**: PII masking should be part of a comprehensive security strategy that includes encryption, access controls, and data minimization.

## Related Documentation

- [Security Best Practices](best_practices.md)
- [Configuration Guide](configuration.md)
- [API Reference](api.md)
- [Examples and Use Cases](examples_use_cases.md)