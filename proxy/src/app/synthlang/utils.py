"""
SynthLang utility functions.

This module provides utility functions for SynthLang integration.
"""
import os
import logging
import importlib.util
from typing import Any, Dict, Optional, List, Union
import json

# Configure logging
logger = logging.getLogger(__name__)


def get_dspy_lm(model_name: Optional[str] = None) -> Optional[Any]:
    """
    Get a DSPy language model instance.
    
    Args:
        model_name: Optional model name to use
        
    Returns:
        DSPy language model instance or None if not available
    """
    # Check if DSPy is available
    if importlib.util.find_spec("dspy") is None:
        logger.warning("DSPy is not installed")
        return None
        
    try:
        import dspy
        from dspy.openai import OpenAI
        
        # Use environment variables for API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY environment variable not set")
            return None
            
        # Use the specified model or default
        model = model_name or os.environ.get("SYNTHLANG_DEFAULT_MODEL", "gpt-4o-mini")
        
        # Create OpenAI LM
        lm = OpenAI(api_key=api_key, model=model)
        logger.info(f"Created DSPy OpenAI LM with model: {model}")
        
        return lm
    except ImportError as e:
        logger.error(f"Failed to import DSPy or OpenAI: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to create DSPy LM: {e}")
        return None


def format_synthlang_response(result: Dict) -> Dict:
    """
    Format SynthLang result for API response.
    
    Args:
        result: SynthLang result dictionary
        
    Returns:
        Formatted result for API response
    """
    # Add version and timestamp
    formatted = {
        "version": "1.0",
        "timestamp": import_time_module().now().isoformat(),
        **result
    }
    
    # Ensure all values are JSON serializable
    return make_json_serializable(formatted)


def make_json_serializable(obj: Any) -> Any:
    """
    Make an object JSON serializable.
    
    Args:
        obj: Object to make JSON serializable
        
    Returns:
        JSON serializable object
    """
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # Convert to string for non-serializable objects
        return str(obj)


def import_time_module():
    """
    Import datetime module.
    
    Returns:
        datetime module
    """
    from datetime import datetime
    return datetime


def load_dspy_module() -> Optional[Any]:
    """
    Load DSPy module if available.
    
    Returns:
        DSPy module or None if not available
    """
    try:
        import dspy
        return dspy
    except ImportError:
        logger.warning("DSPy is not installed")
        return None


def get_storage_dir() -> str:
    """
    Get the storage directory for SynthLang.
    
    Returns:
        Storage directory path
    """
    storage_dir = os.environ.get("SYNTHLANG_STORAGE_DIR", "/tmp/synthlang")
    os.makedirs(storage_dir, exist_ok=True)
    return storage_dir


def save_json(data: Dict, filepath: str) -> bool:
    """
    Save data as JSON.
    
    Args:
        data: Data to save
        filepath: Path to save to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")
        return False


def load_json(filepath: str) -> Optional[Dict]:
    """
    Load JSON data.
    
    Args:
        filepath: Path to load from
        
    Returns:
        Loaded data or None if failed
    """
    try:
        with open(filepath) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return None


def validate_synthlang_format(text: str) -> bool:
    """
    Validate if text follows SynthLang format.
    
    Args:
        text: Text to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Import symbols from core
    try:
        from app.synthlang.core import SynthLangSymbols
        
        # Check if text contains at least one of each symbol
        has_input = SynthLangSymbols.INPUT in text
        has_process = SynthLangSymbols.PROCESS in text
        has_output = SynthLangSymbols.OUTPUT in text
        
        # Basic validation: must have at least input and output symbols
        return has_input and has_output
    except ImportError:
        logger.warning("Failed to import SynthLangSymbols")
        # Fallback validation
        return "↹" in text and "Σ" in text