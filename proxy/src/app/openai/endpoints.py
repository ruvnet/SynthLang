"""
OpenAI-compatible API endpoints.

This module defines the FastAPI endpoints that are compatible with the OpenAI API.
"""
import logging
import time
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.app import auth, llm_provider
from src.app.models import (
    ChatRequest,
    ChatResponse,
    ChatResponseChoice,
    Message
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/v1", tags=["openai"])


def verify_auth(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify authorization header and return API key.
    
    Args:
        authorization: Authorization header
        
    Returns:
        API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Missing API key",
                    "type": "auth_error",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    return auth.verify_api_key(authorization)


@router.get("/models")
async def list_models(
    api_key: str = Depends(verify_auth)
):
    """
    List available models.
    
    Args:
        api_key: The API key
        
    Returns:
        List of available models
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Log the request
    logger.info(f"List models request from user {user_id}")
    
    # Get available models from LLM provider
    models = await llm_provider.list_models()
    
    # Format response in OpenAI format
    return {
        "object": "list",
        "data": [
            {
                "id": model["id"],
                "object": "model",
                "created": int(time.time()),
                "owned_by": model.get("owned_by", "unknown"),
                "permission": [],
                "root": model["id"],
                "parent": None
            }
            for model in models
        ]
    }


@router.post("/completions")
async def create_completion(
    request: ChatRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Create a completion (legacy endpoint).
    
    This endpoint is provided for compatibility with the OpenAI API.
    It converts the request to a chat completion format.
    
    Args:
        request: The completion request
        api_key: The API key
        
    Returns:
        The completion response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Log the request
    logger.info(f"Legacy completion request from user {user_id} for model {request.model}")
    
    # Convert to chat format if needed
    messages = request.messages
    if not messages:
        # If no messages provided, create a user message from the prompt
        messages = [Message(role="user", content=request.prompt if hasattr(request, "prompt") else "")]
    
    # Create a chat request
    chat_request = ChatRequest(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        top_p=request.top_p,
        n=request.n,
        max_tokens=request.max_tokens,
        presence_penalty=request.presence_penalty,
        frequency_penalty=request.frequency_penalty,
        logit_bias=request.logit_bias,
        user=request.user,
        stream=request.stream
    )
    
    # Call LLM provider
    if request.stream:
        # Handle streaming response
        response_iter = await llm_provider.stream_chat(
            model=request.model,
            messages=[msg.dict() for msg in chat_request.messages],
            temperature=chat_request.temperature or 1.0,
            top_p=chat_request.top_p or 1.0,
            n=chat_request.n or 1,
            user_id=user_id
        )
        
        # Define a generator function to format the streaming response
        async def stream_generator():
            """Generate streaming response chunks."""
            async for chunk in response_iter:
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        
        # Return streaming response
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream"
        )
    else:
        # Handle non-streaming response
        llm_response = await llm_provider.complete_chat(
            model=request.model,
            messages=[msg.dict() for msg in chat_request.messages],
            temperature=chat_request.temperature or 1.0,
            top_p=chat_request.top_p or 1.0,
            n=chat_request.n or 1,
            user_id=user_id
        )
        
        # Extract assistant message
        assistant_msg = llm_response["choices"][0]["message"]["content"]
        
        # Format response in OpenAI completions format
        return {
            "id": llm_response["id"].replace("chatcmpl", "cmpl"),
            "object": "text_completion",
            "created": llm_response["created"],
            "model": request.model,
            "choices": [
                {
                    "text": assistant_msg,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": llm_response["choices"][0].get("finish_reason", "stop")
                }
            ],
            "usage": llm_response.get("usage", {
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(assistant_msg.split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + len(assistant_msg.split())
            })
        }