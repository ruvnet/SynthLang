# SynthLang Router

A high-speed LLM proxy with SynthLang integration for prompt compression.

## Overview

SynthLang Router is a middleware service that sits between clients and large language model (LLM) providers like OpenAI. It reduces latency, cuts costs, and adds enterprise features while remaining compatible with the OpenAI API.

## Features

- **Prompt Compression with SynthLang**: Uses SynthLang to compress prompts, reducing token count and latency by up to 90%
- **OpenAI-Compatible API Endpoints**: Exposes the same REST endpoints as OpenAI's API
- **Vector Similarity Cache**: Reuses past responses for semantically similar queries
- **Multi-Tenancy & API Keys**: Supports multiple users via API key authentication
- **Security & Privacy**: Encrypts stored prompts and responses, performs audit logging
- **Persistent Storage**: Stores data in a Postgres database
- **Streaming Responses**: Delivers partial results with low latency via Server-Sent Events

## Installation

### Using Poetry (recommended)

```bash
# Clone the repository
git clone https://github.com/ruvnet/SynthLang.git
cd SynthLang/proxy

# Install dependencies with Poetry
poetry install
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/ruvnet/SynthLang.git
cd SynthLang/proxy

# Install dependencies
pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database_name
ENCRYPTION_KEY=your_fernet_encryption_key_base64
USE_SYNTHLANG=1
MASK_PII_BEFORE_LLM=0
MASK_PII_IN_LOGS=1
DEFAULT_RATE_LIMIT_QPM=60
```

## Usage

### Starting the Server

```bash
# Using Poetry
poetry run uvicorn src.app.main:app --reload

# Using pip
uvicorn src.app.main:app --reload
```

### API Endpoints

- `POST /v1/chat/completions` - Chat completions endpoint (OpenAI-compatible)

## Development

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy .
```

## Docker Deployment

```bash
# Build Docker image
docker build -t synthlang-router .

# Run container
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  -e ENCRYPTION_KEY=your_key \
  synthlang-router
```

## License

MIT