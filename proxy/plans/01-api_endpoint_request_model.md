# Phase 1: API Endpoint and Request Model (01-api_endpoint_request_model.md)

## Objective
Implement the basic FastAPI API endpoint for chat completions and define the Pydantic models for request validation.

## Steps

1.  **Create `app` directory and necessary files:**
    -   If not already present, create the `app` directory under `synthlang_router/`.
    -   Create `app/__init__.py` to make `app` a Python package.
    -   Create `app/main.py` for the FastAPI application.
    -   Create `app/models.py` for Pydantic models.

2.  **Define Pydantic Models in `app/models.py`:**
    -   Implement the `Message` model with `role` (Literal\["system", "user", "assistant"]) and `content` (str) fields.
    -   Implement the `ChatRequest` model with:
        -   `model` (str, required)
        -   `messages` (List\[Message], required)
        -   `stream` (Optional\[bool], default False)
        -   `temperature` (Optional\[float])
        -   `top_p` (Optional\[float])
        -   `n` (Optional\[int])

    ```python
    # app/models.py
    from pydantic import BaseModel, Field
    from typing import List, Literal, Optional

    class Message(BaseModel):
        role: Literal["system", "user", "assistant"]
        content: str

    class ChatRequest(BaseModel):
        model: str = Field(..., description="Model name (e.g., gpt-3.5-turbo)")
        messages: List[Message] = Field(..., description="Conversation messages")
        stream: Optional[bool] = False
        temperature: Optional[float] = None
        top_p: Optional[float] = None
        n: Optional[int] = None
    ```

3.  **Implement basic API endpoint in `app/main.py`:**
    -   Create a FastAPI application instance.
    -   Define a POST endpoint `/v1/chat/completions` that:
        -   Takes `ChatRequest` as input.
        -   For now, simply returns a placeholder JSON response to indicate it's working.

    ```python
    # app/main.py
    from fastapi import FastAPI

    app = FastAPI()

    @app.post("/v1/chat/completions")
    async def create_chat_completion(request: ChatRequest):
        return {"message": "Endpoint is working", "request_model_valid": True}
    ```

4.  **Create test file `tests/test_api.py`:**
    -   If not already present, create the `tests` directory under `synthlang_router/`.
    -   Create `tests/__init__.py` to make `tests` a Python package.
    -   Create `tests/test_api.py` for API endpoint tests.

5.  **Write basic test for API endpoint in `tests/test_api.py`:**
    -   Use `fastapi.testclient.TestClient` to create a test client for the FastAPI app.
    -   Write a test function `test_chat_completion_endpoint_exists` to:
        -   Send a POST request to `/v1/chat/completions` with a valid JSON body (according to `ChatRequest` model).
        -   Assert that the response status code is 200.
        -   Assert that the response JSON matches the placeholder response from the endpoint.

    ```python
    # tests/test_api.py
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    def test_chat_completion_endpoint_exists():
        headers = {"Authorization": "Bearer test_api_key_123"} # Placeholder header, auth not implemented yet
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Endpoint is working", "request_model_valid": True}
    ```

6.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_api.py` to execute the test.
    -   Ensure the test passes.

## Test-Driven Development Checklist

-   [x] Step 1: Create necessary files and directories.
-   [x] Step 2: Define Pydantic models in `app/models.py`.
-   [x] Step 3: Implement basic API endpoint in `app/main.py`.
-   [x] Step 4: Create test file `tests/test_api.py`.
-   [x] Step 5: Write basic test for API endpoint in `tests/test_api.py`.
-   [ ] Step 6: Run tests using Pytest and ensure they pass.

**Next Phase:** Implement API Key Authentication (02-authentication.md)

---