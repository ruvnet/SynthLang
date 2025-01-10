# SynthLang CLI Usage Guide

## Installation

Install the SynthLang CLI using pip:

```bash
pip install synthlang-cli
```

Or install from source:

```bash
git clone <repository-url>
cd cli
pip install -e .
```

## Configuration

1. Copy the sample environment file:
```bash
cp .env.sample .env
```

2. Edit `.env` with your settings:
```bash
# Required: Your OpenAI API key
OPENAI_API_KEY=your-api-key-here

# Optional: Configure model and environment
SYNTHLANG_MODEL=gpt-4o-mini
SYNTHLANG_ENV=development
SYNTHLANG_LOG_LEVEL=INFO
```

## Basic Commands

### Initialize Configuration
```bash
synthlang init --config config.json
```

### Translate Code Between Frameworks
```bash
# Translate from a file
synthlang translate --config config.json --source path/to/source.js --target-framework python

# Translate from stdin
echo "function hello() { console.log('Hello') }" | synthlang translate --config config.json --target-framework python
```

### Generate System Prompts
```bash
synthlang generate --config config.json --task "Create a chatbot that helps users learn Python"
```

### Optimize Prompts
```bash
synthlang optimize --config config.json --prompt "You are a helpful assistant..."
```

### Manage Configuration
```bash
# Show current configuration
synthlang config show --config config.json

# Update configuration value
synthlang config set --config config.json --key model --value gpt-4o-mini
```

## Environment Variables

The CLI supports the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `SYNTHLANG_MODEL`: Model to use (default: gpt-4o-mini)
- `SYNTHLANG_ENV`: Environment (development, production, testing)
- `SYNTHLANG_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `SYNTHLANG_LOG_FILE`: Path to log file (optional)
- `SYNTHLANG_CONFIG_PATH`: Path to configuration file (optional)

## Examples

### Framework Translation
```bash
# Translate React component to Vue
synthlang translate --config config.json \
  --source "function App() { return <div>Hello</div> }" \
  --target-framework vue
```

### System Prompt Generation
```bash
# Generate a prompt for code review
synthlang generate --config config.json \
  --task "Create an AI assistant that helps with Python code review"
```

### Configuration Management
```bash
# Initialize with custom settings
synthlang init --config config.json

# Update log level
synthlang config set --config config.json --key log_level --value DEBUG

# Show current settings
synthlang config show --config config.json
```

## Error Handling

The CLI provides detailed error messages and logs. If you encounter issues:

1. Check the log output (use DEBUG level for more detail)
2. Verify your configuration settings
3. Ensure your API key is valid
4. Check your internet connection

## Best Practices

1. Always use version control for your prompts and translations
2. Start with small, simple translations to verify behavior
3. Use the DEBUG log level during development
4. Keep your API key secure and never commit it to version control
5. Use separate configuration files for different environments

## Support

For issues and feature requests, please visit:
- GitHub Issues: [Link to issues]
- Documentation: [Link to docs]
