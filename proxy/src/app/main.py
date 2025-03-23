"""
Main FastAPI application.

This module contains the FastAPI application and API endpoints.
"""
# Import path_fix first to ensure correct module resolution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import logging
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request, Response, Header
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import (
    ChatRequest,
    ChatResponse,
    ChatResponseChoice,
    Message,
    APIInfo,
    HealthCheck
)
from . import auth, cache, llm_provider, db
from .database import init_db
from .synthlang import is_synthlang_available
from .synthlang.endpoints import router as synthlang_router
from .openai.endpoints import router as openai_router
from .cache.endpoints import router as cache_router
from .agents.endpoints import router as tools_router
from .keywords.endpoints import router as keywords_router
from .config.keywords import initialize_from_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    
    This function is called when the application starts up and shuts down.
    It initializes the database and performs other startup/shutdown tasks.
    
    Args:
        app: The FastAPI application instance
    """
    # Startup logic
    logger.info("Initializing application...")
    
    # Check required environment variables
    from .config import OPENAI_API_KEY, DATABASE_URL, ENCRYPTION_KEY
    
    # Verify OpenAI API key is set
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable is not set. API calls will fail.")
        logger.error("Please set the OPENAI_API_KEY environment variable in the .env file.")
        # We don't raise an exception here to allow the app to start, but it will fail on API calls
    else:
        logger.info("OPENAI_API_KEY environment variable is set.")
    
    # Initialize the database
    db_initialized = await init_db()
    if db_initialized:
        logger.info("Database initialized successfully")
        
        # Initialize user roles from the database
        logger.info("Initializing user roles from the database...")
        await auth.init_user_roles()
        logger.info("User roles initialized successfully")
        
        # Load API keys from the database
        logger.info("Loading API keys from the database...")
        await auth.load_api_keys_from_db()
        logger.info("API keys loaded successfully")
    else:
        logger.warning("Database initialization failed, some features may not work correctly")
    
    # Initialize keyword detection system
    try:
        pattern_count = initialize_from_config()
        logger.info(f"Keyword detection system initialized with {pattern_count} patterns")
        
        # Import all tools to ensure they are registered
        from src.app.agents.tools.import_tools import import_all_tools
        tool_count = import_all_tools()
        logger.info(f"Imported {tool_count} tools")
    except Exception as e:
        logger.error(f"Error initializing keyword detection system: {e}")
    
    logger.info("Application initialization complete")
    
    yield  # This is where the application runs
    
    # Shutdown logic
    logger.info("Shutting down application...")
    # Add any cleanup tasks here
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="SynthLang Router API",
    description="A high-speed LLM router and proxy with SynthLang integration",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(synthlang_router)
app.include_router(openai_router)
app.include_router(cache_router)
app.include_router(tools_router)
app.include_router(keywords_router)


@app.get("/", response_model=APIInfo)
async def root():
    """
    Get basic API information.
    
    Returns:
        Basic information about the API
    """
    return {
        "name": "SynthLang Router API",
        "version": "0.1.0",
        "status": "operational",
        "documentation": "/docs"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Check the health of the API.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "synthlang_available": is_synthlang_available(),
        "version": "0.1.0"
    }


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def create_chat_completion(
    request: ChatRequest,
    authorization: str = Header(None)
):
    """
    Create a chat completion.
    
    Args:
        request: The chat completion request
        authorization: The Authorization header containing the API key
        
    Returns:
        The chat completion response
    """
    # Verify API key
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
    
    api_key = auth.verify_api_key(authorization)
    
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Log the request
    logger.info(f"Chat completion request from user {user_id} for model {request.model}")
    
    # Check for keyword patterns in the last user message
    from .middleware.keyword_detection import apply_keyword_detection
    keyword_response = await apply_keyword_detection(
        [msg.dict() for msg in request.messages], 
        user_id
    )
    
    if keyword_response:
        logger.info(f"Keyword detected in message from user {user_id}, using tool response")
        
        # Create a response with the tool's content
        response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": keyword_response.get("content", "I processed your request but couldn't generate a response.")
                    },
                    "finish_reason": "tool_invocation"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(keyword_response.get("content", "").split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + 
                                len(keyword_response.get("content", "").split())
            },
            # Include keyword detection information for debugging
            "debug": {
                "keyword_detection": True,
                "tool_used": keyword_response.get("tool", "unknown"),
                "pattern_matched": keyword_response.get("pattern", "unknown")
            }
        }
        
        # Save interaction to database
        await db.save_interaction(
            user_id, 
            request.model, 
            [msg.dict() for msg in request.messages], 
            keyword_response.get("content", ""), 
            cache_hit=False
        )
        
        # Return streaming response if requested
        if request.stream:
            async def yield_keyword_response():
                """Generate SSE events from the keyword response."""
                content = keyword_response.get("content", "")
                yield f"data: {content}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(yield_keyword_response(), media_type="text/event-stream")
        
        return response
    
    # 1. Compress user and system messages using SynthLang
    compressed_messages = []
    for msg in request.messages:
        if msg.role in ("user", "system"):
            # Use the new API for compression
            from .synthlang.api import synthlang_api
            compressed_content = synthlang_api.compress(msg.content)
            compressed_messages.append({"role": msg.role, "content": compressed_content})
        else:
            compressed_messages.append({"role": msg.role, "content": msg.content})
    
    # 2. Semantic cache lookup: embed last user message
    cache_key = cache.make_cache_key(compressed_messages, request.model)
    cached_response = cache.get_similar_response(cache_key)
    
    # If we have a cache hit, return the cached response
    if cached_response:
        logger.info(f"Cache hit for user {user_id} with model {request.model}")
        
        # Handle streaming for cache hits
        if request.stream:
            async def yield_cached():
                """Generate SSE events from the cached response."""
                yield f"data: {cached_response}\n\n"
                yield "data: [CACHE_END]\n\n"  # Signal end of cached stream
            
            # Save interaction to database
            await db.save_interaction(user_id, request.model, compressed_messages, cached_response, cache_hit=True)
            logger.info(f"Saved cache hit interaction to database for user {user_id}")
            
            return StreamingResponse(yield_cached(), media_type="text/event-stream")
        
        # Non-streaming cache hit
        # Create a response with the cached content
        response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": cached_response
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(cached_response.split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + len(cached_response.split())
            },
            # Include cache information for debugging
            "debug": {
                "cache_hit": True,
                "compressed_messages": compressed_messages,
                "decompressed_messages": None
            }
        }
        
        # Save interaction to database
        await db.save_interaction(user_id, request.model, compressed_messages, cached_response, cache_hit=True)
        logger.info(f"Saved cache hit interaction to database for user {user_id}")
        
        return response
    
    # 3. No cache hit: Call LLM provider
    # Prepare messages for LLM call by decompressing
    final_messages = []
    for msg in compressed_messages:
        if msg["role"] in ("user", "system"):
            # Use the new API for decompression
            from .synthlang.api import synthlang_api
            final_messages.append({"role": msg["role"], "content": synthlang_api.decompress(msg["content"])})
        else:
            final_messages.append(msg)
    
    try:
        # Call LLM provider
        if request.stream:
            # Handle streaming response
            response_iter = await llm_provider.stream_chat(
                model=request.model,
                messages=final_messages,
                temperature=request.temperature or 1.0,
                top_p=request.top_p or 1.0,
                n=request.n or 1,
                user_id=user_id
            )
            
            # Define a generator function to format the streaming response as SSE
            async def stream_generator():
                """Generate SSE events from the LLM streaming response."""
                full_response = ""
                # Iterate over the generator directly
                async for chunk in response_iter:
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        if 'delta' in chunk['choices'][0]:
                            content_piece = chunk['choices'][0]['delta'].get('content', '')
                            if content_piece:
                                full_response += content_piece
                                yield f"data: {content_piece}\n\n"
                
                # Signal end of stream
                yield "data: [DONE]\n\n"
                
                # Store the complete response in cache after streaming is done
                if cache_key and full_response:
                    cache.store(cache_key, full_response)
                    logger.info(f"Stored streamed response in cache for user {user_id} with model {request.model}")
                    
                    # Save interaction to database
                    await db.save_interaction(user_id, request.model, compressed_messages, full_response, cache_hit=False)
                    logger.info(f"Saved streamed LLM interaction to database for user {user_id}")
            
            # Return streaming response
            return StreamingResponse(
                stream_generator(),
                media_type="text/event-stream"
            )
        else:
            # Handle non-streaming response
            llm_response = await llm_provider.complete_chat(
                model=request.model,
                messages=final_messages,
                temperature=request.temperature or 1.0,
                top_p=request.top_p or 1.0,
                n=request.n or 1,
                user_id=user_id
            )
            
            # Extract assistant message
            assistant_msg = llm_response["choices"][0]["message"]["content"]
            
            # Store in cache
            if cache_key:
                cache.store(cache_key, assistant_msg)
                logger.info(f"Stored response in cache for user {user_id} with model {request.model}")
            
            # Save interaction to database
            await db.save_interaction(user_id, request.model, compressed_messages, assistant_msg, cache_hit=False)
            logger.info(f"Saved LLM interaction to database for user {user_id}")
            
            # Create response
            response = {
                "id": llm_response["id"],
                "object": "chat.completion",
                "created": llm_response["created"],
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": assistant_msg
                        },
                        "finish_reason": llm_response["choices"][0].get("finish_reason", "stop")
                    }
                ],
                "usage": llm_response.get("usage", {
                    "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                    "completion_tokens": len(assistant_msg.split()),
                    "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + len(assistant_msg.split())
                }),
                # Include debug information
                "debug": {
                    "cache_hit": False,
                    "compressed_messages": compressed_messages,
                    "decompressed_messages": None
                }
            }
            
            return response
    except Exception as e:
        logger.error(f"LLM provider call failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"LLM provider call failed: {str(e)}",
                    "type": "llm_error",
                    "code": 500
                }
            }
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions and return a standardized error response.
    
    Args:
        request: The request that caused the exception
        exc: The HTTP exception
        
    Returns:
        A JSON response with the error details
    """
    # Log the error
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    
    # If the exception already has a structured error detail, use it
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers
        )
    
    # Otherwise, create a structured error response
    error_response = {
        "error": {
            "message": str(exc.detail),
            "type": "api_error",
            "code": exc.status_code
        }
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=exc.headers
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions and return a standardized error response.
    
    Args:
        request: The request that caused the exception
        exc: The exception
        
    Returns:
        A JSON response with the error details
    """
    # Log the error
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    
    # Create a structured error response
    error_response = {
        "error": {
            "message": "An internal server error occurred",
            "type": "server_error",
            "code": 500
        }
    }
    
    return JSONResponse(
        status_code=500,
        content=error_response
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)