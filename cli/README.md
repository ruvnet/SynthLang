# SynthLang CLI Implementation

A command-line interface implementation of the SynthLang framework using DSPy.

## Technical Specification

### Project Structure
```
cli/
├── pyproject.toml        # Poetry project configuration
├── setup.py             # Pip installation setup
├── synthlang/           # Main package directory
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # CLI entry point
│   ├── config.py       # Configuration management
│   ├── core/           # Core functionality
│   │   ├── __init__.py
│   │   ├── models.py   # DSPy model implementations
│   │   ├── modules.py  # DSPy module definitions
│   │   └── optimizers.py # Custom optimizers
│   ├── utils/          # Utility functions
│   │   ├── __init__.py
│   │   ├── env.py      # Environment variable handling
│   │   └── logger.py   # Logging configuration
│   └── templates/      # System prompt templates
│       └── __init__.py
└── tests/              # Test directory
    ├── __init__.py
    ├── conftest.py     # Test configuration
    ├── test_cli.py     # CLI tests
    ├── test_config.py  # Configuration tests
    ├── test_models.py  # Model tests
    └── test_modules.py # Module tests
```

### Dependencies
- Python >= 3.8
- Poetry for dependency management
- Key packages:
  - dspy-ai
  - click (CLI framework)
  - python-dotenv
  - pytest (testing)
  - pytest-cov (coverage)

### Core Components

#### 1. DSPy Integration
- Implements DSPy modules for structured prompting
- Supports multiple LM backends (OpenAI, Anthropic, etc.)
- Configurable model settings and optimizers

#### 2. CLI Interface
Commands:
```
synthlang init          # Initialize configuration
synthlang compile       # Compile prompts using DSPy
synthlang optimize      # Optimize prompts and weights
synthlang run          # Execute compiled prompts
synthlang config       # Manage configuration
```

#### 3. Configuration Management
- Uses .env for API keys and secrets
- Configurable via CLI or config file
- Supports multiple environments (dev, prod)

#### 4. Testing Strategy
- Unit tests for all components
- Integration tests for CLI commands
- Mock LM responses for testing
- Coverage reporting

### Installation

Development:
```bash
# Clone repository
git clone <repo>
cd cli

# Install with poetry
poetry install

# Install in development mode
pip install -e .
```

Production:
```bash
pip install synthlang-cli
```

### Environment Variables
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
SYNTHLANG_ENV=development
SYNTHLANG_LOG_LEVEL=INFO
```

### Development Guidelines
1. Use type hints throughout the codebase
2. Follow PEP 8 style guide
3. Document all public functions and classes
4. Write tests for new functionality
5. Use pre-commit hooks for linting and formatting

### Testing
```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=synthlang
