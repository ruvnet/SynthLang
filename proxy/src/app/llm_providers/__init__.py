"""
LLM provider integration module.

This module provides functions for interacting with LLM providers
such as OpenAI to get chat completions and embeddings.
It's designed to be modular and extensible to support multiple providers.
"""
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, AsyncGenerator, Type

from dotenv import load_dotenv

from .exceptions import (
    LLMProviderError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMModelNotFoundError,
    LLMInvalidRequestError
)
from .base import BaseLLMProvider
from .factory import LLMProviderFactory
from .providers.openai_provider import OpenAIProvider

# Configure logging
logger = logging.getLogger(__name__)

# Load API key directly from .env file
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
if env_path.exists():
    logger.info(f"LLM Provider: Loading environment variables from {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    logger.warning(f"LLM Provider: No .env file found at {env_path}")

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("LLM Provider: OPENAI_API_KEY environment variable is not set.")
else:
    logger.info("LLM Provider: OPENAI_API_KEY environment variable is set.")

# Register the OpenAI provider
LLMProviderFactory.register_provider("openai", OpenAIProvider)

# Create default provider instance (OpenAI)
default_provider = LLMProviderFactory.create_provider("openai")

# Export the main functions that match the original API
async def list_models() -> List[Dict[str, Any]]:
    """List available models from the provider."""
    return await default_provider.list_models()

async def complete_chat(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    top_p: float = 1.0,
    n: int = 1,
    user_id: str = None
) -> Dict[str, Any]:
    """Generate a chat completion (non-streaming)."""
    return await default_provider.complete_chat(
        model, messages, temperature, top_p, n, user_id
    )

async def stream_chat(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    top_p: float = 1.0,
    n: int = 1,
    user_id: str = None
) -> AsyncGenerator:
    """Generate a streaming chat completion."""
    return await default_provider.stream_chat(
        model, messages, temperature, top_p, n, user_id
    )

def get_embedding(text: str) -> List[float]:
    """Get embeddings for a single text."""
    return default_provider.get_embedding(text)

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for multiple texts."""
    return await default_provider.get_embeddings(texts)