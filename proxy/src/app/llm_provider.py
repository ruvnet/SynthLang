"""
LLM provider integration module.

This module provides functions for interacting with LLM providers
such as OpenAI to get chat completions and embeddings.
It's designed to be modular and extensible to support multiple providers.

This is a compatibility layer that re-exports the functions from the
llm_providers package to maintain backward compatibility.
"""
import logging
from typing import Dict, Any, List, AsyncGenerator

from .llm_providers import (
    complete_chat,
    stream_chat,
    get_embedding,
    get_embeddings,
    list_models,
    LLMProviderError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMModelNotFoundError,
    LLMInvalidRequestError
)

# Configure logging
logger = logging.getLogger(__name__)

# Re-export the functions and classes
__all__ = [
    "complete_chat",
    "stream_chat",
    "get_embedding",
    "get_embeddings",
    "list_models",
    "LLMProviderError",
    "LLMAuthenticationError",
    "LLMRateLimitError",
    "LLMConnectionError",
    "LLMTimeoutError",
    "LLMModelNotFoundError",
    "LLMInvalidRequestError"
]
