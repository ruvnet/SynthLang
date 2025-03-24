"""Local proxy server implementation for SynthLang."""
import os
import sys
from typing import Dict, Optional, Any, List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from synthlang.proxy.config import get_proxy_config, ProxyConfig
from synthlang.proxy.cache import SemanticCache
from synthlang.proxy.compression import compress_prompt, decompress_prompt
from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """Chat completion request model."""
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class TranslationRequest(BaseModel):
    """Translation request model."""
    source: str
    framework: str = "synthlang"


class CompressionRequest(BaseModel):
    """Compression request model."""
    text: str
    use_gzip: bool = False


class DecompressionRequest(BaseModel):
    """Decompression request model."""
    text: str


def create_app() -> FastAPI:
    """Create FastAPI application for proxy server.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title="SynthLang Proxy",
        description="Local proxy server for SynthLang",
        version="0.2.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize cache
    cache = SemanticCache()
    
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """Health check endpoint.
        
        Returns:
            Dict: Health status
        """
        return {
            "status": "ok",
            "version": "0.2.0",
            "cache_stats": cache.get_stats()
        }
    
    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatCompletionRequest) -> Dict[str, Any]:
        """Chat completions endpoint.
        
        Args:
            request: Chat completion request
            
        Returns:
            Dict: Chat completion response
        """
        try:
            # Check cache first if not streaming
            if not request.stream:
                cache_key = {
                    "type": "chat_completion",
                    "model": request.model,
                    "messages": [m.dict() for m in request.messages],
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens
                }
                
                cached_response = cache.get(cache_key)
                if cached_response:
                    logger.info(f"Cache hit for chat completion with model {request.model}")
                    return cached_response
            
            # If not in cache, use OpenAI API
            import dspy
            
            # Create language model
            lm = dspy.LM(model=request.model)
            
            # Format messages for DSPy
            messages = [{"role": m.role, "content": m.content} for m in request.messages]
            
            # Call the API
            response = lm.complete(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens or 1024
            )
            
            # Format response
            result = {
                "id": f"chatcmpl-{os.urandom(4).hex()}",
                "object": "chat.completion",
                "created": int(dspy.utils.time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": -1,  # Not available
                    "completion_tokens": -1,  # Not available
                    "total_tokens": -1  # Not available
                }
            }
            
            # Cache the result if not streaming
            if not request.stream:
                cache.set(cache_key, result)
            
            return result
        except Exception as e:
            logger.error(f"Error in chat completions: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/v1/translate")
    async def translate(request: TranslationRequest) -> Dict[str, Any]:
        """Translate text to SynthLang format.
        
        Args:
            request: Translation request
            
        Returns:
            Dict: Translation result
        """
        try:
            # Check cache first
            cache_key = {
                "type": "translate",
                "source": request.source,
                "framework": request.framework
            }
            
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit for translation to {request.framework}")
                return cached_response
            
            # If not in cache, use translator
            from synthlang.core.translator import FrameworkTranslator
            import dspy
            
            # Create language model and translator
            lm = dspy.LM()
            translator = FrameworkTranslator(lm)
            
            # Translate
            result = translator.translate(request.source)
            
            # Format response
            response = {
                "source": request.source,
                "target": result["target"],
                "framework": request.framework,
                "explanation": result.get("explanation", "")
            }
            
            # Cache the result
            cache.set(cache_key, response)
            
            return response
        except Exception as e:
            logger.error(f"Error in translation: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/v1/compress")
    async def compress(request: CompressionRequest) -> Dict[str, Any]:
        """Compress text using SynthLang compression.
        
        Args:
            request: Compression request
            
        Returns:
            Dict: Compression result
        """
        try:
            # Compress the text
            compressed = compress_prompt(request.text, request.use_gzip)
            
            # Calculate compression stats
            original_len = len(request.text)
            compressed_len = len(compressed)
            ratio = original_len / max(1, compressed_len)
            
            return {
                "original": request.text,
                "compressed": compressed,
                "original_length": original_len,
                "compressed_length": compressed_len,
                "compression_ratio": ratio,
                "method": "gzip" if request.use_gzip else "synthlang"
            }
        except Exception as e:
            logger.error(f"Error in compression: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/v1/decompress")
    async def decompress(request: DecompressionRequest) -> Dict[str, Any]:
        """Decompress SynthLang-compressed text.
        
        Args:
            request: Decompression request
            
        Returns:
            Dict: Decompression result
        """
        try:
            # Decompress the text
            decompressed = decompress_prompt(request.text)
            
            return {
                "compressed": request.text,
                "decompressed": decompressed,
                "compressed_length": len(request.text),
                "decompressed_length": len(decompressed)
            }
        except Exception as e:
            logger.error(f"Error in decompression: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/v1/clear-cache")
    async def clear_cache() -> Dict[str, Any]:
        """Clear the semantic cache.
        
        Returns:
            Dict: Clear cache result
        """
        try:
            count = cache.clear()
            return {
                "status": "success",
                "cleared_entries": count
            }
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app


def start_server(
    host: Optional[str] = None,
    port: Optional[int] = None,
    log_level: str = "info",
    reload: bool = False
) -> None:
    """Start the proxy server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        log_level: Logging level
        reload: Whether to enable auto-reload
    """
    config = get_proxy_config()
    
    server_host = host or config.host
    server_port = port or config.port
    
    logger.info(f"Starting SynthLang Proxy server on {server_host}:{server_port}")
    
    uvicorn.run(
        "synthlang.proxy.server:create_app",
        factory=True,
        host=server_host,
        port=server_port,
        log_level=log_level,
        reload=reload
    )