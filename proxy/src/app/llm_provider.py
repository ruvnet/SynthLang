"""
LLM provider integration module.

This module provides functions for interacting with LLM providers
such as OpenAI to get chat completions and embeddings.
"""
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable

from openai import OpenAI, AsyncOpenAI
from app.agents import registry
from app.config import OPENAI_API_KEY, MODEL_PROVIDER

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = None
async_client = None


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
        Exception: If the API call fails
    """
    # Special case for search-preview models - invoke web search tool
    if "search-preview" in model:
        web_search_tool = registry.get_tool("web_search")
        if web_search_tool:
            logger.info(f"Invoking web_search tool for user {user_id}")
            tool_response = web_search_tool(user_message=messages[-1]["content"])
            logger.info(f"Web search tool invocation successful for user {user_id}")
            
            # Format the response to match OpenAI API format
            return {
                "id": f"chatcmpl-tool-{model}",
                "object": "chat.completion",
                "created": int(__import__('time').time()),
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
    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        raise  # Re-raise exception for handling in main.py


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
        Exception: If the API call fails
    """
    # Special case for search-preview models - invoke web search tool
    if "search-preview" in model:
        web_search_tool = registry.get_tool("web_search")
        if web_search_tool:
            logger.info(f"Invoking web_search tool (non-streaming) for user {user_id}")
            tool_response = web_search_tool(user_message=messages[-1]["content"])
            logger.info(f"Web search tool invocation successful for user {user_id}")
            
            # Format the response to match OpenAI API format
            response = {
                "id": f"chatcmpl-tool-{model}",
                "object": "chat.completion",
                "created": int(__import__('time').time()),
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
            
            # For now, return a non-streaming response for tool invocation
            # In the future, implement proper streaming for tool responses
            return response
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
    except Exception as e:
        logger.error(f"LLM API streaming call failed: {e}")
        raise  # Re-raise exception for handling in main.py


def get_embedding(text: str) -> List[float]:
    """
    Call the OpenAI Embedding API to get embeddings for text.
    
    Args:
        text: The text to embed
        
    Returns:
        The embedding vector as a list of floats
        
    Raises:
        Exception: If the API call fails
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
    except Exception as e:
        logger.error(f"Embedding API call failed: {e}")
        raise  # Re-raise exception for handling