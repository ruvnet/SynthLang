"""
Forgiving validation handler for FastAPI (fixed version).

This module provides enhanced error handling for validation errors with automatic correction
of common issues in API requests, but with minimal changes to the request body.
"""
import json
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Dict, Any, Optional

# Configure logging
logger = logging.getLogger("app.forgiving_validation")

class ForgivingValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware that attempts to fix common issues with API requests before validation.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request and attempt to fix common issues.
        
        Args:
            request: The incoming request
            call_next: The next middleware or endpoint handler
            
        Returns:
            The response from the next handler
        """
        # Only process POST requests to chat completions endpoints
        path = request.url.path
        if request.method == "POST" and ("/chat/completions" in path or "/v1/chat/completions" in path):
            # Try to read and fix the request body
            try:
                # Read the original body
                body_bytes = await request.body()
                
                # If body is empty, provide a default structure
                if not body_bytes:
                    logger.warning(f"Empty request body received for {path}, using default structure")
                    fixed_body = {
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                    # Create a modified request with the fixed body
                    request._body = json.dumps(fixed_body).encode()
                    return await call_next(request)
                
                # Try to parse as JSON
                try:
                    body = json.loads(body_bytes.decode())
                    
                    # Only apply minimal fixes to the body
                    fixed_body = await self._minimal_fix_request_body(body)
                    
                    if fixed_body != body:
                        logger.info(f"Fixed request body for {path}")
                        # Create a modified request with the fixed body
                        request._body = json.dumps(fixed_body).encode()
                
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in request body for {path}")
                    # If not valid JSON, we'll let the regular validation handle it
            
            except Exception as e:
                logger.error(f"Error in ForgivingValidationMiddleware: {e}")
                # Continue with the original request if there's an error
        
        # Process the request with the next handler
        return await call_next(request)
    
    async def _minimal_fix_request_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply minimal fixes to the request body to avoid breaking changes.
        
        Args:
            body: The original request body
            
        Returns:
            The fixed request body
        """
        fixed_body = body.copy()
        
        # Fix 1: Ensure model is present (only if completely missing)
        if "model" not in fixed_body:
            fixed_body["model"] = "gpt-4o-mini"
            logger.info("Added default model to request")
        
        # Fix 2: Ensure messages is present and valid
        if "messages" in fixed_body and isinstance(fixed_body["messages"], list):
            # Only fix messages that are clearly broken
            fixed_messages = []
            for i, msg in enumerate(fixed_body["messages"]):
                if not isinstance(msg, dict):
                    # Convert non-dict messages to dict
                    if isinstance(msg, str):
                        fixed_msg = {"role": "user", "content": msg}
                        logger.info(f"Converted string message at index {i} to dict")
                    else:
                        # Skip invalid messages
                        continue
                else:
                    fixed_msg = msg.copy()
                    # Only fix role if it's completely invalid
                    if "role" not in fixed_msg:
                        fixed_msg["role"] = "user"
                        logger.info(f"Added missing role in message at index {i}")
                    
                    # Only fix content if it's completely missing
                    if "content" not in fixed_msg:
                        fixed_msg["content"] = ""
                        logger.info(f"Added empty content to message at index {i}")
                
                fixed_messages.append(fixed_msg)
            
            fixed_body["messages"] = fixed_messages
        
        return fixed_body


async def forgiving_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with more forgiving behavior.
    
    Args:
        request: The request that caused the exception
        exc: The validation exception
        
    Returns:
        A JSON response with error information
    """
    # Get the raw request body
    raw_body = b""
    try:
        raw_body = await request.body()
    except Exception as e:
        logger.error(f"Error reading request body: {e}")
        raw_body = b"Could not read request body"
    
    # Try to parse the raw body as JSON
    try:
        body_json = json.loads(raw_body.decode())
    except Exception as e:
        logger.error(f"Error parsing request body as JSON: {e}")
        body_json = {"error": "Could not parse request body as JSON", "raw": raw_body.decode(errors='replace')}
    
    # Get request headers (excluding sensitive information)
    headers = dict(request.headers)
    if "authorization" in headers:
        headers["authorization"] = "Bearer [REDACTED]"
    
    # Log detailed information
    logger.error(f"Validation error for {request.method} {request.url.path}")
    logger.error(f"Request body: {body_json}")
    logger.error(f"Validation errors: {exc.errors()}")
    
    # Create a standard error response
    error_response = {
        "error": {
            "message": "Request validation error",
            "type": "validation_error",
            "code": 422,
            "detail": [
                {
                    "loc": error.get("loc", []),
                    "msg": error.get("msg", ""),
                    "type": error.get("type", "")
                } for error in exc.errors()
            ],
            "request_info": {
                "method": request.method,
                "url": str(request.url),
                "body": body_json
            }
        }
    }
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )