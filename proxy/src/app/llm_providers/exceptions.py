"""
Exceptions for LLM provider module.

This module defines custom exceptions for the LLM provider module.
"""


class LLMProviderError(Exception):
    """Base exception for all LLM provider errors."""
    pass


class LLMAuthenticationError(LLMProviderError):
    """Exception raised when authentication with the LLM provider fails."""
    pass


class LLMRateLimitError(LLMProviderError):
    """Exception raised when the LLM provider rate limit is exceeded."""
    pass


class LLMConnectionError(LLMProviderError):
    """Exception raised when there's a connection error with the LLM provider."""
    pass


class LLMTimeoutError(LLMProviderError):
    """Exception raised when the request to the LLM provider times out."""
    pass


class LLMModelNotFoundError(LLMProviderError):
    """Exception raised when the requested model is not found."""
    pass


class LLMInvalidRequestError(LLMProviderError):
    """Exception raised when the request to the LLM provider is invalid."""
    pass