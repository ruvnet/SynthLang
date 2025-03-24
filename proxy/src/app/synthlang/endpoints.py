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


@router.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Translate natural language to SynthLang format.
    
    Args:
        request: The translation request
        api_key: The API key
        
    Returns:
        The translation response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Translation request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.translate(request.text, request.instructions)
    
    # Format response
    return {
        "source": result.get("source", request.text),
        "target": result.get("target", ""),
        "explanation": result.get("explanation", ""),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Generate a system prompt from task description.
    
    Args:
        request: The generation request
        api_key: The API key
        
    Returns:
        The generation response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Generation request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.generate(request.task_description)
    
    # Format response
    return {
        "prompt": result.get("prompt", ""),
        "rationale": result.get("rationale", ""),
        "metadata": result.get("metadata", {}),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(
    request: OptimizeRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Optimize a prompt for clarity, specificity, and efficiency.
    
    Args:
        request: The optimization request
        api_key: The API key
        
    Returns:
        The optimization response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "premium")
    
    # Log the request
    logger.info(f"Optimization request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.optimize(request.prompt, request.max_iterations)
    
    # Format response
    return {
        "optimized": result.get("optimized", request.prompt),
        "improvements": result.get("improvements", []),
        "metrics": result.get("metrics", {}),
        "original": result.get("original", request.prompt),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/evolve", response_model=EvolveResponse)
async def evolve(
    request: EvolveRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Evolve a prompt using genetic algorithms.
    
    Args:
        request: The evolution request
        api_key: The API key
        
    Returns:
        The evolution response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "premium")
    
    # Log the request
    logger.info(f"Evolution request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.evolve(request.seed_prompt, request.n_generations)
    
    # Format response
    return {
        "best_prompt": result.get("best_prompt", request.seed_prompt),
        "fitness": result.get("fitness", {}),
        "generations": result.get("generations", 0),
        "total_variants": result.get("total_variants", 0),
        "successful_mutations": result.get("successful_mutations", 0),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/classify", response_model=ClassifyResponse)
async def classify(
    request: ClassifyRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Classify a prompt into categories.
    
    Args:
        request: The classification request
        api_key: The API key
        
    Returns:
        The classification response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Classification request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.classify(request.text, request.labels)
    
    # Format response
    return {
        "input": result.get("input", request.text),
        "label": result.get("label", ""),
        "explanation": result.get("explanation", ""),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


# Prompt Management Endpoints
@router.post("/prompts/save", response_model=SavePromptResponse)
async def save_prompt(
    request: SavePromptRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Save a prompt for later use.
    
    Args:
        request: The save prompt request
        api_key: The API key
        
    Returns:
        The save prompt response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Save prompt request from user {user_id}")
    
    # Add user ID to metadata
    metadata = request.metadata or {}
    metadata["user_id"] = user_id
    
    # Call SynthLang API
    synthlang_api.save_prompt(request.name, request.prompt, metadata)
    
    # Format response
    return {
        "success": True,
        "name": request.name,
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/prompts/load", response_model=LoadPromptResponse)
async def load_prompt(
    request: LoadPromptRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Load a saved prompt.
    
    Args:
        request: The load prompt request
        api_key: The API key
        
    Returns:
        The load prompt response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Load prompt request from user {user_id}")
    
    # Call SynthLang API
    result = synthlang_api.load_prompt(request.name)
    
    # Check if prompt exists
    if not result.get("prompt"):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Prompt '{request.name}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Format response
    return {
        "name": result.get("name", request.name),
        "prompt": result.get("prompt", ""),
        "metadata": result.get("metadata", {}),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.get("/prompts/list", response_model=ListPromptsResponse)
async def list_prompts(
    api_key: str = Depends(verify_auth)
):
    """
    List all saved prompts.
    
    Args:
        api_key: The API key
        
    Returns:
        The list prompts response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"List prompts request from user {user_id}")
    
    # Call SynthLang API
    prompts = synthlang_api.list_prompts()
    
    # Filter prompts by user ID for non-admin users
    if not auth.has_role(user_id, "admin"):
        prompts = [p for p in prompts if p.get("metadata", {}).get("user_id") == user_id]
    
    # Format response
    return {
        "prompts": prompts,
        "count": len(prompts),
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/prompts/delete", response_model=DeletePromptResponse)
async def delete_prompt(
    request: DeletePromptRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Delete a saved prompt.
    
    Args:
        request: The delete prompt request
        api_key: The API key
        
    Returns:
        The delete prompt response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "basic")
    
    # Log the request
    logger.info(f"Delete prompt request from user {user_id}")
    
    # Check if prompt exists and belongs to user
    prompt_data = synthlang_api.load_prompt(request.name)
    if not prompt_data.get("prompt"):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Prompt '{request.name}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Check if user owns the prompt or is an admin
    prompt_user_id = prompt_data.get("metadata", {}).get("user_id")
    if prompt_user_id != user_id and not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "You don't have permission to delete this prompt",
                    "type": "permission_denied",
                    "code": HTTP_401_UNAUTHORIZED
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Call SynthLang API
    success = synthlang_api.delete_prompt(request.name)
    
    # Format response
    return {
        "success": success,
        "name": request.name,
        "version": get_version(),
        "timestamp": get_timestamp()
    }


@router.post("/prompts/compare", response_model=ComparePromptsResponse)
async def compare_prompts(
    request: ComparePromptsRequest,
    api_key: str = Depends(verify_auth)
):
    """
    Compare two saved prompts.
    
    Args:
        request: The compare prompts request
        api_key: The API key
        
    Returns:
        The compare prompts response
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(request, api_key)
    
    # Check if user has required role
    auth.require_role(user_id, "premium")
    
    # Log the request
    logger.info(f"Compare prompts request from user {user_id}")
    
    # Check if prompts exist
    prompt1 = synthlang_api.load_prompt(request.name1)
    prompt2 = synthlang_api.load_prompt(request.name2)
    
    if not prompt1.get("prompt"):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Prompt '{request.name1}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    if not prompt2.get("prompt"):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Prompt '{request.name2}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Call SynthLang API
    result = synthlang_api.compare_prompts(request.name1, request.name2)
    
    # Format response
    return {
        "prompts": result.get("prompts", {}),
        "metrics": result.get("metrics", {}),
        "differences": result.get("differences", {}),
        "version": get_version(),
        "timestamp": get_timestamp()
    }