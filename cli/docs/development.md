# SynthLang CLI Development Guide

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cli
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install poetry
poetry install
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

## Project Structure

```
cli/
├── docs/                 # Documentation
├── synthlang/           # Main package
│   ├── core/            # Core functionality
│   │   ├── modules.py   # DSPy modules
│   │   └── ...
│   ├── utils/           # Utilities
│   │   ├── env.py      # Environment handling
│   │   └── logger.py   # Logging
│   ├── cli.py          # CLI implementation
│   └── config.py       # Configuration
├── tests/              # Test suite
│   ├── conftest.py    # Test configuration
│   └── ...
├── .env.sample        # Environment template
└── pyproject.toml     # Project configuration
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following these guidelines:
   - Follow PEP 8 style guide
   - Add type hints to all functions
   - Document new functions and classes
   - Write tests for new functionality

3. Run tests:
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=synthlang

# Run specific test file
poetry run pytest tests/test_specific.py
```

4. Format code:
```bash
# Format with black
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy synthlang
```

## Testing

### Test Organization

- `test_cli.py`: CLI interface tests
- `test_config.py`: Configuration management tests
- `test_modules.py`: DSPy module tests
- `test_logger.py`: Logging functionality tests

### Writing Tests

1. Use fixtures from `conftest.py` when possible
2. Follow the Arrange-Act-Assert pattern
3. Use descriptive test names
4. Add docstrings to test functions
5. Use appropriate markers for different test types

Example:
```python
@pytest.mark.integration
def test_framework_translation(lm):
    """Test framework translation with actual API call."""
    translator = FrameworkTranslator(lm)
    result = translator.translate("source code here")
    assert "target" in result
```

## DSPy Integration

### Key Components

1. `SynthLangModule`: Base class for DSPy modules
2. `FrameworkTranslator`: Handles code translation
3. `SystemPromptGenerator`: Generates system prompts

### Adding New Modules

1. Create a new class inheriting from `SynthLangModule`
2. Define the signature using `@signature` decorator
3. Implement the required methods
4. Add tests for the new module

Example:
```python
@signature
class NewModuleSignature:
    input: str
    output: str

class NewModule(SynthLangModule):
    def __init__(self, lm):
        super().__init__(lm)
        self.predictor = Predict(NewModuleSignature)

    def process(self, input_text: str) -> Dict[str, Any]:
        # Implementation here
        pass
```

## Configuration Management

### Environment Variables

- Use `SYNTHLANG_` prefix for all environment variables
- Document new variables in `.env.sample`
- Add validation in `config.py`

### Adding New Settings

1. Add the setting to the `Config` class in `config.py`
2. Update configuration tests
3. Document the new setting
4. Update the sample environment file

## Logging

### Log Levels

- DEBUG: Detailed debugging information
- INFO: General operational events
- WARNING: Unexpected but handled events
- ERROR: Serious issues that need attention
- CRITICAL: System-level failures

### Best Practices

1. Use appropriate log levels
2. Include relevant context in log messages
3. Handle exceptions properly
4. Use structured logging when appropriate

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run full test suite
4. Build distribution:
```bash
poetry build
```
5. Create a release tag
6. Push to PyPI:
```bash
poetry publish
```

## Contributing

1. Check existing issues and pull requests
2. Discuss major changes in issues first
3. Follow the code style guidelines
4. Include tests with your changes
5. Update documentation as needed
6. Submit a pull request

## Resources

- [DSPy Documentation](https://dspy.ai/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PyTest Documentation](https://docs.pytest.org/)
