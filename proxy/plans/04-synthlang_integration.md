# Phase 4: SynthLang Integration (04-synthlang_integration.md)

## Objective
Integrate SynthLang CLI for prompt compression and decompression.

## Steps

1.  **Create `app/synthlang.py` file:**
    -   Create `app/synthlang.py` to house SynthLang integration logic.

2.  **Implement SynthLang Compression/Decompression Functions in `app/synthlang.py`:**
    -   Implement `compress_prompt(text: str)` function:
        -   This function should take text as input and compress it using the SynthLang CLI.
        -   Use `subprocess.run` to execute the `synthlang compress` command.
        -   Capture the stdout as the compressed text.
        -   Handle potential errors during subprocess execution (e.g., `FileNotFoundError`, non-zero exit code) and return the original text in case of error, logging the error.
        -   Implement a toggle `ENABLE_SYNTHLANG = True` to easily disable SynthLang for testing or if it's not available. If disabled, `compress_prompt` should return the original text unchanged.
    -   Implement `decompress_prompt(text: str)` function:
        -   This function should take compressed text as input and decompress it using the SynthLang CLI (`synthlang decompress` command).
        -   Similar error handling and toggle as `compress_prompt`.

    ```python
    # app/synthlang.py
    import subprocess

    ENABLE_SYNTHLANG = True # Toggle to enable/disable SynthLang

    def compress_prompt(text: str) -> str:
        """Compress a prompt using SynthLang CLI. Returns the compressed text."""
        if not ENABLE_SYNTHLANG:
            return text  # no compression if disabled
        try:
            proc = subprocess.run(
                ["synthlang", "compress"],  # command to compress via CLI
                input=text,
                text=True,
                capture_output=True,
                check=True
            )
            compressed = proc.stdout.strip()
            return compressed if compressed else text
        except Exception as e:
            print(f"[SynthLang] Compression error: {e}") # Log error
            return text # Fallback to original text

    def decompress_prompt(text: str) -> str:
        """Decompress a prompt using SynthLang CLI. Returns the decompressed text."""
        if not ENABLE_SYNTHLANG:
            return text # no decompression if disabled
        try:
            proc = subprocess.run(
                ["synthlang", "decompress"], # command to decompress via CLI
                input=text,
                text=True,
                capture_output=True,
                check=True
            )
            decompressed = proc.stdout.strip()
            return decompressed if decompressed else text
        except Exception as e:
            print(f"[SynthLang] Decompression error: {e}") # Log error
            return text # Fallback to original text
    ```

3.  **Integrate SynthLang in `app/main.py`:**
    -   Import `synthlang` from `app.synthlang`.
    -   In `create_chat_completion` function:
        -   Before cache lookup, compress the `content` of user and system messages in `request.messages` using `synthlang.compress_prompt()`. Create a new list `compressed_messages` with compressed content.
        -   After cache lookup (or if no cache hit), decompress the `content` of user and system messages in `compressed_messages` using `synthlang.decompress_prompt()` before sending to the LLM provider. Create a new list `final_messages` with decompressed content.
        -   For now, include the compressed and decompressed messages in the response for verification.

    ```python
    # app/main.py
    from fastapi import FastAPI, Depends, HTTPException
    from app.models import ChatRequest
    from app import auth, synthlang # Import synthlang

    app = FastAPI()

    @app.post("/v1/chat/completions")
    async def create_chat_completion(request: ChatRequest, api_key: str = Depends(auth.verify_api_key)):
        user_id = auth.get_user_id(api_key)
        if not auth.allow_request(user_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # 1. Compress user and system messages using SynthLang.
        compressed_messages = []
        for msg in request.messages:
            comp_content = synthlang.compress_prompt(msg.content) if msg.role in ("user", "system") else msg.content
            compressed_messages.append({"role": msg.role, "content": comp_content})

        # 2. For now, skip cache and LLM, just decompress and return
        final_messages = []
        for msg in compressed_messages:
            if msg["role"] in ("user", "system"):
                final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
            else:
                final_messages.append(msg)


        return {
            "message": "Endpoint is working",
            "request_model_valid": True,
            "api_key_verified": True,
            "user_id": user_id,
            "rate_limit_allowed": True,
            "compressed_messages": compressed_messages, # Include compressed messages in response
            "decompressed_messages": final_messages # Include decompressed messages in response
        }
    ```

4.  **Create test file `tests/test_synthlang.py`:**
    -   Create `tests/test_synthlang.py` for SynthLang integration tests.

5.  **Write tests for SynthLang integration in `tests/test_synthlang.py`:**
    -   Test `compress_prompt` and `decompress_prompt` functions:
        -   **Compression Shortens Text:** Test that `compress_prompt` reduces the length of a sample text.
        -   **Decompression Restores Original Text:** Test that `decompress_prompt` restores the original text after compression (round-trip test).
        -   **SynthLang Disabled:** Test that when `ENABLE_SYNTHLANG` is set to `False`, both functions return the original text unchanged.
        -   **Error Handling:** Test that if SynthLang CLI is not available or fails, the functions handle the error and return the original text (and log the error - verify logging output if feasible). (This might be harder to test without mocking subprocess, can be added later).

    ```python
    # tests/test_synthlang.py
    from app import synthlang

    def test_compress_prompt_shortens_text():
        original_text = "This is a long text to be compressed."
        compressed_text = synthlang.compress_prompt(original_text)
        assert len(compressed_text) < len(original_text)
        assert compressed_text != original_text # Ensure it's actually compressed

    def test_decompress_prompt_restores_original_text():
        original_text = "This is a text to be compressed and decompressed."
        compressed_text = synthlang.compress_prompt(original_text)
        decompressed_text = synthlang.decompress_prompt(compressed_text)
        assert decompressed_text == original_text # Round-trip test

    def test_synthlang_disabled():
        synthlang.ENABLE_SYNTHLANG = False # Disable SynthLang
        original_text = "Text to test when SynthLang is disabled."
        compressed_text = synthlang.compress_prompt(original_text)
        decompressed_text = synthlang.decompress_prompt(original_text)
        assert compressed_text == original_text # Should return original if disabled
        assert decompressed_text == original_text # Should return original if disabled
        synthlang.ENABLE_SYNTHLANG = True # Re-enable for other tests
    ```

6.  **Update `tests/test_api.py` to test SynthLang integration in API endpoint:**
    -   In `test_chat_completion_endpoint_exists` and `test_valid_api_key`, assert that the `decompressed_messages` in the response are the same as the original `request.messages` (basic check for decompression).
    -   (Optional) Add a more specific test in `tests/test_api.py` to check if compression is actually happening and compressed messages are different from original (this might require mocking Synthlang CLI or more complex assertions).

7.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_synthlang.py tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/synthlang.py` file.
-   [x] Step 2: Implement SynthLang Compression/Decompression Functions in `app/synthlang.py`.
-   [x] Step 3: Integrate SynthLang in `app/main.py`.
-   [x] Step 4: Create test file `tests/test_synthlang.py`.
-   [x] Step 5: Write tests for SynthLang integration in `tests/test_synthlang.py`.
-   [x] Step 6: Update `tests/test_api.py` to test SynthLang in API endpoint.
-   [ ] Step 7: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Semantic Cache (05-semantic_cache.md)

---