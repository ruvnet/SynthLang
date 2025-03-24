# SynthLang Proxy API Endpoint Examples

This directory contains shell script examples demonstrating all the endpoints available in the SynthLang Proxy API.

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

4. Run individual examples or use the run_all_endpoints.sh script:
   ```bash
   ./run_all_endpoints.sh
   ```

## Example Scripts

### Common Utilities

- **common.sh**: Shared utility functions used by all examples

### OpenAI-Compatible Endpoints

- **02_list_models.sh**: List available models
- **03_chat_completions.sh**: Create a chat completion
- **04_streaming_chat_completions.sh**: Create a streaming chat completion
- **05_completions_legacy.sh**: Create a completion using the legacy endpoint

### SynthLang-Specific Endpoints

- **01_health_check.sh**: Check the health of the SynthLang Proxy service
- **06_synthlang_translate.sh**: Translate natural language to SynthLang format
- **07_system_prompt_generation.sh**: Generate a system prompt from a task description
- **08_prompt_optimization.sh**: Optimize a prompt for clarity, specificity, and efficiency
- **09_prompt_evolution.sh**: Evolve a prompt using genetic algorithms
- **10_prompt_classification.sh**: Classify a prompt into categories

### Prompt Management

- **11_prompt_management.sh**: Save, load, list, delete, and compare prompts

### Cache Management

- **12_cache_management.sh**: Get cache statistics and clear the cache

### Agent Tools

- **13_agent_tools.sh**: List available tools and call them directly

### Keyword Pattern Management

- **14_keyword_pattern_management.sh**: List, add, update, delete patterns and update settings

## Features Demonstrated

- **Authentication**: All examples include proper API key handling
- **Request Formatting**: Examples of properly formatted requests for each endpoint
- **Response Parsing**: Extracting and displaying relevant information from responses
- **Error Handling**: Checking for errors and displaying appropriate messages
- **Tool Integration**: Examples of using tools directly and through chat completions
- **Streaming**: Real-time streaming of responses
- **Compression**: Using SynthLang compression to reduce token usage

## Customization

You can customize the examples by modifying the parameters passed to the API endpoints. For example:

- Change the model used for completions
- Modify the prompt or messages
- Adjust temperature and other generation parameters
- Change the tools being called

## Troubleshooting

- If you get connection errors, make sure the SynthLang Proxy server is running
- If you get authentication errors, check that your API key is valid
- If jq is not installed, the JSON output will not be formatted
- If an endpoint returns an error, check the API documentation for the correct parameters

## Additional Resources

- [SynthLang Proxy API Documentation](../../docs/api.md)
- [SynthLang Proxy CLI Documentation](../../docs/cli.md)
- [SynthLang Proxy Keyword Detection System](../../docs/keyword_detection.md)