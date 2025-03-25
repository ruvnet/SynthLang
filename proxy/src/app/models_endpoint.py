"""
Models endpoint for the SynthLang Proxy API.

This module provides endpoints for retrieving available models.
"""
import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from . import auth
from .models import ModelInfo
from .config import DEFAULT_MODEL

# Configure logging
logger = logging.getLogger("app.models")

# Create router
router = APIRouter()

# Define available models
AVAILABLE_MODELS = [
    {
        "id": "gpt-4o-mini",
        "object": "model",
        "created": 1709006457,
        "owned_by": "synthlang",
        "permission": [],
        "root": "gpt-4o-mini",
        "parent": None,
        "is_default": True
    },
    {
        "id": "gpt-4o",
        "object": "model",
        "created": 1709006457,
        "owned_by": "synthlang",
        "permission": [],
        "root": "gpt-4o",
        "parent": None,
        "is_default": False
    },
    {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1677610602,
        "owned_by": "synthlang",
        "permission": [],
        "root": "gpt-3.5-turbo",
        "parent": None,
        "is_default": False
    },
    # Add Claude models
    {
        "id": "claude-3-opus",
        "object": "model",
        "created": 1709006457,
        "owned_by": "anthropic",
        "permission": [],
        "root": "claude-3-opus",
        "parent": None,
        "is_default": False
    },
    {
        "id": "claude-3-sonnet",
        "object": "model",
        "created": 1709006457,
        "owned_by": "anthropic",
        "permission": [],
        "root": "claude-3-sonnet",
        "parent": None,
        "is_default": False
    },
    {
        "id": "claude-3-haiku",
        "object": "model",
        "created": 1709006457,
        "owned_by": "anthropic",
        "permission": [],
        "root": "claude-3-haiku",
        "parent": None,
        "is_default": False
    },
    {
        "id": "claude-3.5-sonnet",
        "object": "model",
        "created": 1709006457,
        "owned_by": "anthropic",
        "permission": [],
        "root": "claude-3.5-sonnet",
        "parent": None,
        "is_default": False
    },
    {
        "id": "claude-3-7-sonnet-latest",
        "object": "model",
        "created": 1709006457,
        "owned_by": "anthropic",
        "permission": [],
        "root": "claude-3-7-sonnet-latest",
        "parent": None,
        "is_default": False
    }
]

# Define response model for models endpoint
class ModelsResponse(BaseModel):
    data: List[ModelInfo]
    default_model: Optional[str] = None

async def log_request_details(request: Request):
    """
    Log detailed information about the request.
    
    Args:
        request: The incoming request
    """
    # Get request headers (excluding sensitive information)
    headers = dict(request.headers)
    if "authorization" in headers:
        headers["authorization"] = "Bearer [REDACTED]"
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    # Try to get request body
    body = None
    try:
        body_bytes = await request.body()
        if body_bytes:
            body = json.loads(body_bytes.decode())
    except:
        body = "Could not parse request body"
    
    # Log request details
    logger.info(f"Request to {request.method} {request.url.path}")
    logger.info(f"Headers: {json.dumps(headers)}")
    logger.info(f"Query params: {json.dumps(query_params)}")
    if body:
        logger.info(f"Request body: {json.dumps(body) if isinstance(body, dict) else body}")

@router.get("/models", response_model=ModelsResponse)
async def list_models(request: Request):
    """
    Get a list of available models.
    
    Returns:
        A dictionary containing a list of available models
    """
    await log_request_details(request)
    
    # Add information about the default model
    response = {
        "data": AVAILABLE_MODELS,
        "default_model": DEFAULT_MODEL
    }
    
    logger.info(f"Returning models list with default model: {DEFAULT_MODEL}")
    return response

@router.get("/v1/models", response_model=ModelsResponse)
async def list_models_v1(request: Request):
    """
    Get a list of available models (v1 endpoint).
    
    Returns:
        A dictionary containing a list of available models
    """
    await log_request_details(request)
    
    # Add information about the default model
    response = {
        "data": AVAILABLE_MODELS,
        "default_model": DEFAULT_MODEL
    }
    
    logger.info(f"Returning models list with default model: {DEFAULT_MODEL}")
    return response