# Phase 6: LLM Provider Integration (06-llm_provider_integration.md)

## Objective
Integrate with an LLM provider (e.g., OpenAI) to get chat completions when cache misses occur. Implement dynamic model routing (GPT-4o vs o3-mini).

## Steps

1.  **Create `app/llm_provider.py` file:**
    -   Create `app/llm_provider.py` to house LLM provider integration logic.

2.  **Implement LLM Provider Client Functions in `app/llm_provider.py`:**
    -   Implement `complete_chat(model: str, messages: list, temperature: float = 1.0, top_p: float = 1.0, n: int = 1, user_id: str = None) -> dict` function:
        -   This function will call the LLM API to get a chat completion.
        -   For now, hardcode API key or use a placeholder for API key retrieval.
        -   Use `openai` Python library to call OpenAI ChatCompletion API.
        -   Implement basic model routing:
            -   If `model` contains "gpt-4o", use "gpt-4o-search-preview" model (or similar).
            -   Otherwise, use "o3-mini" model (or similar).
        -   Return the raw response dictionary from `openai.ChatCompletion.create()`.
        -   Handle potential exceptions during API calls (e.g., network errors, API errors) and raise them as custom exceptions or return error responses.
    -   Implement `stream_chat(model: str, messages: list, temperature: float = 1.0, top_p: float = 1.0, n: int = 1, user_id: str = None)` function:
        -   Implement streaming chat completion using `openai.ChatCompletion.create(stream=True)`.
        -   Return an async generator that yields chunks from the streaming response.
    -   Implement `get_embedding(text: str) -> list` function (if not already implemented in `app/cache.py` in a previous phase):
        -   This function should call the OpenAI Embedding API to get embeddings for text.
        -   For now, use "text-embedding-ada-002" model.
        -   Return the embedding vector as a list of floats.

    ```python
    # app/llm_provider.py
    import os
    import openai

    # For simplicity, using a hardcoded API key for now, replace with config/env var later
    openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY") # Replace with your API key or env var

    async def complete_chat(model: str, messages: list, temperature: float = 1.0,
                            top_p: float = 1.0, n: int = 1, user_id: str = None) -> dict:
        """Calls OpenAI ChatCompletion API (non-streaming)."""
        # Basic model routing
        if "gpt-4o" in model:
            llm_model = "gpt-4o-search-preview" # Or appropriate GPT-4o model
        else:
            llm_model = "o3-mini" # Or appropriate o3-mini model

        try:
            response = openai.ChatCompletion.create(
                model=llm_model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=False # Non-streaming
            )
            return response
        except Exception as e:
            print(f"LLM API call failed: {e}") # Log error
            raise # Re-raise exception for handling in main.py

    async def stream_chat(model: str, messages: list, temperature: float = 1.0,
                          top_p: float = 1.0, n: int = 1, user_id: str = None):
        """Calls OpenAI ChatCompletion API (streaming). Returns async generator."""
        if "gpt-4o" in model:
            llm_model = "gpt-4o-search-preview" # Or appropriate GPT-4o model
        else:
            llm_model = "o3-mini" # Or appropriate o3-mini model

        response_iter = openai.ChatCompletion.create(
            model=llm_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=True # Streaming
        )
        async def stream_generator(): # Wrap iterator in async generator
            for chunk in response_iter:
                yield chunk
        return stream_generator()

    def get_embedding(text: str) -> list:
        """Calls OpenAI Embedding API."""
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response["data"][0]["embedding"]
        return embedding
    ```

3.  **Integrate LLM Provider in `app/main.py`:**
    -   Import `llm_provider` from `app.llm_provider`.
    -   In `create_chat_completion` function:
        -   If `cached_response` is `None` (cache miss):
            -   Call `llm_provider.complete_chat(model=request.model, messages=final_messages, temperature=request.temperature, top_p=request.top_p, n=request.n, user_id=user_id)` for non-streaming requests.
            -   Call `llm_provider.stream_chat(...)` for streaming requests and return `StreamingResponse` (similar to how cached streaming response is handled).
            -   Extract the assistant's message content from the LLM response and return it in the API response.
        -   For now, handle only non-streaming requests for simplicity. Streaming will be added in a sub-step or next phase.
        -   Handle potential exceptions from `llm_provider.complete_chat` and return 500 error if LLM call fails.
        -   After successful LLM call and getting `assistant_msg`, call `cache.store(cache_key, assistant_msg)` to store the response in the cache.

    ```python
    # app/main.py
    from fastapi import FastAPI, Depends, HTTPException
    from fastapi.responses import StreamingResponse, JSONResponse # Import JSONResponse
    from app.models import ChatRequest
    from app import auth, synthlang, cache, llm_provider # Import llm_provider

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

        # 2. Semantic cache lookup: embed last user message.
        cache_key = cache.make_cache_key(compressed_messages, request.model)
        cached_response = cache.get_similar_response(cache_key)
        if cached_response: # Cache hit
            return {"message": "Cache hit!", "cached_response": cached_response, "cache_hit": True} # Indicate cache hit

        # 3. No cache hit: Call LLM provider
        final_messages = []
        for msg in compressed_messages: # Decompress for LLM call
            if msg["role"] in ("user", "system"):
                final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
            else:
                final_messages.append(msg)
        try:
            result = await llm_provider.complete_chat(model=request.model, messages=final_messages, temperature=request.temperature, top_p=request.top_p, n=request.n, user_id=user_id) # Call LLM
            assistant_msg = result["choices"][0]["message"]["content"] # Extract assistant message
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM provider call failed: {e}") # Handle LLM errors

        # 4. Store in cache (after successful LLM call)
        cache.store(cache_key, assistant_msg) # Store LLM response in cache

        return {
            "message": "LLM response",
            "request_model_valid": True,
            "api_key_verified": True,
            "user_id": user_id,
            "rate_limit_allowed": True,
            "compressed_messages": compressed_messages,
            "cache_hit": False, # Indicate cache miss
            "llm_response_content": assistant_msg # Include LLM response content
        }
    ```

4.  **Create test file `tests/test_llm_provider.py`:**
    -   Create `tests/test_llm_provider.py` for LLM provider integration tests.

5.  **Write tests for LLM Provider in `tests/test_llm_provider.py`:**
    -   Test `complete_chat` function:
        -   **Successful LLM Call:** Mock `openai.ChatCompletion.create` to return a successful response. Test that `complete_chat` returns a dictionary and does not raise an exception. Verify the returned dictionary structure (e.g., check for "choices" key). (More detailed response validation can be added later).
        -   **LLM API Call Failure:** Mock `openai.ChatCompletion.create` to raise an exception. Test that `complete_chat` raises an exception or returns an error response (depending on error handling strategy).

    ```python
    # tests/test_llm_provider.py
    from app import llm_provider
    from unittest.mock import AsyncMock, patch
    import pytest

    @pytest.mark.asyncio
    async def test_complete_chat_success():
        # Mock openai.ChatCompletion.create to simulate successful LLM call
        mock_chat_completion_create = AsyncMock(return_value={"choices": [{"message": {"content": "Test response"}}], "usage": {}})
        with patch("openai.ChatCompletion.create", new=mock_chat_completion_create):
            response = await llm_provider.complete_chat(model="test-model", messages=[{"role": "user", "content": "Test message"}])
            assert isinstance(response, dict) # Check if response is a dict
            assert "choices" in response # Check for 'choices' key

    @pytest.mark.asyncio
    async def test_complete_chat_failure():
        # Mock openai.ChatCompletion.create to raise an exception (simulate API error)
        mock_chat_completion_create = AsyncMock(side_effect=Exception("API Error"))
        with patch("openai.ChatCompletion.create", new=mock_chat_completion_create):
            with pytest.raises(Exception, match="LLM API call failed"): # Expect exception to be raised
                await llm_provider.complete_chat(model="test-model", messages=[{"role": "user", "content": "Test message"}])
    ```

6.  **Update `tests/test_api.py` to test LLM Provider integration in API endpoint:**
    -   In `test_chat_completion_endpoint_exists` and `test_valid_api_key`:
        -   Monkeypatch `llm_provider.complete_chat` to return a mock LLM response.
        -   Assert that when there's a cache miss, the API endpoint calls `llm_provider.complete_chat` and returns the LLM response content in the API response (check for `"llm_response_content"` key).
        -   For cache hit scenario in tests, ensure that LLM provider is NOT called (verify using mock call count).

7.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_llm_provider.py tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/llm_provider.py` file.
-   [x] Step 2: Implement LLM Provider Client Functions in `app/llm_provider.py`.
-   [x] Step 3: Integrate LLM Provider in `app/main.py`.
-   [x] Step 4: Create test file `tests/test_llm_provider.py`.
-   [x] Step 5: Write tests for LLM Provider in `tests/test_llm_provider.py`.
-   [x] Step 6: Update `tests/test_api.py` to test LLM Provider in API endpoint.
    - [ ] Step 6.1: Test LLM call on cache miss and response content.
    - [ ] Step 6.2: Test LLM is NOT called on cache hit.
-   [ ] Step 7: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Database Persistence (07-database_persistence.md)

---