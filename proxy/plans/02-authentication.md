# Phase 2: API Key Authentication (02-authentication.md)

## Objective
Implement API key authentication for the `/v1/chat/completions` endpoint.

## Steps

1.  **Create `app/auth.py` file:**
    -   Create `app/auth.py` to house authentication logic.

2.  **Implement API Key Verification in `app/auth.py`:**
    -   Define a dictionary `API_KEYS` for storing valid API keys and associated user IDs and rate limits (for now, in-memory).
    -   Implement `verify_api_key(authorization: str = Header(...))` function:
        -   This function will be a FastAPI dependency.
        -   It should extract the API key from the `Authorization` header (Bearer token).
        -   Check if the API key exists in `API_KEYS`.
        -   If the key is missing or invalid, raise an `HTTPException(status_code=401)`.
        -   If the key is valid, return the API key string.
    -   Implement `get_user_id(api_key: str)` function to retrieve the user ID associated with a valid API key.

    ```python
    # app/auth.py
    from fastapi import Header, HTTPException
    from starlette.status import HTTP_401_UNAUTHORIZED

    API_KEYS = {
        "sk_test_user1": {"user_id": "user1", "rate_limit_qpm": 60},
        "sk_test_user2": {"user_id": "user2", "rate_limit_qpm": 5},
    }

    def verify_api_key(authorization: str = Header(...)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing API key")
        api_key = authorization.split(" ", 1)[1]
        if api_key not in API_KEYS:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API key")
        return api_key

    def get_user_id(api_key: str) -> str:
        return API_KEYS[api_key]["user_id"]
    ```

3.  **Apply `verify_api_key` dependency to `/v1/chat/completions` endpoint in `app/main.py`:**
    -   Import `verify_api_key` from `app.auth`.
    -   Add `api_key: str = Depends(auth.verify_api_key)` as a dependency to the `create_chat_completion` function.
    -   For now, just pass the `api_key` to the response to verify it's working.

    ```python
    # app/main.py
    from fastapi import FastAPI, Depends
    from app.models import ChatRequest
    from app import auth

    app = FastAPI()

    @app.post("/v1/chat/completions")
    async def create_chat_completion(request: ChatRequest, api_key: str = Depends(auth.verify_api_key)):
        return {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": auth.get_user_id(api_key)}
    ```

4.  **Update test file `tests/test_api.py`:**
    -   Add tests for:
        -   **Missing API Key:** Send a request without the `Authorization` header and assert that the status code is 401.
        -   **Invalid API Key:** Send a request with an invalid API key in the `Authorization` header and assert that the status code is 401.
        -   **Valid API Key:** Send a request with a valid API key and assert that the status code is 200 and the response includes `"api_key_verified": true` and the correct `user_id`.

    ```python
    # tests/test_api.py
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    def test_chat_completion_endpoint_exists(): # Existing test, keep it
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": "user1"} # Updated assertion

    def test_missing_api_key():
        response = client.post("/v1/chat/completions", json={"model": "test-model", "messages": []})
        assert response.status_code == 401

    def test_invalid_api_key():
        headers = {"Authorization": "Bearer invalid_key"}
        response = client.post("/v1/chat/completions", json={"model": "test-model", "messages": []}, headers=headers)
        assert response.status_code == 401

    def test_valid_api_key():
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Endpoint is working", "request_model_valid": True, "api_key_verified": True, "user_id": "user1"} # Assertions for valid key
    ```

5.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_api.py` to execute the tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/auth.py` file.
-   [x] Step 2: Implement API Key Verification in `app/auth.py`.
-   [x] Step 3: Apply `verify_api_key` dependency to endpoint in `app/main.py`.
-   [x] Step 4: Update test file `tests/test_api.py` with authentication tests.
-   [ ] Step 5: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Rate Limiting (03-rate_limiting.md)

---