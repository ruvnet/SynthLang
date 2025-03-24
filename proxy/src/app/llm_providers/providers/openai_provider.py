"""
OpenAI provider implementation.

This module provides an implementation of the BaseLLMProvider interface
for the OpenAI API.
"""
import logging
import os
import time
import httpx
from typing import List, Dict, Any, AsyncGenerator

from openai import OpenAI, AsyncOpenAI

from ..base import BaseLLMProvider
from ..exceptions import (
    LLMProviderError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMModelNotFoundError,
    LLMInvalidRequestError
)
from src.app.agents import registry
from src.app.config import MODEL_PROVIDER

# Configure logging
logger = logging.getLogger(__name__)

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI implementation of the LLM provider interface.
    """
    
    def __init__(self):
        """Initialize the OpenAI provider."""
        self.client = None
        self.async_client = None
    
    def get_openai_client(self):
        """
        Get or initialize the OpenAI client.
        
        Returns:
            The OpenAI client instance
            
        Raises:
            LLMAuthenticationError: If the API key is not set
        """
        if self.client is None:
            api_key = OPENAI_API_KEY
            if not api_key:
                logger.error("OPENAI_API_KEY is not set. Using environment variable is required.")
                raise LLMAuthenticationError("OPENAI_API_KEY environment variable is not set")
            self.client = OpenAI(api_key=api_key)
        return self.client
    
    def get_async_openai_client(self):
        """
        Get or initialize the async OpenAI client.
        
        Returns:
            The async OpenAI client instance
            
        Raises:
            LLMAuthenticationError: If the API key is not set
        """
        if self.async_client is None:
            api_key = OPENAI_API_KEY
            if not api_key:
                logger.error("OPENAI_API_KEY is not set. Using environment variable is required.")
                raise LLMAuthenticationError("OPENAI_API_KEY environment variable is not set")
            self.async_client = AsyncOpenAI(api_key=api_key)
        return self.async_client
    
    def get_model_params(self, model: str, params: Dict[str, Any]) -> Dict[str, Any]:
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
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models from the OpenAI API.
        
        Returns:
            A list of model information dictionaries
            
        Raises:
            LLMAuthenticationError: If authentication with the LLM provider fails
            LLMConnectionError: If there's a connection error with the LLM provider
            LLMTimeoutError: If the request to the LLM provider times out
            LLMProviderError: For other LLM provider errors
        """
        try:
            # Get the async OpenAI client
            openai_client = self.get_async_openai_client()
            
            # Call the OpenAI API to list models
            response = await openai_client.models.list()
            
            # Convert the response to a list of dictionaries
            models = [
                {
                    "id": model.id,
                    "object": model.object,
                    "created": model.created,
                    "owned_by": model.owned_by
                }
                for model in response.data
            ]
            
            # Add SynthLang-specific models
            synthlang_models = [
                {
                    "id": "synthlang-translate",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "synthlang"
                },
                {
                    "id": "synthlang-generate",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "synthlang"
                },
                {
                    "id": "synthlang-optimize",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "synthlang"
                },
                {
                    "id": "synthlang-evolve",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "synthlang"
                },
                {
                    "id": "synthlang-classify",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "synthlang"
                }
            ]
            
            # Combine OpenAI and SynthLang models
            all_models = models + synthlang_models
            
            logger.info(f"Retrieved {len(all_models)} models")
            return all_models
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
            elif "connection" in error_msg or "network" in error_msg:
                raise LLMConnectionError(f"Connection error with LLM provider: {str(e)}")
            elif "timeout" in error_msg:
                raise LLMTimeoutError(f"Request to LLM provider timed out: {str(e)}")
            else:
                raise LLMProviderError(f"LLM provider error: {str(e)}")
    
    async def complete_chat(
        self,
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
            openai_client = self.get_async_openai_client()
            
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
            model_params = self.get_model_params(provider_model, params)
            
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
        self,
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
            openai_client = self.get_async_openai_client()
            
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
            model_params = self.get_model_params(provider_model, params)
            
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
    
    def get_embedding(self, text: str) -> List[float]:
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
            LLMProviderError: For other LLM provider errors
        """
        try:
            # Get the OpenAI client
            openai_client = self.get_openai_client()
            
            # Call the OpenAI API
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            
            # Extract the embedding
            embedding = response.data[0].embedding
            
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
            else:
                raise LLMProviderError(f"LLM provider error: {str(e)}")
    
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Call the OpenAI Embedding API to get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            LLMAuthenticationError: If authentication with the LLM provider fails
            LLMRateLimitError: If the LLM provider rate limit is exceeded
            LLMConnectionError: If there's a connection error with the LLM provider
            LLMTimeoutError: If the request to the LLM provider times out
            LLMProviderError: For other LLM provider errors
        """
        try:
            # Get the async OpenAI client
            openai_client = self.get_async_openai_client()
            
            # Call the OpenAI API
            response = await openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            # Extract the embeddings
            embeddings = [data.embedding for data in response.data]
            
            return embeddings
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
            else:
                raise LLMProviderError(f"LLM provider error: {str(e)}")