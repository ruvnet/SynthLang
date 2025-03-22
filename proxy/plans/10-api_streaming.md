## Objective
Implement API streaming for both LLM responses and cached responses using Server-Sent Events (SSE).

## Steps

1.  **Implement Streaming Response in `app/main.py` for LLM calls:**
    -   Modify `create_chat_completion` function in `app/main.py`:
        -   When `request.stream` is `True` and there's a cache miss (LLM call is needed):
            -   Call `llm_provider.stream_chat(...)` to get an async generator for streaming LLM responses.
            -   Define an inner generator function `stream_generator()` that iterates through the `response_iter` from `llm_provider.stream_chat()`:
                -   For each chunk in `response_iter`, extract the `content_piece` from `chunk['choices'][0]['delta'].get('content', '')`.
                -   `yield` f"data: {content_piece}\n\n" to format it as SSE data event.
                -   `yield "data: [DONE]\n\n"` after the stream is finished to signal end of stream.
            -   Return `StreamingResponse(stream_generator(), media_type="text/event-stream")`.
        -   For non-streaming requests (`request.stream` is `False`), keep the existing logic of calling `llm_provider.complete_chat(...)` and returning `JSONResponse`.

    ```python
    # app/main.py (update create_chat_completion for streaming)
    from fastapi import FastAPI, Depends, HTTPException, Request
    from fastapi.responses import StreamingResponse, JSONResponse
    from app.models import ChatRequest
    from app import auth, synthlang, cache, llm_provider, db
    from app.agents import registry

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
            if request.stream: # Streaming cached response
                def yield_cached():
                    yield f"data: {cached_response}\n\n"
                    yield "data: [CACHE_END]\n\n" # Signal end of cached stream
                return StreamingResponse(yield_cached(), media_type="text/event-stream") # Return streaming response for cache hit
            else: # Non-streaming cache hit (existing logic)
                return JSONResponse(content={"message": "Cache hit!", "cached_response": cached_response, "cache_hit": True})

        # 3. No cache hit: Call LLM provider (handle streaming and non-streaming)
        final_messages = []
        for msg in compressed_messages:
            if msg["role"] in ("user", "system"):
                final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
            else:
                final_messages.append(msg)
        try:
            if request.stream: # Streaming LLM response
                response_iter = await llm_provider.stream_chat(model=request.model, messages=final_messages,
                                                                 temperature=request.temperature or 1.0,
                                                                 top_p=request.top_p or 1.0,
                                                                 n=request.n or 1, user_id=user_id)
                def stream_generator():
                    for chunk in response_iter:
                        if 'delta' in chunk.get('choices', [{}])[0]:
                            content_piece = chunk['choices'][0]['delta'].get('content', '')
                            yield f"data: {content_piece}\n\n" # Yield SSE data event
                    yield "data: [DONE]\n\n" # Signal end of LLM stream
                return StreamingResponse(stream_generator(), media_type="text/event-stream") # Return streaming response for LLM
            else: # Non-streaming LLM response (existing logic)
                result = await llm_provider.complete_chat(model=request.model, messages=final_messages,
                                                          temperature=request.temperature,
                                                          top_p=request.top_p,
                                                          n=request.n, user_id=user_id)
                assistant_msg = result["choices"][0]["message"]["content"]
                response_content = assistant_msg # Use LLM response
                cache_hit_flag = False # Cache miss
                # 4. Store in cache (after successful LLM call if cache miss) - keep existing logic
                cache.store(cache_key, response_content)

                # 5. Persist interaction to database - keep existing logic
                await db.save_interaction(user_id, request.model, compressed_messages, response_content, cache_hit=cache_hit_flag)

                return JSONResponse(content={ # Return non-streaming JSON response
                    "message": "LLM response",
                    "request_model_valid": True,
                    "api_key_verified": True,
                    "user_id": user_id,
                    "rate_limit_allowed": True,
                    "compressed_messages": compressed_messages,
                    "cache_hit": cache_hit_flag,
                    "llm_response_content": response_content
                })

        except Exception as e: # Exception handling - keep existing logic
            raise HTTPException(status_code=500, detail=f"LLM provider call failed: {e}")

2.  **Implement Streaming Response in `app/main.py` for Cache hits:**
    -   Modify `create_chat_completion` function in `app/main.py` (already done in step 1 in the code snippet above):
        -   When `request.stream` is `True` and there's a cache hit (`cached_response` is not `None`):
            -   Define an inner generator function `yield_cached()`:
                -   `yield f"data: {cached_response}\n\n"` to send the cached response as SSE data event.
                -   `yield "data: [CACHE_END]\n\n"` to signal end of cached stream.
            -   Return `StreamingResponse(yield_cached(), media_type="text/event-stream")`.

3.  **Update `tests/test_api.py` to test Streaming API endpoint:**
    -   Add tests for:
        -   **Non-Streaming Request:** Keep existing non-streaming tests to ensure they still work.
        -   **Streaming Request - Cache Miss:**
            -   Mock `llm_provider.stream_chat` to return a dummy streaming response (async generator).
            -   Send a streaming request (`stream=True`) to the API endpoint (cache miss scenario).
            -   Assert that the response status code is 200.
            -   Read the streaming response using `res.iter_lines(decode_unicode=True)`.
            -   Assert that the response is indeed a streaming response (check for "data:" prefixes in chunks).
            -   Reconstruct the full response text from the streamed chunks and assert that it matches the expected response (from the mock `llm_provider.stream_chat`).
        -   **Streaming Request - Cache Hit:**
            -   First, send a non-streaming request to populate the cache.
            -   Then, send a streaming request (`stream=True`) with the same input (cache hit scenario).
            -   Assert that the response status code is 200.
            -   Read the streaming response and assert that it contains the cached response and the `[CACHE_END]` signal.

    ```python
    # tests/test_api.py (update with streaming tests)
    from fastapi.testclient import TestClient
    from app.main import app
    from unittest.mock import AsyncMock, patch
    import pytest

    client = TestClient(app)

    # ... (Existing non-streaming tests remain) ...

    @pytest.mark.asyncio
    async def test_chat_completion_stream_cache_miss():
        # Mock llm_provider.stream_chat for streaming test (cache miss)
        async def mock_stream_chat(*args, **kwargs):
            async def stream_generator():
                yield {"choices": [{"delta": {"content": "Chunk 1"}}]}
                yield {"choices": [{"delta": {"content": "Chunk 2"}}]}
                yield {} # End of stream
            return stream_generator()
        with patch("app.llm_provider.stream_chat", new=mock_stream_chat):
            headers = {"Authorization": "Bearer sk_test_user1"}
            req_body = {"model": "test-model", "messages": [{"role": "user", "content": "Stream test"}], "stream": True}
            res = client.post("/v1/chat/completions", json=req_body, headers=headers, stream=True)
            assert res.status_code == 200
            streamed_text = "".join([chunk.replace("data: ", "") for chunk in res.iter_lines(decode_unicode=True) if chunk.startswith("data: ")]) # Reconstruct streamed text
            assert "Chunk 1Chunk 2" in streamed_text # Check streamed content

    @pytest.mark.asyncio
    async def test_chat_completion_stream_cache_hit():
        # First, populate cache with a non-streaming request
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body_non_stream = {"model": "test-model", "messages": [{"role": "user", "content": "Cache stream test"}], "stream": False}
        res_non_stream = client.post("/v1/chat/completions", json=req_body_non_stream, headers=headers)
        assert res_non_stream.status_code == 200

        # Now, send a streaming request with the same input (should be cache hit)
        req_body_stream = {"model": "test-model", "messages": [{"role": "user", "content": "Cache stream test"}], "stream": True}
        res_stream = client.post("/v1/chat/completions", json=req_body_stream, headers=headers, stream=True)
        assert res_stream.status_code == 200
        streamed_text = "".join([chunk.replace("data: ", "") for chunk in res_stream.iter_lines(decode_unicode=True) if chunk.startswith("data: ")]) # Reconstruct streamed text
        assert "Cache hit!" in streamed_text # Check for cache hit message
        assert "[CACHE_END]" in streamed_text # Check for cache end signal
        assert "cached_response" in streamed_text # Check for cached response content (might need more robust check if cached response is complex)
    ```

4.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Implement Streaming Response in `app/main.py` for LLM calls.
-   [x] Step 2: Implement Streaming Response in `app/main.py` for Cache hits.
-   [x] Step 3: Update `tests/test_api.py` to test Streaming API endpoint.
    - [ ] Step 3.1: Test Non-Streaming requests (ensure existing tests pass).
    - [ ] Step 3.2: Test Streaming Request - Cache Miss.
    - [ ] Step 3.3: Test Streaming Request - Cache Hit.
-   [ ] Step 4: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Configuration and Environment Variables (11-configuration_env_vars.md)

---