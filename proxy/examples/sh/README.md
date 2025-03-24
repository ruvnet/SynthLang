# SynthLang Proxy API Examples

This directory contains example shell scripts demonstrating various features of the SynthLang Proxy API.

## Prerequisites

- SynthLang Proxy server running on localhost:8000
- jq installed for JSON formatting (`apt-get install jq` or `brew install jq`)
- API key generated and available in your environment

## Getting Started

1. Make sure the SynthLang Proxy server is running:
   ```bash
   cd /workspaces/SynthLang/proxy
   python -m src.app.main
   ```

2. Generate an API key if you don't have one:
   ```bash
   cd /workspaces/SynthLang/proxy
   python -m src.cli.api_keys create --user-id test_user --rate-limit 100 --save-env
   ```

3. Make the example scripts executable:
   ```bash
   chmod +x *.sh
   ```

4. Run individual examples or use the run_all_examples.sh script:
   ```bash
   ./run_all_examples.sh
   ```

## Example Scripts

### Basic Examples

- **01_simple_chat.sh**: Basic chat completion request with gpt-3.5-turbo
- **02_gpt4o_mini_example.sh**: Using the gpt-4o-mini model
- **03_o3_mini_example.sh**: Using the o3-mini model
- **04_streaming_example.sh**: Streaming responses in real-time

### Tool Examples

- **05_weather_tool_example.sh**: Using the weather tool via pattern detection
- **06_calculator_tool_example.sh**: Using the calculator tool via pattern detection
- **09_hashtag_directive_example.sh**: Using the #weather hashtag directive to trigger the weather tool
- **10_function_calling_example.sh**: Using the #calculator hashtag directive with parameters

### Compression Examples

- **07_compression_example.sh**: Using SynthLang compression to reduce token usage
- **08_gzip_compression_example.sh**: Using gzip compression on top of SynthLang compression

### Complex Examples

- **11_complex_example.sh**: Complex scenario combining multiple features (system message, multi-turn conversation, tool invocation, streaming)

### PII Masking Examples

- **pii/01_basic_pii_masking.sh**: Demonstrates basic PII masking in text
- **pii/02_pii_masking_before_llm.sh**: Shows how to mask PII before sending to LLMs
- **pii/03_pii_masking_in_logs.sh**: Illustrates PII masking in logs
- **pii/04_combined_pii_masking.sh**: Demonstrates a combination of PII masking techniques
- **pii/04_combined_pii_masking_debug.sh**: Shows detailed debug output for PII masking
- **pii/test_pii_masking.sh**: Tests the PII masking function directly
- **pii/test_pii_integration.sh**: Tests the integration of PII masking with the API
- **pii/implement_pii_masking.py**: Provides a guide for implementing PII masking in the API

To run all PII masking examples:
```bash
cd pii
./run_all_examples.sh
```

## Features Demonstrated

- **Different Models**: Examples of using gpt-3.5-turbo, gpt-4o-mini, and o3-mini
- **Streaming**: Real-time streaming of responses
- **Tool Usage**: Both automatic pattern detection and explicit hashtag directives
- **Compression**: SynthLang compression and gzip compression for token reduction
- **Multi-turn Conversations**: Maintaining context across multiple messages
- **System Messages**: Setting the assistant's behavior
- **PII Masking**: Protection of personally identifiable information in logs and before sending to LLMs
  - PII detection and masking for emails, phone numbers, SSNs, credit cards, etc.
  - Control via HTTP headers (X-Mask-PII-Before-LLM, X-Mask-PII-In-Logs)
  - Testing and implementation guidance

## API Key Handling

All scripts include automatic API key handling:
- They check for an API key in the environment
- If no key is found, they attempt to create one using the CLI
- The key is then used for all API requests

## Troubleshooting

- If you get connection errors, make sure the SynthLang Proxy server is running
- If you get authentication errors, check that your API key is valid
- If the hashtag directives aren't working, ensure the keyword detection system is properly configured
- If PII masking isn't working, check the implementation guide in pii/implement_pii_masking.py

## Additional Resources

- [SynthLang Proxy Documentation](../docs/)
- [API Reference](../docs/api.md)
- [CLI Documentation](../docs/cli.md)
- [Keyword Detection System](../docs/keyword_detection.md)
- [PII Masking Documentation](pii/README.md)