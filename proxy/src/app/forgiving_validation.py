"""
Forgiving validation handler for FastAPI.

This module provides enhanced error handling for validation errors with automatic correction
of common issues in API requests.
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
                    
                    # Apply fixes to the body
                    fixed_body = await self._fix_request_body(body)
                    
                    if fixed_body != body:
                        logger.info(f"Fixed request body for {path}")
                        # Create a modified request with the fixed body
                        request._body = json.dumps(fixed_body).encode()
                
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in request body for {path}")
                    # If not valid JSON, try to create a basic structure
                    content = body_bytes.decode(errors='replace')
                    fixed_body = {
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": content}]
                    }
                    # Create a modified request with the fixed body
                    request._body = json.dumps(fixed_body).encode()
                    logger.info(f"Created basic request structure from non-JSON content for {path}")
            
            except Exception as e:
                logger.error(f"Error in ForgivingValidationMiddleware: {e}")
                # Continue with the original request if there's an error
        
        # Process the request with the next handler
        return await call_next(request)
    
    async def _fix_request_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fix common issues in the request body.
        
        Args:
            body: The original request body
            
        Returns:
            The fixed request body
        """
        fixed_body = body.copy()
        
        # Fix 1: Ensure model is present
        if "model" not in fixed_body or not fixed_body["model"]:
            fixed_body["model"] = "gpt-4o-mini"
            logger.info("Added default model to request")
        
        # Fix 2: Ensure messages is present and valid
        if "messages" not in fixed_body or not isinstance(fixed_body["messages"], list):
            # If no messages, create a default one
            fixed_body["messages"] = [{"role": "user", "content": "Hello"}]
            logger.info("Added default messages to request")
        else:
            # Ensure each message has role and content
            fixed_messages = []
            for i, msg in enumerate(fixed_body["messages"]):
                if not isinstance(msg, dict):
                    # Convert non-dict messages to dict
                    if isinstance(msg, str):
                        fixed_msg = {"role": "user", "content": msg}
                    else:
                        fixed_msg = {"role": "user", "content": str(msg)}
                    logger.info(f"Converted non-dict message at index {i} to dict")
                else:
                    fixed_msg = msg.copy()
                    # Ensure role is present and valid
                    if "role" not in fixed_msg or fixed_msg["role"] not in ["system", "user", "assistant"]:
                        fixed_msg["role"] = "user"
                        logger.info(f"Fixed invalid role in message at index {i}")
                    
                    # Ensure content is present and is a string
                    if "content" not in fixed_msg:
                        fixed_msg["content"] = ""
                        logger.info(f"Added empty content to message at index {i}")
                    elif not isinstance(fixed_msg["content"], str):
                        fixed_msg["content"] = str(fixed_msg["content"])
                        logger.info(f"Converted non-string content to string in message at index {i}")
                
                fixed_messages.append(fixed_msg)
            
            fixed_body["messages"] = fixed_messages
        
        # Fix 3: Ensure temperature is valid
        if "temperature" in fixed_body and fixed_body["temperature"] is not None:
            try:
                temp = float(fixed_body["temperature"])
                if temp < 0:
                    fixed_body["temperature"] = 0
                    logger.info("Fixed negative temperature value")
                elif temp > 2:
                    fixed_body["temperature"] = 2
                    logger.info("Fixed temperature value > 2")
            except (ValueError, TypeError):
                fixed_body["temperature"] = 0.7
                logger.info("Fixed invalid temperature value")
        
        # Fix 4: Ensure top_p is valid
        if "top_p" in fixed_body and fixed_body["top_p"] is not None:
            try:
                top_p = float(fixed_body["top_p"])
                if top_p < 0:
                    fixed_body["top_p"] = 0
                    logger.info("Fixed negative top_p value")
                elif top_p > 1:
                    fixed_body["top_p"] = 1
                    logger.info("Fixed top_p value > 1")
            except (ValueError, TypeError):
                fixed_body["top_p"] = 1.0
                logger.info("Fixed invalid top_p value")
        
        # Fix 5: Ensure n is valid
        if "n" in fixed_body and fixed_body["n"] is not None:
            try:
                n = int(fixed_body["n"])
                if n < 1:
                    fixed_body["n"] = 1
                    logger.info("Fixed n value < 1")
            except (ValueError, TypeError):
                fixed_body["n"] = 1
                logger.info("Fixed invalid n value")
        
        return fixed_body


async def forgiving_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with more forgiving behavior.
    
    Args:
        request: The request that caused the exception
        exc: The validation exception
        
    Returns:
        A JSON response with error information or a fixed request
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
    
    # Check if this is a chat completions endpoint
    path = request.url.path
    if request.method == "POST" and ("/chat/completions" in path or "/v1/chat/completions" in path):
        # Try to create a valid request from the invalid one
        try:
            fixed_body = {}
            
            # Add default model if missing
            fixed_body["model"] = "gpt-4o-mini"
            
            # Extract any messages or create default ones
            if isinstance(body_json, dict) and "messages" in body_json and isinstance(body_json["messages"], list):
                # Fix messages
                fixed_messages = []
                for msg in body_json["messages"]:
                    if isinstance(msg, dict):
                        fixed_msg = {}
                        # Set role
                        if "role" in msg and msg["role"] in ["system", "user", "assistant"]:
                            fixed_msg["role"] = msg["role"]
                        else:
                            fixed_msg["role"] = "user"
                        
                        # Set content
                        if "content" in msg and isinstance(msg["content"], str):
                            fixed_msg["content"] = msg["content"]
                        else:
                            fixed_msg["content"] = str(msg.get("content", ""))
                        
                        fixed_messages.append(fixed_msg)
                    elif isinstance(msg, str):
                        # Convert string messages to user messages
                        fixed_messages.append({"role": "user", "content": msg})
            else:
                # Create a default message
                content = str(body_json) if isinstance(body_json, (str, dict)) else "Hello"
                fixed_messages = [{"role": "user", "content": content}]
            
            fixed_body["messages"] = fixed_messages
            
            # Add other parameters with defaults
            fixed_body["stream"] = body_json.get("stream", False) if isinstance(body_json, dict) else False
            fixed_body["temperature"] = 0.7
            fixed_body["top_p"] = 1.0
            fixed_body["n"] = 1
            
            logger.info(f"Created fixed request body: {fixed_body}")
            
            # Return a success response with the fixed body
            error_response = {
                "error": {
                    "message": "Request validation error, but we fixed it for you",
                    "type": "validation_error_fixed",
                    "code": 200,
                    "original_errors": [
                        {
                            "loc": error.get("loc", []),
                            "msg": error.get("msg", ""),
                            "type": error.get("type", "")
                        } for error in exc.errors()
                    ],
                    "fixed_request": fixed_body
                }
            }
            
            return JSONResponse(
                status_code=200,
                content=error_response
            )
            
        except Exception as e:
            logger.error(f"Error creating fixed request: {e}")
    
    # If we couldn't fix it or it's not a chat completions endpoint, return the standard error
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
                "body": body_json,
                "headers": headers
            }
        }
    }
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )