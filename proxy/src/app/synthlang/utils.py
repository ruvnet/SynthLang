"""
Utility functions for SynthLang API.

This module provides utility functions for the SynthLang API.
"""
import logging
import time
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)


def get_dspy_lm() -> Optional[Any]:
    """
    Get a DSPy language model instance.
    
    Returns:
        DSPy language model instance or None if not available
    """
    try:
        # Import DSPy
        import dspy
        
        # Create a language model instance
        from src.app.config import OPENAI_API_KEY
        
        # Check if API key is set
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set, cannot create DSPy language model")
            return None
        
        # Create OpenAI LM
        lm = dspy.OpenAI(api_key=OPENAI_API_KEY, model="gpt-4")
        logger.info("Created DSPy language model")
        
        return lm
    except ImportError:
        logger.warning("DSPy not installed, cannot create language model")
        return None
    except Exception as e:
        logger.error(f"Failed to create DSPy language model: {e}")
        return None


def format_synthlang_response(result: Dict[str, Any], version: str = "1.0") -> Dict[str, Any]:
    """
    Format a SynthLang API response.
    
    Args:
        result: The result to format
        version: API version
        
    Returns:
        Formatted response
    """
    # Add version and timestamp
    response = result.copy()
    response["version"] = version
    response["timestamp"] = time.time()
    
    return response


def is_synthlang_available() -> bool:
    """
    Check if SynthLang is available.
    
    Returns:
        True if SynthLang is available, False otherwise
    """
    try:
        # Import SynthLang API
        from src.app.synthlang.api import synthlang_api
        
        # Check if API is enabled
        return synthlang_api.is_enabled()
    except ImportError:
        logger.warning("SynthLang API not available")
        return False
    except Exception as e:
        logger.error(f"Error checking SynthLang availability: {e}")
        return False