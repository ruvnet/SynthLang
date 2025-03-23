"""
SynthLang API endpoints.

This module defines the FastAPI endpoints for SynthLang functionality.
"""
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.app import auth
from src.app.synthlang.api import synthlang_api
from src.app.synthlang.models import (
    TranslateRequest, TranslateResponse,
    GenerateRequest, GenerateResponse,
    OptimizeRequest, OptimizeResponse,
    EvolveRequest, EvolveResponse,
    ClassifyRequest, ClassifyResponse,
    SavePromptRequest, SavePromptResponse,
    LoadPromptRequest, LoadPromptResponse,
    ListPromptsResponse,
    DeletePromptRequest, DeletePromptResponse,
    ComparePromptsRequest, ComparePromptsResponse
)
from src.app.synthlang.utils import (
    get_dspy_lm,
    format_synthlang_response
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/v1/synthlang", tags=["synthlang"])


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def get_version() -> str:
    """Get API version."""
    return "1.0"


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
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    return auth.verify_api_key(authorization)