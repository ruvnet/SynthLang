#!/usr/bin/env python3
"""
PII Masking Implementation Script

This script demonstrates how to implement PII masking in the API flow.
It shows the code changes needed to properly integrate PII masking with the API.
"""
import sys
import os
import logging
from typing import List, Dict, Any, Optional

# Add the proxy directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pii_implementation")

# Import the security module
try:
    from src.app.security import mask_pii, should_mask_pii_before_llm
    logger.info("Successfully imported security module")
except ImportError as e:
    logger.error(f"Error importing security module: {e}")
    sys.exit(1)

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_code(code, title=None):
    """Print code with syntax highlighting."""
    if title:
        print(f"\n--- {title} ---")
    print("\n```python")
    print(code)
    print("```\n")

def demonstrate_implementation():
    """Demonstrate how to implement PII masking in the API flow."""
    print_section("PII MASKING IMPLEMENTATION GUIDE")
    
    print("""
This script demonstrates how to properly implement PII masking in the SynthLang API flow.
Based on our testing, we've identified that while the PII masking function works correctly
when called directly, it's not being properly integrated into the API request/response flow.

Below are the recommended code changes to implement PII masking correctly.
""")

    # 1. Handling headers in the API endpoint
    print_section("1. HANDLING PII MASKING HEADERS")
    
    print("""
The first step is to properly handle the PII masking headers in the API endpoints.
The X-Mask-PII-Before-LLM and X-Mask-PII-In-Logs headers should be extracted and
used to override the default configuration.
""")
    
    header_code = """
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def create_chat_completion(
    request: ChatRequest,
    authorization: str = Header(None),
    x_mask_pii_before_llm: Optional[str] = Header(None, alias="X-Mask-PII-Before-LLM"),
    x_mask_pii_in_logs: Optional[str] = Header(None, alias="X-Mask-PII-In-Logs")
):
    \"\"\"
    Create a chat completion.
    
    Args:
        request: The chat completion request
        authorization: The Authorization header containing the API key
        x_mask_pii_before_llm: Header to control PII masking before sending to LLM
        x_mask_pii_in_logs: Header to control PII masking in logs
        
    Returns:
        The chat completion response
    \"\"\"
    # Verify API key
    if not authorization:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Missing API key",
                    "type": "auth_error",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    # Override PII masking configuration based on headers
    from src.app.security import should_mask_pii_before_llm, should_mask_pii_in_logs
    mask_pii_before_llm = bool(int(x_mask_pii_before_llm)) if x_mask_pii_before_llm is not None else should_mask_pii_before_llm()
    mask_pii_in_logs = bool(int(x_mask_pii_in_logs)) if x_mask_pii_in_logs is not None else should_mask_pii_in_logs()
    
    logger.info(f"PII masking settings: before_llm={mask_pii_before_llm}, in_logs={mask_pii_in_logs}")
    
    # Continue with the rest of the function...
"""
    print_code(header_code, "API Endpoint with PII Headers")

    # 2. Applying PII masking after compression
    print_section("2. APPLYING PII MASKING AFTER COMPRESSION")
    
    print("""
The key issue we identified is that PII masking needs to be applied AFTER compression
but BEFORE sending to the LLM. Currently, the compression is applied but PII masking
is not being called in the API flow.
""")
    
    masking_code = """
# 1. Compress user and system messages using SynthLang
compressed_messages = []
for msg in request.messages:
    if msg.role in ("user", "system"):
        # Use the new API for compression
        from .synthlang.api import synthlang_api
        compressed_content = synthlang_api.compress(msg.content)
        compressed_messages.append({"role": msg.role, "content": compressed_content})
    else:
        compressed_messages.append({"role": msg.role, "content": msg.content})

# 2. Apply PII masking to compressed messages if enabled
if mask_pii_before_llm:
    from src.app.security import mask_pii
    masked_messages = []
    for msg in compressed_messages:
        if msg["role"] in ("user", "system"):
            masked_content = mask_pii(msg["content"])
            masked_messages.append({"role": msg["role"], "content": masked_content})
        else:
            masked_messages.append(msg)
    compressed_messages = masked_messages
    logger.info("Applied PII masking to compressed messages before sending to LLM")

# 3. Semantic cache lookup: embed last user message
cache_key = cache.make_cache_key(compressed_messages, request.model)
cached_response = cache.get_similar_response(cache_key)

# Continue with the rest of the function...
"""
    print_code(masking_code, "Applying PII Masking After Compression")

    # 3. Applying PII masking to logs
    print_section("3. APPLYING PII MASKING TO LOGS")
    
    print("""
For log masking, we need to ensure that PII is masked before writing to logs.
This can be implemented by creating a custom log formatter or by wrapping the
logger to mask PII in log messages.
""")
    
    logging_code = """
# Create a PII-masking log formatter
class PIIMaskingFormatter(logging.Formatter):
    \"\"\"
    A log formatter that masks PII in log messages.
    \"\"\"
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        from src.app.security import mask_pii, should_mask_pii_in_logs
        self.mask_pii = mask_pii
        self.should_mask_pii_in_logs = should_mask_pii_in_logs
    
    def format(self, record):
        # First, format the record normally
        formatted = super().format(record)
        
        # Then, if PII masking is enabled, mask PII in the formatted message
        if self.should_mask_pii_in_logs():
            return self.mask_pii(formatted)
        return formatted

# Configure the logger with the PII-masking formatter
def configure_pii_masking_logger():
    \"\"\"
    Configure the logger to use the PII-masking formatter.
    \"\"\"
    formatter = PIIMaskingFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Configure handlers
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)
    
    logger.info("Configured PII masking for logs")

# Call this function during application startup
configure_pii_masking_logger()
"""
    print_code(logging_code, "PII Masking for Logs")

    # 4. Testing the implementation
    print_section("4. TESTING THE IMPLEMENTATION")
    
    print("""
After implementing these changes, you can test the PII masking functionality using
the test scripts we've provided:

1. `test_pii_masking.sh`: Tests the PII masking function directly
2. `test_pii_integration.sh`: Tests the integration of PII masking with the API

The tests should show that:
- PII is properly masked in the compressed messages when the X-Mask-PII-Before-LLM header is set
- PII is properly masked in logs when the X-Mask-PII-In-Logs header is set
""")

    # 5. Summary
    print_section("SUMMARY")
    
    print("""
To properly implement PII masking in the SynthLang API, you need to:

1. Extract and handle the PII masking headers in the API endpoints
2. Apply PII masking to compressed messages before sending to the LLM
3. Configure logging to mask PII in log messages

The PII masking function itself is already implemented correctly in src/app/security.py.
The issue is that it's not being called at the right points in the API flow.

By making these changes, you'll ensure that sensitive information is properly protected
before being sent to LLMs and before being written to logs.
""")

if __name__ == "__main__":
    demonstrate_implementation()