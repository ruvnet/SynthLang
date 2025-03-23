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

from app import auth
from app.synthlang.api import synthlang_api
from app.synthlang.models import (
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
from app.synthlang.utils import (
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
async def translate_prompt(
    request: TranslateRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Translate natural language to SynthLang format.
    
    Args:
        request: Translation request
        authorization: Authorization header
        
    Returns:
        Translation response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Initialize language model if not already initialized
    if not synthlang_api.lm:
        lm = get_dspy_lm()
        if not lm:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "message": "Failed to initialize language model",
                        "type": "service_unavailable",
                        "code": 503
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        synthlang_api.set_language_model(lm)
    
    # Translate prompt
    try:
        result = synthlang_api.translate(request.text, request.instructions)
        
        # Format response
        response = {
            **result,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Translation error: {str(e)}",
                    "type": "translation_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/generate", response_model=GenerateResponse)
async def generate_prompt(
    request: GenerateRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Generate a system prompt from task description.
    
    Args:
        request: Generation request
        authorization: Authorization header
        
    Returns:
        Generation response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Initialize language model if not already initialized
    if not synthlang_api.lm:
        lm = get_dspy_lm()
        if not lm:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "message": "Failed to initialize language model",
                        "type": "service_unavailable",
                        "code": 503
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        synthlang_api.set_language_model(lm)
    
    # Generate prompt
    try:
        result = synthlang_api.generate(request.task_description)
        
        # Format response
        response = {
            **result,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Generation error: {str(e)}",
                    "type": "generation_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_prompt(
    request: OptimizeRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Optimize a prompt using SynthLang.
    
    Args:
        request: Optimization request
        authorization: Authorization header
        
    Returns:
        Optimization response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Initialize language model if not already initialized
    if not synthlang_api.lm:
        lm = get_dspy_lm()
        if not lm:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "message": "Failed to initialize language model",
                        "type": "service_unavailable",
                        "code": 503
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        synthlang_api.set_language_model(lm)
    
    # Optimize prompt
    try:
        result = synthlang_api.optimize(request.prompt, request.max_iterations)
        
        # Format response
        response = {
            **result,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Optimization error: {str(e)}",
                    "type": "optimization_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/evolve", response_model=EvolveResponse)
async def evolve_prompt(
    request: EvolveRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Evolve a prompt using SynthLang.
    
    Args:
        request: Evolution request
        authorization: Authorization header
        
    Returns:
        Evolution response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Initialize language model if not already initialized
    if not synthlang_api.lm:
        lm = get_dspy_lm()
        if not lm:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "message": "Failed to initialize language model",
                        "type": "service_unavailable",
                        "code": 503
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        synthlang_api.set_language_model(lm)
    
    # Evolve prompt
    try:
        result = synthlang_api.evolve(request.seed_prompt, request.n_generations)
        
        # Format response
        response = {
            "best_prompt": result["best_prompt"],
            "fitness": result["fitness"],
            "generations": result["generations"],
            "total_variants": result["total_variants"],
            "successful_mutations": result["successful_mutations"],
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Evolution error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Evolution error: {str(e)}",
                    "type": "evolution_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/classify", response_model=ClassifyResponse)
async def classify_prompt(
    request: ClassifyRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Classify a prompt using SynthLang.
    
    Args:
        request: Classification request
        authorization: Authorization header
        
    Returns:
        Classification response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Initialize language model if not already initialized
    if not synthlang_api.lm:
        lm = get_dspy_lm()
        if not lm:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "message": "Failed to initialize language model",
                        "type": "service_unavailable",
                        "code": 503
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        synthlang_api.set_language_model(lm)
    
    # Classify prompt
    try:
        result = synthlang_api.classify(request.text, request.labels)
        
        # Format response
        response = {
            "input": result["input"],
            "label": result["label"],
            "explanation": result["explanation"],
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Classification error: {str(e)}",
                    "type": "classification_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/prompts/save", response_model=SavePromptResponse)
async def save_prompt(
    request: SavePromptRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Save a prompt with metadata.
    
    Args:
        request: Save prompt request
        authorization: Authorization header
        
    Returns:
        Save prompt response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Save prompt
    try:
        # Add user ID to metadata
        metadata = request.metadata or {}
        metadata["user_id"] = user_id
        metadata["saved_at"] = get_timestamp()
        
        synthlang_api.save_prompt(request.name, request.prompt, metadata)
        
        # Format response
        response = {
            "success": True,
            "name": request.name,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"Save prompt error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Save prompt error: {str(e)}",
                    "type": "save_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/prompts/load", response_model=LoadPromptResponse)
async def load_prompt(
    request: LoadPromptRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Load a saved prompt.
    
    Args:
        request: Load prompt request
        authorization: Authorization header
        
    Returns:
        Load prompt response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Load prompt
    try:
        result = synthlang_api.load_prompt(request.name)
        
        # Check if prompt exists
        if not result.get("prompt"):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "message": f"No prompt found with name: {request.name}",
                        "type": "not_found",
                        "code": HTTP_404_NOT_FOUND
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        
        # Format response
        response = {
            **result,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"No prompt found with name: {request.name}",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    except Exception as e:
        logger.error(f"Load prompt error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Load prompt error: {str(e)}",
                    "type": "load_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.get("/prompts/list", response_model=ListPromptsResponse)
async def list_prompts(
    authorization: str = Depends(verify_auth)
):
    """
    List all saved prompts.
    
    Args:
        authorization: Authorization header
        
    Returns:
        List prompts response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # List prompts
    try:
        prompts = synthlang_api.list_prompts()
        
        # Format response
        response = {
            "prompts": prompts,
            "count": len(prompts),
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except Exception as e:
        logger.error(f"List prompts error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"List prompts error: {str(e)}",
                    "type": "list_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/prompts/delete", response_model=DeletePromptResponse)
async def delete_prompt(
    request: DeletePromptRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Delete a saved prompt.
    
    Args:
        request: Delete prompt request
        authorization: Authorization header
        
    Returns:
        Delete prompt response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Delete prompt
    try:
        success = synthlang_api.delete_prompt(request.name)
        
        # Check if prompt was deleted
        if not success:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "message": f"No prompt found with name: {request.name}",
                        "type": "not_found",
                        "code": HTTP_404_NOT_FOUND
                    },
                    "version": get_version(),
                    "timestamp": get_timestamp()
                }
            )
        
        # Format response
        response = {
            "success": True,
            "name": request.name,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"No prompt found with name: {request.name}",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    except Exception as e:
        logger.error(f"Delete prompt error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Delete prompt error: {str(e)}",
                    "type": "delete_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )


@router.post("/prompts/compare", response_model=ComparePromptsResponse)
async def compare_prompts(
    request: ComparePromptsRequest,
    authorization: str = Depends(verify_auth)
):
    """
    Compare two saved prompts.
    
    Args:
        request: Compare prompts request
        authorization: Authorization header
        
    Returns:
        Compare prompts response
    """
    # Get user ID from API key
    api_key = auth.verify_api_key(authorization)
    user_id = auth.get_user_id(api_key)
    
    # Check if SynthLang API is enabled
    if not synthlang_api.is_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "SynthLang API is disabled",
                    "type": "service_unavailable",
                    "code": 503
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    
    # Compare prompts
    try:
        result = synthlang_api.compare_prompts(request.name1, request.name2)
        
        # Format response
        response = {
            **result,
            "version": get_version(),
            "timestamp": get_timestamp()
        }
        
        return response
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": str(e),
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )
    except Exception as e:
        logger.error(f"Compare prompts error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Compare prompts error: {str(e)}",
                    "type": "compare_error",
                    "code": 500
                },
                "version": get_version(),
                "timestamp": get_timestamp()
            }
        )