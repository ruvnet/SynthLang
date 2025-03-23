"""
LLM provider integration module.

This module provides functions for interacting with LLM providers
such as OpenAI to get chat completions and embeddings.
"""
import logging
import os
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable
import time
import httpx
from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI, AsyncOpenAI
from src.app.agents import registry
from src.app.config import MODEL_PROVIDER

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = None
async_client = None

# Load API key directly from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
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
    """Exception raised when the request to the LLM provider times out."""
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
        
    Raises:
        LLMAuthenticationError: If the API key is not set
    """
    global client
    if client is None:
        api_key = OPENAI_API_KEY
        if not api_key:
            logger.error("OPENAI_API_KEY is not set. Using environment variable is required.")
            raise LLMAuthenticationError("OPENAI_API_KEY environment variable is not set")
        client = OpenAI(api_key=api_key)
    return client


def get_async_openai_client():
    """
    Get or initialize the async OpenAI client.
    
    Returns:
        The async OpenAI client instance
        
    Raises:
        LLMAuthenticationError: If the API key is not set
    """
    global async_client
    if async_client is None:
        api_key = OPENAI_API_KEY
        if not api_key:
            logger.error("OPENAI_API_KEY is not set. Using environment variable is required.")
            raise LLMAuthenticationError("OPENAI_API_KEY environment variable is not set")
        async_client = AsyncOpenAI(api_key=api_key)
    return async_client


# Model-specific parameter handling
def get_model_params(model: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get model-specific parameters by filtering out incompatible parameters.
    
    Args:
        model: The model name
        params: The original parameters
        
    Returns:
        A dictionary of compatible parameters for the model
    """
    # Default parameters that work with all models
    result = {
        "model": model,
        "messages": params.get("messages", []),
        "stream": params.get("stream", False),
    }
    
    # Add user if provided
    if "user" in params:
        result["user"] = params["user"]
    
    # Model-specific parameter handling
    if "gpt-4o-mini" in model:
        # GPT-4o-mini doesn't support n, temperature, or top_p parameters
        logger.info(f"Using limited parameters for {model}")
    else:
        # Add optional parameters for other models
        if "temperature" in params:
            result["temperature"] = params["temperature"]
        if "top_p" in params:
            result["top_p"] = params["top_p"]
        if "n" in params:
            result["n"] = params["n"]
    
    logger.info(f"Using parameters for {model}: {result}")
    return result


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
                            "message": {
                                "role": "assistant",
                                "content": tool_response.get("content", "I processed your request but couldn't generate a response.")
                            },
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
            provider_model = "gpt-4o"  # Or appropriate GPT-4o model
        elif "gpt-4o-mini" in model:
            provider_model = "gpt-4o-mini"  # Use exact model name
        else:
            provider_model = "gpt-3.5-turbo"  # Default fallback
    
    logger.info(f"Calling LLM API with model {provider_model} for user {user_id}")
    
    try:
        # Get the async OpenAI client
        openai_client = get_async_openai_client()
        
        # Prepare parameters based on the model
        params = {
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": False,  # Non-streaming
            "user": user_id
        }
        
        # Get model-specific parameters
        model_params = get_model_params(provider_model, params)
        
        # Call the OpenAI API
        response = await openai_client.chat.completions.create(**model_params)
        
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
                            "message": {
                                "role": "assistant",
                                "content": tool_response.get("content", "I processed your request but couldn't generate a response.")
                            },
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
            provider_model = "gpt-4o"  # Or appropriate GPT-4o model
        elif "gpt-4o-mini" in model:
            provider_model = "gpt-4o-mini"  # Use exact model name
        else:
            provider_model = "gpt-3.5-turbo"  # Default fallback
    
    logger.info(f"Calling LLM API (streaming) with model {provider_model} for user {user_id}")
    
    try:
        # Get the async OpenAI client
        openai_client = get_async_openai_client()
        
        # Prepare parameters based on the model
        params = {
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": True,  # Streaming
            "user": user_id
        }
        
        # Get model-specific parameters
        model_params = get_model_params(provider_model, params)
        
        # Call the OpenAI API with streaming
        stream = await openai_client.chat.completions.create(**model_params)
        
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
        
        # Extract the embedding from the response
        embedding = response.data[0].embedding
        
        logger.info("OpenAI Embedding API call successful")
        return embedding
    except httpx.TimeoutException as e:
        # Handle timeout errors specifically
        logger.error(f"OpenAI Embedding API request timed out: {e}")
        raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"OpenAI Embedding API call failed: {e}")
        
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


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Call the OpenAI Embedding API to get embeddings for multiple texts.
    
    Args:
        texts: The texts to embed
        
    Returns:
        A list of embedding vectors
        
    Raises:
        LLMAuthenticationError: If authentication with the LLM provider fails
        LLMRateLimitError: If the LLM provider rate limit is exceeded
        LLMConnectionError: If there's a connection error with the LLM provider
        LLMTimeoutError: If the request to the LLM provider times out
        LLMModelNotFoundError: If the requested model is not found
        LLMInvalidRequestError: If the request to the LLM provider is invalid
        LLMProviderError: For other LLM provider errors
    """
    logger.info(f"Calling OpenAI Embedding API for {len(texts)} texts")
    
    # Process in batches to avoid rate limits
    batch_size = 100
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            # Get the OpenAI client
            openai_client = get_openai_client()
            
            # Call the OpenAI API
            response = openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=batch
            )
            
            # Extract the embeddings from the response
            batch_embeddings = [data.embedding for data in response.data]
            embeddings.extend(batch_embeddings)
            
            logger.info(f"OpenAI Embedding API call successful for batch {i//batch_size + 1}")
        except Exception as e:
            logger.error(f"OpenAI Embedding API call failed for batch {i//batch_size + 1}: {e}")
            raise
    
    return embeddings