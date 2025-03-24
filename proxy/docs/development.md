# SynthLang Proxy Development Guide

This guide is intended for developers who want to extend, customize, or contribute to SynthLang Proxy.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Poetry (recommended for dependency management)
- Docker (optional, for containerized development)
- PostgreSQL (optional, SQLite can be used for development)

### Clone the Repository

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy
```

### Install Dependencies

Using Poetry (recommended):

```bash
poetry install
```

Using pip:

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the repository root:

```
# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=true

# Database Configuration
USE_SQLITE=1
SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db

# Security
# Generate a secure random key for development
ENCRYPTION_KEY=your_development_encryption_key

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key
```

### Run Tests

```bash
pytest
```

### Run the Development Server

```bash
python -m app.main
```

This will start the development server at http://localhost:8000.

## Project Structure

SynthLang Proxy follows a modular architecture. Here's an overview of the project structure:

```
proxy/
├── src/                # Source code
│   ├── app/            # Application code
│   │   ├── __init__.py 
│   │   ├── main.py     # Application entry point
│   │   ├── api/        # API endpoints
│   │   ├── auth/       # Authentication and authorization
│   │   ├── agents/     # Agent tools and framework
│   │   ├── benchmark/  # Benchmarking framework
│   │   ├── cache/      # Semantic caching
│   │   ├── config/     # Configuration management
│   │   ├── keywords/   # Keyword detection system
│   │   ├── models/     # Data models
│   │   ├── providers/  # LLM provider integrations
│   │   ├── synthlang/  # SynthLang integration
│   │   └── utils/      # Utility functions
│   ├── cli/            # Command-line interface
│   │   ├── __init__.py
│   │   ├── commands/   # CLI commands
│   │   └── utils/      # CLI utilities
├── tests/              # Test suite
│   ├── conftest.py     # Test fixtures
│   ├── test_api/       # API tests
│   ├── test_auth/      # Authentication tests
│   └── ...             # Other test modules
├── config/             # Configuration files
│   ├── keywords.toml   # Keyword pattern definitions
│   └── ...             # Other configuration files
├── docs/               # Documentation
├── .env.sample         # Sample environment variables
├── pyproject.toml      # Project configuration
└── README.md           # Project README
```

## Architecture Overview

SynthLang Proxy follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Implements business logic
3. **Repository Layer**: Manages data access
4. **Infrastructure Layer**: Provides integration with external systems

For a detailed architecture overview, see [Architecture Documentation](architecture.md).

## Extending SynthLang Proxy

### Adding a New Agent Tool

Agent tools allow SynthLang Proxy to perform actions and integrate with external services. Here's how to add a new tool:

1. Create a new file in `src/app/agents/tools/` (e.g., `stock_price.py`):

```python
from app.agents.registry import register_tool

async def get_stock_price(ticker, user_message=None, user_id=None):
    """
    Get the current stock price for a ticker symbol.
    
    Args:
        ticker (str): Stock ticker symbol
        user_message (str, optional): Original user message
        user_id (str, optional): ID of the user making the request
        
    Returns:
        dict: Response containing stock price information
    """
    # Implement your stock price logic here
    # For example, calling a stock price API
    
    # Return a formatted response
    return {
        "content": f"The current price of {ticker} is $150.25"
    }

# Register the tool with the tool registry
register_tool("stock_price", get_stock_price)
```

2. Create a test file in `tests/test_agents/tools/` (e.g., `test_stock_price.py`):

```python
import pytest
from app.agents.tools.stock_price import get_stock_price

@pytest.mark.asyncio
async def test_get_stock_price():
    # Test the stock price tool
    result = await get_stock_price("AAPL")
    assert "content" in result
    assert "AAPL" in result["content"]
```

3. Update `src/app/agents/__init__.py` to import your new tool:

```python
# Import tools to register them
from app.agents.tools import weather, calculator, web_search, stock_price
```

4. Add a keyword pattern for your tool in `config/keywords.toml`:

```toml
[patterns.stock_price_query]
name = "stock_price_query"
pattern = "(?:what's|what is|get|check)\\s+(?:the)?\\s*(?:stock price|share price|stock value)\\s+(?:of|for)?\\s+(?P<ticker>[A-Z]+)"
tool = "stock_price"
description = "Detects requests for stock price information"
priority = 95
required_role = "premium"
enabled = true
```

### Adding a New LLM Provider

SynthLang Proxy can be extended to support additional LLM providers:

1. Create a new file in `src/app/providers/` (e.g., `anthropic.py`):

```python
from typing import Dict, Any, AsyncGenerator, Optional, List
from app.providers.base import BaseProvider
from app.models.api import ChatMessage, ChatCompletionRequest, ChatCompletionResponse, ChatCompletionChunk

class AnthropicProvider(BaseProvider):
    """Provider for Anthropic Claude API."""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        
    async def chat_completion(
        self, 
        request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """
        Generate a chat completion using Anthropic's Claude API.
        """
        # Implement API call to Anthropic
        # Convert request from OpenAI format to Anthropic format
        # Convert response from Anthropic format to OpenAI format
        # Return standardized response
        
    async def chat_completion_stream(
        self, 
        request: ChatCompletionRequest
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        """
        Stream a chat completion using Anthropic's Claude API.
        """
        # Implement streaming API call to Anthropic
        # Convert request from OpenAI format to Anthropic format
        # Convert streaming response from Anthropic format to OpenAI format
        # Yield standardized chunks
```

2. Register your provider in `src/app/providers/__init__.py`:

```python
from app.providers.openai import OpenAIProvider
from app.providers.anthropic import AnthropicProvider

def get_provider(provider_name: str, api_key: str):
    """Get the appropriate provider instance."""
    if provider_name == "openai":
        return OpenAIProvider(api_key)
    elif provider_name == "anthropic":
        return AnthropicProvider(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
```

3. Update configuration to support the new provider:

```python
# In src/app/config/settings.py
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

### Adding a New API Endpoint

To add a new API endpoint:

1. Create or update a file in `src/app/api/` (e.g., `custom.py`):

```python
from fastapi import APIRouter, Depends, HTTPException
from app.auth.api_keys import verify_api_key
from app.models.custom import CustomRequest, CustomResponse

router = APIRouter(prefix="/v1/custom", tags=["custom"])

@router.post("/process", response_model=CustomResponse)
async def process_custom_request(
    request: CustomRequest,
    user_id: str = Depends(verify_api_key)
):
    """
    Process a custom request.
    """
    # Implement your custom endpoint logic
    result = await custom_service.process(request, user_id)
    return result
```

2. Register your router in `src/app/api/__init__.py`:

```python
from fastapi import APIRouter
from app.api import chat, models, custom

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(models.router)
api_router.include_router(custom.router)
```

### Adding a New CLI Command

To add a new CLI command:

1. Create a new file in `src/cli/commands/` (e.g., `custom.py`):

```python
import click
from cli.utils import config

@click.group()
def custom():
    """Custom command group."""
    pass

@custom.command()
@click.argument("input_text")
@click.option("--output", "-o", help="Output file")
def process(input_text, output):
    """Process custom input."""
    # Implement your command logic
    result = "Processed: " + input_text
    
    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        click.echo(result)
```

2. Register your command in `src/cli/cli.py`:

```python
from cli.commands import translate, proxy, custom

cli = click.Group()
cli.add_command(translate)
cli.add_command(proxy)
cli.add_command(custom)
```

## Working with the Codebase

### Code Style

SynthLang Proxy follows these coding conventions:

- **Python Style Guide**: PEP 8
- **Docstrings**: Google-style docstrings
- **Type Hints**: Use Python type hints for better code readability
- **Variable Naming**: 
  - Use snake_case for variables and functions
  - Use PascalCase for classes
  - Use UPPERCASE for constants
- **Comment Style**: Use comments to explain why, not what

### Pre-commit Hooks

The repository uses pre-commit hooks to ensure code quality. Install them with:

```bash
pip install pre-commit
pre-commit install
```

### Logging

Use the built-in logging system:

```python
from app.utils.logging import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Error Handling

Follow these guidelines for error handling:

1. Use custom exceptions defined in `app.utils.exceptions`
2. Propagate errors to the appropriate layer
3. Use try/except blocks to catch specific exceptions
4. Log errors with context

Example:

```python
from app.utils.exceptions import ResourceNotFoundError, PermissionDeniedError
from app.utils.logging import get_logger

logger = get_logger(__name__)

async def get_resource(resource_id, user_id):
    try:
        resource = await repository.get_by_id(resource_id)
        
        if not resource:
            raise ResourceNotFoundError(f"Resource {resource_id} not found")
            
        if not has_permission(user_id, resource):
            raise PermissionDeniedError(f"User {user_id} does not have permission to access {resource_id}")
            
        return resource
    
    except (ResourceNotFoundError, PermissionDeniedError) as e:
        # Re-raise these exceptions to be handled by the API layer
        logger.warning(f"Access error: {str(e)}")
        raise
        
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error accessing resource {resource_id}: {str(e)}", exc_info=True)
        raise
```

## Testing

### Unit Tests

Write unit tests for individual components:

```python
import pytest
from app.synthlang.compression import compress, decompress

def test_compression():
    original = "This is a test prompt for compression"
    compressed = compress(original)
    
    # Verify compression reduces size
    assert len(compressed) < len(original)
    
    # Verify decompression restores original
    decompressed = decompress(compressed)
    assert decompressed == original
```

### Integration Tests

Write integration tests for component interactions:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chat_endpoint_with_cache():
    # Set up a test client
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First request should trigger LLM call and cache result
        response1 = await client.post(
            "/v1/chat/completions",
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ]
            },
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Second request with similar content should hit cache
        response2 = await client.post(
            "/v1/chat/completions",
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": "Hi, how are you doing?"}
                ]
            },
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Both responses should be successful
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # The second response should have a cache hit header
        assert response2.headers.get("X-Cache-Hit") == "true"
```

### End-to-End Tests

Write end-to-end tests for full workflows:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_complete_workflow():
    # Set up a test client
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Step 1: Send a chat request with a keyword pattern
        chat_response = await client.post(
            "/v1/chat/completions",
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": "What's the weather in London?"}
                ]
            },
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Verify that the weather tool was triggered
        assert chat_response.status_code == 200
        assert "London" in chat_response.json()["choices"][0]["message"]["content"]
        assert "temperature" in chat_response.json()["choices"][0]["message"]["content"].lower()
```

### Mocking

Use mocks to isolate components during testing:

```python
import pytest
from unittest.mock import patch, AsyncMock
from app.providers.openai import OpenAIProvider

@pytest.mark.asyncio
async def test_openai_provider_with_mock():
    # Create a mock for the OpenAI API client
    mock_openai_client = AsyncMock()
    mock_openai_client.chat.completions.create.return_value = {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-4o",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18
        }
    }
    
    # Patch the OpenAI client creation
    with patch("app.providers.openai.OpenAI", return_value=mock_openai_client):
        provider = OpenAIProvider("fake_api_key")
        
        # Call the method under test
        result = await provider.chat_completion({
            "model": "gpt-4o",
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        })
        
        # Verify the result
        assert result.choices[0].message.content == "Hello! How can I help you today?"
        
        # Verify the mock was called with expected arguments
        mock_openai_client.chat.completions.create.assert_called_once()
```

## Continuous Integration and Deployment

### CI Workflow

SynthLang Proxy uses GitHub Actions for continuous integration:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    - name: Lint
      run: |
        poetry run black --check .
        poetry run isort --check .
        poetry run mypy .
    - name: Test
      run: |
        poetry run pytest --cov=app
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### CD Workflow

```yaml
# .github/workflows/cd.yml
name: CD

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    - name: Login to Container Registry
      uses: docker/login-action@v1
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

## Database Migrations

SynthLang Proxy uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Revert to a specific version
alembic downgrade <revision>
```

## Documentation

### Code Documentation

- Use Google-style docstrings
- Document all public functions, methods, and classes
- Include type hints

Example:

```python
def compress(text: str, use_gzip: bool = False) -> str:
    """
    Compress text using SynthLang compression algorithm.
    
    Applies semantic compression to reduce token usage while preserving meaning.
    Optionally applies additional gzip compression for larger texts.
    
    Args:
        text: The text to compress
        use_gzip: Whether to apply additional gzip compression
        
    Returns:
        The compressed text
        
    Raises:
        ValueError: If the input text is empty
    """
    if not text:
        raise ValueError("Input text cannot be empty")
        
    # Compression logic...
    
    return compressed_text
```

### API Documentation

- Use FastAPI's built-in documentation features
- Add detailed descriptions to endpoints, parameters, and responses

Example:

```python
@router.post("/compress", response_model=CompressResponse)
async def compress_text(
    request: CompressRequest,
    user_id: str = Depends(verify_api_key)
):
    """
    Compress text using SynthLang compression algorithm.
    
    This endpoint applies semantic compression to reduce token usage while
    preserving meaning. For larger texts, additional gzip compression can
    be applied for even greater reduction.
    
    - Typical compression ratio: 40-60%
    - Response includes original and compressed sizes
    - Token counts are estimated based on GPT-4 tokenization
    
    Args:
        request: The compression request containing text to compress
        user_id: User ID from API key verification
        
    Returns:
        CompressResponse with original and compressed text, sizes, and metrics
    """
    result = await compression_service.compress(request.text, request.use_gzip)
    return result
```

## Contributing

### Contribution Guidelines

Follow these steps to contribute to SynthLang Proxy:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Process

1. Update documentation if needed
2. Include tests for new functionality
3. Update the CHANGELOG.md file
4. Get approval from at least one maintainer

### Code Review Guidelines

- Check for code quality and style
- Verify tests are included and pass
- Ensure documentation is updated
- Look for security issues
- Verify performance implications

## Troubleshooting Development Issues

### Common Issues

1. **Database Connection Errors**
   - Check that the database is running
   - Verify connection URL in `.env`
   - Check for network issues if using remote database

2. **API Key Issues**
   - Verify API key format
   - Check environment variables
   - Check API key permissions

3. **Dependency Issues**
   - Try `poetry lock --no-update` followed by `poetry install`
   - Verify Python version compatibility

4. **Performance Issues**
   - Enable logging to identify bottlenecks
   - Check for N+1 database queries
   - Verify cache is working properly

### Debugging Tools

1. **Python Debugger**:
   ```python
   import pdb; pdb.set_trace()
   ```

2. **FastAPI Debug Mode**:
   ```python
   uvicorn app.main:app --reload --debug
   ```

3. **SQLAlchemy Echo Mode**:
   ```python
   engine = create_async_engine(DATABASE_URL, echo=True)
   ```

4. **Request Logging Middleware**:
   ```python
   @app.middleware("http")
   async def log_requests(request: Request, call_next):
       start_time = time.time()
       response = await call_next(request)
       process_time = time.time() - start_time
       logger.debug(f"Request {request.method} {request.url.path} took {process_time:.2f}s")
       return response
   ```

## Performance Optimization

### Database Optimization

- Use indexes for frequently queried fields
- Batch database operations when possible
- Use appropriate fetch sizes for queries
- Consider using connection pooling

### Caching Strategies

- Use semantic caching for similar requests
- Consider Redis for distributed caching
- Implement tiered caching (memory + persistent)
- Set appropriate cache expiration policies

### Async/Await Best Practices

- Use asyncio for I/O-bound operations
- Avoid blocking operations in async code
- Use `asyncio.gather` for parallel operations
- Be mindful of the event loop

Example:

```python
import asyncio
from app.providers.openai import OpenAIProvider

async def get_multiple_completions(provider: OpenAIProvider, prompts: list[str]):
    """Get completions for multiple prompts in parallel."""
    async def get_completion(prompt):
        request = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}]
        }
        return await provider.chat_completion(request)
    
    # Execute all requests in parallel
    results = await asyncio.gather(*[get_completion(prompt) for prompt in prompts])
    return results
```

## Security Considerations

### API Key Management

- Never hardcode API keys
- Rotate API keys regularly
- Use environment variables for API keys
- Consider using a secrets management solution

### Input Validation

- Validate all user inputs
- Use Pydantic models for request validation
- Sanitize inputs to prevent injection attacks
- Implement rate limiting

### Authentication and Authorization

- Use secure API key validation
- Implement role-based access control
- Verify permissions for each operation
- Log authentication failures

### Sensitive Data Handling

- Encrypt sensitive data at rest
- Mask PII in logs and responses
- Use secure connections (HTTPS)
- Implement proper error handling to avoid leaking sensitive information

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/)
- [PyTest Documentation](https://docs.pytest.org/)