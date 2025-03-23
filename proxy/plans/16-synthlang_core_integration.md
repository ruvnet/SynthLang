# SynthLang Core Integration Plan

## Overview

This plan outlines the integration of the SynthLang core modules from the CLI into the proxy service. The goal is to provide a clean API interface for the core functionality and expose it through FastAPI endpoints.

## Objectives

1. Import and use the existing SynthLang core modules from the CLI
2. Create a clean API interface for the core functionality
3. Expose the functionality through FastAPI endpoints
4. Maintain backward compatibility with the existing compression/decompression functionality
5. Add comprehensive tests and documentation

## Architecture

The SynthLang integration will follow a modular architecture:

```
proxy/src/app/synthlang/
  ├── __init__.py           # Exports main functionality
  ├── compression.py        # Original compression/decompression functionality
  ├── api.py                # API interface for SynthLang core
  ├── endpoints.py          # FastAPI endpoints
  ├── models.py             # Pydantic models for API
  ├── utils.py              # Utility functions
  └── core/                 # Core modules from CLI
      └── __init__.py       # Imports core modules from CLI
```

## Implementation Steps

### 1. Create Core Module

Create a core module that imports the SynthLang core modules from the CLI:

```python
# proxy/src/app/synthlang/core/__init__.py
"""
SynthLang core module.

This module imports and re-exports the core modules from the CLI implementation.
"""
import sys
import os
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Add the CLI directory to the Python path to import the core modules
cli_path = Path(__file__).parent.parent.parent.parent.parent / "cli"
if cli_path.exists() and str(cli_path) not in sys.path:
    sys.path.append(str(cli_path))
    logger.info(f"Added CLI path to Python path: {cli_path}")

# Import core modules from CLI
try:
    from cli.synthlang.core import (
        SynthLangModule,
        FrameworkTranslator,
        SystemPromptGenerator,
        PromptOptimizer,
        PromptEvolver,
        PromptManager,
        PromptClassifier,
        TranslationResult,
        GenerationResult,
        OptimizationResult,
        SynthLangSymbols,
        FormatRules
    )
    
    logger.info("Successfully imported SynthLang core modules from CLI")
except ImportError as e:
    logger.error(f"Failed to import SynthLang core modules from CLI: {e}")
    # Define fallback classes
    # ...
```

### 2. Create API Interface

Create an API interface for the SynthLang core functionality:

```python
# proxy/src/app/synthlang/api.py
"""
SynthLang API interface.

This module provides a clean API interface to the SynthLang core functionality.
"""
import logging
from typing import Any, Dict, List, Optional, Union
import os

from app.config import USE_SYNTHLANG
from app.synthlang.compression import compress_prompt, decompress_prompt
from app.synthlang.core import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator,
    PromptOptimizer,
    PromptEvolver,
    PromptClassifier,
    PromptManager,
    TranslationResult,
    GenerationResult,
    OptimizationResult,
    SynthLangSymbols,
    FormatRules
)

# Configure logging
logger = logging.getLogger(__name__)

# Toggle to enable/disable SynthLang from configuration
ENABLE_SYNTHLANG = USE_SYNTHLANG


class SynthLangAPI:
    """API interface for SynthLang functionality."""
    
    def __init__(self, lm: Optional[Any] = None, storage_dir: Optional[str] = None):
        """
        Initialize SynthLang API with optional language model.
        
        Args:
            lm: Optional language model instance
            storage_dir: Optional directory for prompt storage
        """
        self.lm = lm
        self.enabled = ENABLE_SYNTHLANG
        
        # Initialize core modules if enabled
        if self.enabled:
            try:
                self.translator = FrameworkTranslator(lm) if lm else None
                self.generator = SystemPromptGenerator(lm) if lm else None
                self.optimizer = PromptOptimizer(lm) if lm else None
                self.evolver = PromptEvolver(lm) if lm else None
                self.classifier = None  # Initialize on demand with labels
                self.prompt_manager = PromptManager(storage_dir)
                logger.info("SynthLang API initialized with core modules")
            except Exception as e:
                logger.error(f"Failed to initialize SynthLang API: {e}")
                self.enabled = False
    
    # API methods
    # ...
```

### 3. Create Pydantic Models

Create Pydantic models for the API endpoints:

```python
# proxy/src/app/synthlang/models.py
"""
SynthLang API models.

This module defines the Pydantic models for SynthLang API endpoints.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Request model for translation endpoint."""
    text: str = Field(..., description="Text to translate to SynthLang format")
    instructions: Optional[str] = Field(None, description="Optional custom translation instructions")


class TranslateResponse(BaseModel):
    """Response model for translation endpoint."""
    source: str = Field(..., description="Original text")
    target: str = Field(..., description="Translated text in SynthLang format")
    explanation: str = Field(..., description="Explanation of the translation")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")

# More models
# ...
```

### 4. Create FastAPI Endpoints

Create FastAPI endpoints for the SynthLang functionality:

```python
# proxy/src/app/synthlang/endpoints.py
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

# Endpoints
# ...
```

### 5. Update Main Application

Update the main application to include the SynthLang API endpoints:

```python
# proxy/src/app/main.py
# ...
from app.synthlang.endpoints import router as synthlang_router

# ...

# Include SynthLang API router
app.include_router(synthlang_router)
```

### 6. Create Utility Functions

Create utility functions for the SynthLang integration:

```python
# proxy/src/app/synthlang/utils.py
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

# More utility functions
# ...
```

### 7. Create Tests

Create tests for the SynthLang integration:

```python
# proxy/tests/test_synthlang_integration.py
"""
Tests for SynthLang integration.

This module contains tests for the SynthLang integration with the proxy.
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import json
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.synthlang.api import synthlang_api
from app.synthlang.utils import get_dspy_lm


# Create test client
client = TestClient(app)

# Tests
# ...
```

### 8. Create Documentation

Create documentation for the SynthLang integration:

```markdown
# SynthLang Integration

This document describes the integration of SynthLang core functionality into the proxy service.

## Overview

SynthLang is a powerful prompt engineering framework that provides advanced capabilities for working with LLM prompts. The integration brings these capabilities directly into the proxy service, allowing for more sophisticated prompt manipulation, optimization, and management.

## Features

The SynthLang integration provides the following features:

1. Prompt Compression and Decompression
2. Prompt Translation
3. System Prompt Generation
4. Prompt Optimization
5. Prompt Evolution
6. Prompt Classification
7. Prompt Management

## API Endpoints

The SynthLang integration exposes the following API endpoints:

- `/v1/synthlang/translate`
- `/v1/synthlang/generate`
- `/v1/synthlang/optimize`
- `/v1/synthlang/evolve`
- `/v1/synthlang/classify`
- `/v1/synthlang/prompts/save`
- `/v1/synthlang/prompts/load`
- `/v1/synthlang/prompts/list`
- `/v1/synthlang/prompts/delete`
- `/v1/synthlang/prompts/compare`

## Usage Examples

...
```

## Testing Strategy

1. Unit tests for each component
2. Integration tests for the API endpoints
3. Mock tests for the DSPy language model
4. End-to-end tests for the full integration

## Deployment Considerations

1. Ensure the CLI directory is accessible to the proxy service
2. Install the required dependencies (DSPy, etc.)
3. Set the required environment variables (OPENAI_API_KEY, etc.)
4. Configure the storage directory for prompt management

## Future Enhancements

1. Add support for more language models (Claude, Llama, etc.)
2. Add support for fine-tuning SynthLang models
3. Add a web UI for SynthLang functionality
4. Add support for prompt templates and variables
5. Add support for prompt versioning and history

## Timeline

1. Core module implementation: 1 day
2. API interface implementation: 1 day
3. FastAPI endpoints implementation: 1 day
4. Testing and documentation: 1 day
5. Integration and deployment: 1 day

Total: 5 days