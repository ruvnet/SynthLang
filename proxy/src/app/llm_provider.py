"""
LLM provider integration module.

This module provides functions for interacting with LLM providers
such as OpenAI to get chat completions and embeddings.
"""
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable
import time
import httpx

from openai import OpenAI, AsyncOpenAI
from src.app.agents import registry
from src.app.config import OPENAI_API_KEY, MODEL_PROVIDER

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = None
async_client = None


# Custom exception classes for more granular error handling
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
    """Exception raised when a request to the LLM provider times out."""
    pass


class LLMModelNotFoundError(LLMProviderError):
    """Exception raised when the requested model is not found."""
    pass


class LLMInvalidRequestError(LLMProviderError):
    """Exception raised when the request to the LLM provider is invalid."""
    pass


def get_openai_client():
    """
    Get or initialize the OpenAI client.
    
    Returns:
        The OpenAI client instance
    """
    global client
    if client is None:
        api_key = OPENAI_API_KEY or "dummy_key_for_testing"
        client = OpenAI(api_key=api_key)
    return client


def get_async_openai_client():
    """
    Get or initialize the async OpenAI client.
    
    Returns:
        The async OpenAI client instance
    """
    global async_client
    if async_client is None:
        api_key = OPENAI_API_KEY or "dummy_key_for_testing"
        async_client = AsyncOpenAI(api_key=api_key)
    return async_client


async def complete_chat(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    top_p: float = 1.0,
    n: int = 1,
    user_id: str = None
) -> Dict[str, Any]:
    """
    Call the OpenAI ChatCompletion API (non-streaming) or invokes tool.
    
    Args:
        model: The model to use (will be mapped to appropriate provider model)
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        user_id: A unique identifier for the end-user
        
    Returns:
        The raw response from the OpenAI API or tool invocation
        
    Raises:
        LLMAuthenticationError: If authentication with the LLM provider fails
        LLMRateLimitError: If the LLM provider rate limit is exceeded
        LLMConnectionError: If there's a connection error with the LLM provider
        LLMTimeoutError: If the request to the LLM provider times out
        LLMModelNotFoundError: If the requested model is not found
        LLMInvalidRequestError: If the request to the LLM provider is invalid
        LLMProviderError: For other LLM provider errors
    """
    # Special case for search-preview models - invoke web search tool
    if "search-preview" in model:
        web_search_tool = registry.get_tool("web_search")
        if web_search_tool:
            logger.info(f"Invoking web_search tool for user {user_id}")
            try:
                tool_response = web_search_tool(user_message=messages[-1]["content"])
                logger.info(f"Web search tool invocation successful for user {user_id}")
                
                # Format the response to match OpenAI API format
                return {
                    "id": f"chatcmpl-tool-{model}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "message": tool_response,
                            "finish_reason": "tool_invocation"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": sum(len(msg["content"].split()) for msg in messages),
                        "completion_tokens": len(tool_response.get("content", "").split()),
                        "total_tokens": sum(len(msg["content"].split()) for msg in messages) + 
                                        len(tool_response.get("content", "").split())
                    }
                }
            except Exception as e:
                logger.error(f"Web search tool invocation failed: {e}")
                raise LLMProviderError(f"Web search tool invocation failed: {str(e)}")
        else:
            logger.warning("Web search tool not found in registry.")
    
    # Use MODEL_PROVIDER for model routing if available
    provider_model = model
    if model in MODEL_PROVIDER:
        provider = MODEL_PROVIDER[model]
        logger.info(f"Routing model {model} to provider {provider}")
    else:
        # Basic model routing as fallback
        if "gpt-4o" in model:
            provider_model = "gpt-4o-search-preview"  # Or appropriate GPT-4o model
        else:
            provider_model = "o3-mini"  # Or appropriate o3-mini model
    
    logger.info(f"Calling LLM API with model {provider_model} for user {user_id}")
    
    try:
        # Get the async OpenAI client
        openai_client = get_async_openai_client()
        
        # Call the OpenAI API
        response = await openai_client.chat.completions.create(
            model=provider_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=False,  # Non-streaming
            user=user_id
        )
        
        # Convert the response to a dictionary
        response_dict = {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    },
                    "finish_reason": choice.finish_reason
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
        
        logger.info(f"LLM API call successful for user {user_id}")
        return response_dict
    except httpx.TimeoutException as e:
        # Handle timeout errors specifically
        logger.error(f"LLM API request timed out: {e}")
        raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"LLM API call failed: {e}")
        
        # Classify the error based on the error message
        if "authentication" in error_msg or "auth" in error_msg or "invalid api key" in error_msg:
            raise LLMAuthenticationError(f"Authentication with LLM provider failed: {str(e)}")
        elif "rate limit" in error_msg or "ratelimit" in error_msg:
            raise LLMRateLimitError(f"LLM provider rate limit exceeded: {str(e)}")
        elif "connection" in error_msg or "network" in error_msg:
            raise LLMConnectionError(f"Connection error with LLM provider: {str(e)}")
        elif "timeout" in error_msg:
            raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
        elif "model not found" in error_msg or "model_not_found" in error_msg:
            raise LLMModelNotFoundError(f"Model {provider_model} not found: {str(e)}")
        elif "invalid request" in error_msg or "invalid_request" in error_msg:
            raise LLMInvalidRequestError(f"Invalid request to LLM provider: {str(e)}")
        else:
            raise LLMProviderError(f"LLM provider error: {str(e)}")


async def stream_chat(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    top_p: float = 1.0,
    n: int = 1,
    user_id: str = None
) -> AsyncGenerator:
    """
    Call the OpenAI ChatCompletion API (streaming) or invokes tool (non-streaming for now).
    
    Args:
        model: The model to use (will be mapped to appropriate provider model)
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        user_id: A unique identifier for the end-user
        
    Returns:
        An async generator that yields chunks from the streaming response
        
    Raises:
        LLMAuthenticationError: If authentication with the LLM provider fails
        LLMRateLimitError: If the LLM provider rate limit is exceeded
        LLMConnectionError: If there's a connection error with the LLM provider
        LLMTimeoutError: If the request to the LLM provider times out
        LLMModelNotFoundError: If the requested model is not found
        LLMInvalidRequestError: If the request to the LLM provider is invalid
        LLMProviderError: For other LLM provider errors
    """
    # Special case for search-preview models - invoke web search tool
    if "search-preview" in model:
        web_search_tool = registry.get_tool("web_search")
        if web_search_tool:
            logger.info(f"Invoking web_search tool (non-streaming) for user {user_id}")
            try:
                tool_response = web_search_tool(user_message=messages[-1]["content"])
                logger.info(f"Web search tool invocation successful for user {user_id}")
                
                # Format the response to match OpenAI API format
                response = {
                    "id": f"chatcmpl-tool-{model}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "message": tool_response,
                            "finish_reason": "tool_invocation"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": sum(len(msg["content"].split()) for msg in messages),
                        "completion_tokens": len(tool_response.get("content", "").split()),
                        "total_tokens": sum(len(msg["content"].split()) for msg in messages) + 
                                        len(tool_response.get("content", "").split())
                    }
                }
                
                # Convert the non-streaming response to a streaming format
                async def stream_tool_response():
                    # First yield the content as a single chunk
                    yield {
                        "id": response["id"],
                        "object": "chat.completion.chunk",
                        "created": response["created"],
                        "model": response["model"],
                        "choices": [
                            {
                                "index": 0,
                                "delta": {
                                    "content": response["choices"][0]["message"]["content"]
                                },
                                "finish_reason": response["choices"][0]["finish_reason"]
                            }
                        ]
                    }
                
                return stream_tool_response()
            except Exception as e:
                logger.error(f"Web search tool invocation failed: {e}")
                raise LLMProviderError(f"Web search tool invocation failed: {str(e)}")
        else:
            logger.warning("Web search tool not found in registry.")
    
    # Use MODEL_PROVIDER for model routing if available
    provider_model = model
    if model in MODEL_PROVIDER:
        provider = MODEL_PROVIDER[model]
        logger.info(f"Routing model {model} to provider {provider}")
    else:
        # Basic model routing as fallback
        if "gpt-4o" in model:
            provider_model = "gpt-4o-search-preview"  # Or appropriate GPT-4o model
        else:
            provider_model = "o3-mini"  # Or appropriate o3-mini model
    
    logger.info(f"Calling LLM API (streaming) with model {provider_model} for user {user_id}")
    
    try:
        # Get the async OpenAI client
        openai_client = get_async_openai_client()
        
        # Call the OpenAI API with streaming
        stream = await openai_client.chat.completions.create(
            model=provider_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=True,  # Streaming
            user=user_id
        )
        
        async def stream_generator():
            """Yield chunks from the streaming response."""
            async for chunk in stream:
                # Convert the chunk to a dictionary format
                chunk_dict = {
                    "id": chunk.id,
                    "object": chunk.object,
                    "created": chunk.created,
                    "model": chunk.model,
                    "choices": [
                        {
                            "index": choice.index,
                            "delta": {
                                "content": choice.delta.content or ""
                            },
                            "finish_reason": choice.finish_reason
                        }
                        for choice in chunk.choices
                    ]
                }
                yield chunk_dict
        
        logger.info(f"LLM API streaming call initiated for user {user_id}")
        return stream_generator()
    except httpx.TimeoutException as e:
        # Handle timeout errors specifically
        logger.error(f"LLM API streaming request timed out: {e}")
        raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"LLM API streaming call failed: {e}")
        
        # Classify the error based on the error message
        if "authentication" in error_msg or "auth" in error_msg or "invalid api key" in error_msg:
            raise LLMAuthenticationError(f"Authentication with LLM provider failed: {str(e)}")
        elif "rate limit" in error_msg or "ratelimit" in error_msg:
            raise LLMRateLimitError(f"LLM provider rate limit exceeded: {str(e)}")
        elif "connection" in error_msg or "network" in error_msg:
            raise LLMConnectionError(f"Connection error with LLM provider: {str(e)}")
        elif "timeout" in error_msg:
            raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
        elif "model not found" in error_msg or "model_not_found" in error_msg:
            raise LLMModelNotFoundError(f"Model {provider_model} not found: {str(e)}")
        elif "invalid request" in error_msg or "invalid_request" in error_msg:
            raise LLMInvalidRequestError(f"Invalid request to LLM provider: {str(e)}")
        else:
            raise LLMProviderError(f"LLM provider error: {str(e)}")


def get_embedding(text: str) -> List[float]:
    """
    Call the OpenAI Embedding API to get embeddings for text.
    
    Args:
        text: The text to embed
        
    Returns:
        The embedding vector as a list of floats
        
    Raises:
        LLMAuthenticationError: If authentication with the LLM provider fails
        LLMRateLimitError: If the LLM provider rate limit is exceeded
        LLMConnectionError: If there's a connection error with the LLM provider
        LLMTimeoutError: If the request to the LLM provider times out
        LLMModelNotFoundError: If the requested model is not found
        LLMInvalidRequestError: If the request to the LLM provider is invalid
        LLMProviderError: For other LLM provider errors
    """
    logger.info("Calling OpenAI Embedding API")
    
    try:
        # Get the OpenAI client
        openai_client = get_openai_client()
        
        # Call the OpenAI API
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        
        # Extract the embedding
        embedding = response.data[0].embedding
        logger.info("Embedding API call successful")
        return embedding
    except httpx.TimeoutException as e:
        # Handle timeout errors specifically
        logger.error(f"Embedding API request timed out: {e}")
        raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Embedding API call failed: {e}")
        
        # Classify the error based on the error message
        if "authentication" in error_msg or "auth" in error_msg or "invalid api key" in error_msg:
            raise LLMAuthenticationError(f"Authentication with LLM provider failed: {str(e)}")
        elif "rate limit" in error_msg or "ratelimit" in error_msg:
            raise LLMRateLimitError(f"LLM provider rate limit exceeded: {str(e)}")
        elif "connection" in error_msg or "network" in error_msg:
            raise LLMConnectionError(f"Connection error with LLM provider: {str(e)}")
        elif "timeout" in error_msg:
            raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
        elif "model not found" in error_msg or "model_not_found" in error_msg:
            raise LLMModelNotFoundError(f"Model text-embedding-ada-002 not found: {str(e)}")
        elif "invalid request" in error_msg or "invalid_request" in error_msg:
            raise LLMInvalidRequestError(f"Invalid request to LLM provider: {str(e)}")
        else:
            raise LLMProviderError(f"LLM provider error: {str(e)}")