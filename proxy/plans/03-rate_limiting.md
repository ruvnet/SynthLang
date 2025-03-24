# Phase 3: Rate Limiting (03-rate_limiting.md)

## Objective
Implement basic rate limiting per user based on API keys.

## Steps

1.  **Implement Rate Limiting Logic in `app/auth.py`:**
    -   Add `_request_counts` dictionary to `app/auth.py` to track request counts per user within a time window (e.g., 60 seconds).
    -   Implement `allow_request(user_id: str)` function in `app/auth.py`:
        -   This function checks if a user is allowed to make a request based on their rate limit.
        -   It should retrieve the rate limit (`rate_limit_qpm`) for the given `user_id` from `API_KEYS`.
        -   It should check the `_request_counts` for the user:
            -   If the time window has elapsed (e.g., 60 seconds), reset the count for the user.
            -   If the current request count is within the limit, increment the count and return `True`.
            -   If the limit is exceeded, return `False`.

    ```python
    # app/auth.py
    from fastapi import Header, HTTPException
    from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS
    import time

    API_KEYS = {
        "sk_test_user1": {"user_id": "user1", "rate_limit_qpm": 60},
        "sk_test_user2": {"user_id": "user2", "rate_limit_qpm": 5},
    }
    _request_counts = {} # Initialize request counts dictionary

    def verify_api_key(authorization: str = Header(...)): # Existing function, keep it
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing API key")
        api_key = authorization.split(" ", 1)[1]
        if api_key not in API_KEYS:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API key")
        return api_key

    def get_user_id(api_key: str) -> str: # Existing function, keep it
        return API_KEYS[api_key]["user_id"]

    def allow_request(user_id: str) -> bool: # Implement rate limiting function
        if user_id not in _request_counts:
            _request_counts[user_id] = [time.time(), 0] # [window_start, count]
        window_start, count = _request_counts[user_id]
        limit = next(v["rate_limit_qpm"] for k, v in API_KEYS.items() if v["user_id"] == user_id)
        current_time = time.time()
        if current_time - window_start > 60: # Reset window if time elapsed
            _request_counts[user_id] = [current_time, 0]
            return True
        if count < limit: # Allow request if within limit
            _request_counts[user_id][1] += 1
            return True
        return False # Rate limit exceeded
    ```

2.  **Apply Rate Limiting to `/v1/chat/completions` endpoint in `app/main.py`:**
    -   Import `allow_request` from `app.auth`.
    -   Call `auth.allow_request(user_id)` in `create_chat_completion` after getting `user_id`.
    -   If `allow_request` returns `False`, raise an `HTTPException(status_code=429, detail="Rate limit exceeded")`.

    ```python
    # app/main.py
    from fastapi import FastAPI, Depends, HTTPException # Import HTTPException
    from app.models import ChatRequest
    from app import auth

    app = FastAPI()

    @app.post("/v1/chat/completions")
    async def create_chat_completion(request: ChatRequest, api_key: str = Depends(auth.verify_api_key)):
        user_id = auth.get_user_id(api_key)
        if not auth.allow_request(user_id): # Rate limiting check
            raise HTTPException(status_code=429, detail="Rate limit exceeded") # Raise 429 if rate limited
        return {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": user_id, "rate_limit_allowed": True} # Added rate_limit_allowed to response
    ```

3.  **Update test file `tests/test_api.py`:**
    -   Add tests for:
        -   **Rate Limit Not Exceeded:** Send requests within the rate limit and assert that the status code is 200 and the response includes `"rate_limit_allowed": true`.
        -   **Rate Limit Exceeded:** Send requests exceeding the rate limit and assert that the status code is 429.

    ```python
    # tests/test_api.py
    from fastapi.testclient import TestClient
    from app.main import app
    from app import auth # Import auth to modify rate limits in tests

    client = TestClient(app)

    def test_chat_completion_endpoint_exists(): # Existing test, keep it, update assertion
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": "user1", "rate_limit_allowed": True} # Updated assertion

    def test_missing_api_key(): # Existing test, keep it
        response = client.post("/v1/chat/completions", json={"model": "test-model", "messages": []})
        assert response.status_code == 401

    def test_invalid_api_key(): # Existing test, keep it
        headers = {"Authorization": "Bearer invalid_key"}
        response = client.post("/v1/chat/completions", json={"model": "test-model", "messages": []}, headers=headers)
        assert response.status_code == 401

    def test_valid_api_key(): # Existing test, keep it, update assertion
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": "user1", "rate_limit_allowed": True} # Updated assertion


    def test_rate_limit_not_exceeded(): # Test for rate limit within allowed requests
        auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 2 # Set low rate limit for testing
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {"model": "test-model", "messages": [{"role": "user", "content": "Test"}]}
        responses = [client.post("/v1/chat/completions", json=req_body, headers=headers) for _ in range(2)] # Send 2 requests (within limit)
        assert all(res.status_code == 200 for res in responses) # Both should be successful
        assert all(res.json().get("rate_limit_allowed") == True for res in responses) # And rate_limit_allowed should be true
        auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 60 # Reset rate limit

    def test_rate_limit_exceeded(): # Test for exceeding rate limit
        auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 1 # Set very low rate limit for testing
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {"model": "test-model", "messages": [{"role": "user", "content": "Test"}]}
        client.post("/v1/chat/completions", json=req_body, headers=headers) # First request (should pass)
        response_rate_limited = client.post("/v1/chat/completions", json=req_body, headers=headers) # Second request (should be rate limited)
        assert response_rate_limited.status_code == 429 # Assert 429 status code for rate limiting
        auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 60 # Reset rate limit
    ```

4.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_api.py` to execute the tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Implement Rate Limiting Logic in `app/auth.py`.
-   [x] Step 2: Apply Rate Limiting to endpoint in `app/main.py`.
-   [x] Step 3: Update test file `tests/test_api.py` with rate limiting tests.
-   [ ] Step 4: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement SynthLang Integration (04-synthlang_integration.md)

---