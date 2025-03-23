# Phase 16: SynthLang Core Integration (16-synthlang_core_integration.md)

## Objective
Integrate the SynthLang core module from `proxy/src/cli/synthlang/core` into the proxy/src structure to provide advanced prompt engineering capabilities directly within the proxy service.

## Current State Analysis

The SynthLang core module currently exists in `proxy/src/cli/synthlang/core` and includes several powerful components:

1. **Base Module**: `SynthLangModule` - Base class for all SynthLang modules
2. **Translator**: `FrameworkTranslator` - Translates natural language to SynthLang format
3. **Generator**: `SystemPromptGenerator` - Generates system prompts from task descriptions
4. **Optimizer**: `PromptOptimizer` - Optimizes prompts using DSPy techniques
5. **Evolver**: `PromptEvolver` - Evolves prompts using genetic algorithms
6. **Classifier**: `PromptClassifier` - Classifies prompts using DSPy
7. **Prompt Manager**: `PromptManager` - Manages storage and retrieval of prompts
8. **Types**: Type definitions and symbols for SynthLang format

Currently, the proxy only uses SynthLang CLI for basic prompt compression and decompression via subprocess calls in `app/synthlang.py`.

## Integration Plan

### 1. Create a Dedicated SynthLang Module Structure

Create a proper module structure for SynthLang within the proxy:

```
proxy/src/
  ├── app/
  │   ├── synthlang/
  │   │   ├── __init__.py
  │   │   ├── compression.py  # Current compression/decompression functionality
  │   │   ├── core/           # Core modules from cli/synthlang/core
  │   │   │   ├── __init__.py
  │   │   │   ├── base.py
  │   │   │   ├── translator.py
  │   │   │   ├── generator.py
  │   │   │   ├── optimizer.py
  │   │   │   ├── evolver.py
  │   │   │   ├── classifier.py
  │   │   │   ├── prompt_manager.py
  │   │   │   ├── signatures.py
  │   │   │   └── types.py
  │   │   ├── api.py          # API endpoints for SynthLang functionality
  │   │   └── utils.py        # Utility functions
```

### 2. Refactor Current SynthLang Integration

1. Move the current `app/synthlang.py` functionality to `app/synthlang/compression.py`
2. Create a new `app/synthlang/__init__.py` that exports the main functionality
3. Update imports in other modules to use the new structure

### 3. Integrate Core Modules

1. Copy and adapt the core modules from `proxy/src/cli/synthlang/core` to `app/synthlang/core/`
2. Ensure proper imports and dependencies are maintained
3. Adapt modules to work within the proxy context (e.g., use proxy's logging, config)

### 4. Create API Interface

Create a clean API interface in `app/synthlang/api.py` that exposes the core functionality:

```python
# app/synthlang/api.py
from typing import Dict, List, Optional, Any
from app.synthlang.core import (
    FrameworkTranslator,
    SystemPromptGenerator,
    PromptOptimizer,
    PromptEvolver,
    PromptClassifier,
    PromptManager
)

class SynthLangAPI:
    """API interface for SynthLang functionality."""
    
    def __init__(self, lm: Any = None):
        """Initialize SynthLang API with optional language model."""
        self.lm = lm
        self.translator = FrameworkTranslator(lm) if lm else None
        self.generator = SystemPromptGenerator(lm) if lm else None
        self.optimizer = PromptOptimizer(lm) if lm else None
        self.evolver = PromptEvolver(lm) if lm else None
        self.classifier = None  # Initialize on demand with labels
        self.prompt_manager = PromptManager()
        
    # Methods for each functionality...
```

### 5. Create FastAPI Endpoints

Create FastAPI endpoints in `app/main.py` to expose SynthLang functionality:

```python
# app/main.py (additions)
from app.synthlang.api import SynthLangAPI

# Initialize SynthLangAPI with default LM
synthlang_api = SynthLangAPI()

# SynthLang endpoints
@app.post("/v1/synthlang/translate")
async def translate_prompt(request: dict, api_key: str = Depends(auth.verify_api_key)):
    """Translate natural language to SynthLang format."""
    # Implementation...

@app.post("/v1/synthlang/generate")
async def generate_prompt(request: dict, api_key: str = Depends(auth.verify_api_key)):
    """Generate a system prompt from task description."""
    # Implementation...

# More endpoints...
```

### 6. Add Configuration Options

Add configuration options in `app/config.py` for SynthLang features:

```python
# app/config.py (additions)
SYNTHLANG_FEATURES_ENABLED = os.getenv("SYNTHLANG_FEATURES_ENABLED", "true").lower() == "true"
SYNTHLANG_DEFAULT_MODEL = os.getenv("SYNTHLANG_DEFAULT_MODEL", "gpt-4o-mini")
SYNTHLANG_STORAGE_DIR = os.getenv("SYNTHLANG_STORAGE_DIR", "/tmp/synthlang")
```

### 7. Create Utility Functions

Create utility functions in `app/synthlang/utils.py` for common operations:

```python
# app/synthlang/utils.py
import os
from typing import Any, Dict, Optional
import dspy

def get_dspy_lm(model_name: str = None) -> Any:
    """Get a DSPy language model instance."""
    # Implementation...

def format_synthlang_response(result: Dict) -> Dict:
    """Format SynthLang result for API response."""
    # Implementation...
```

### 8. Testing Strategy

Create comprehensive tests for the SynthLang integration:

1. **Unit Tests**:
   - Test each core module individually
   - Test the API interface
   - Test utility functions

2. **Integration Tests**:
   - Test the FastAPI endpoints
   - Test interaction between modules

3. **End-to-End Tests**:
   - Test complete workflows using the SynthLang functionality

Test files:
```
proxy/tests/
  ├── test_synthlang_compression.py  # Tests for compression/decompression
  ├── test_synthlang_translator.py   # Tests for translator module
  ├── test_synthlang_generator.py    # Tests for generator module
  ├── test_synthlang_optimizer.py    # Tests for optimizer module
  ├── test_synthlang_evolver.py      # Tests for evolver module
  ├── test_synthlang_classifier.py   # Tests for classifier module
  ├── test_synthlang_api.py          # Tests for API interface
  └── test_synthlang_endpoints.py    # Tests for FastAPI endpoints
```

### 9. Documentation

Create comprehensive documentation for the SynthLang integration:

1. **API Documentation**:
   - Document all API endpoints
   - Document request/response formats
   - Provide examples

2. **Usage Documentation**:
   - Document how to use SynthLang features
   - Provide examples for common use cases

3. **Developer Documentation**:
   - Document the module structure
   - Document how to extend the functionality

Documentation files:
```
proxy/docs/
  ├── synthlang_integration.md       # Overview of SynthLang integration
  ├── synthlang_api.md               # API documentation
  ├── synthlang_usage.md             # Usage documentation
  └── synthlang_development.md       # Developer documentation
```

## Implementation Steps

### Phase 1: Setup and Refactoring

1. Create the directory structure for the SynthLang module
2. Refactor the current `app/synthlang.py` to `app/synthlang/compression.py`
3. Create `app/synthlang/__init__.py` to export the main functionality
4. Update imports in other modules

### Phase 2: Core Module Integration

1. Copy and adapt the core modules from `proxy/src/cli/synthlang/core`
2. Ensure proper imports and dependencies
3. Adapt modules to work within the proxy context

### Phase 3: API Interface and Endpoints

1. Create the API interface in `app/synthlang/api.py`
2. Create FastAPI endpoints in `app/main.py`
3. Add configuration options in `app/config.py`
4. Create utility functions in `app/synthlang/utils.py`

### Phase 4: Testing and Documentation

1. Create unit tests for each module
2. Create integration tests for the API interface and endpoints
3. Create end-to-end tests for complete workflows
4. Create comprehensive documentation

## Benefits

1. **Enhanced Functionality**: Provides advanced prompt engineering capabilities directly within the proxy
2. **Improved Performance**: Eliminates subprocess calls to the SynthLang CLI
3. **Better Integration**: Tighter integration with the proxy's authentication, rate limiting, and caching
4. **Extensibility**: Easier to extend with new SynthLang features
5. **Testability**: More comprehensive testing of SynthLang functionality
6. **Documentation**: Better documentation for users and developers

## Risks and Mitigations

1. **Dependency Management**: 
   - Risk: The SynthLang core modules have dependencies that may conflict with the proxy's dependencies
   - Mitigation: Carefully manage dependencies and use virtual environments

2. **Performance Impact**:
   - Risk: The SynthLang core modules may impact the performance of the proxy
   - Mitigation: Profile and optimize the integration, consider async processing for heavy operations

3. **Maintenance Overhead**:
   - Risk: Maintaining two copies of the SynthLang core modules (in CLI and proxy)
   - Mitigation: Consider creating a shared package for the core modules

4. **Backward Compatibility**:
   - Risk: Breaking changes to the current SynthLang integration
   - Mitigation: Maintain backward compatibility with the current API

## Success Criteria

1. All tests pass
2. Documentation is complete and accurate
3. Performance is acceptable (benchmarks show no significant degradation)
4. All SynthLang features are accessible through the API
5. Backward compatibility is maintained

## Next Steps

After successful integration of the SynthLang core module, consider:

1. Enhancing the proxy with more advanced SynthLang features
2. Creating a shared package for the SynthLang core modules
3. Providing a web UI for SynthLang functionality
4. Integrating SynthLang with other proxy features (e.g., caching, rate limiting)