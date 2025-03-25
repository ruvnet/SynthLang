"""
Validation error handler for FastAPI.

This module provides enhanced error handling for validation errors (422 Unprocessable Entity).
"""
import json
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Configure logging
logger = logging.getLogger("app.validation")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors (422 Unprocessable Entity) with detailed debugging information.
    
    Args:
        request: The request that caused the exception
        exc: The validation exception
        
    Returns:
        A JSON response with detailed error information
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
    
    # Create detailed error response
    error_detail = []
    for error in exc.errors():
        error_detail.append({
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    # Log detailed information
    logger.error(f"Validation error for {request.method} {request.url.path}")
    logger.error(f"Request body: {body_json}")
    logger.error(f"Validation errors: {error_detail}")
    
    error_response = {
        "error": {
            "message": "Request validation error",
            "type": "validation_error",
            "code": 422,
            "detail": error_detail,
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