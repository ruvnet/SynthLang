# Phase 9: OpenAI Agents SDK and Tool Registry (09-agents_sdk_tool_registry.md)

## Objective
Integrate OpenAI Agents SDK for tool invocation (web search, file search) and implement a tool registry for pluggable tools.

## Steps

1.  **Create `app/agents` directory and necessary files:**
    -   Create `app/agents` directory.
    -   Create `app/agents/__init__.py` to make `app/agents` a Python package.
    -   Create `app/agents/registry.py` for the tool registry.
    -   Create `app/agents/tools` directory.
    -   Create `app/agents/tools/__init__.py` to make `app/agents/tools` a Python package.
    -   Create `app/agents/tools/web_search.py` for the web search tool.
    -   Create `app/agents/tools/file_search.py` for the file search tool (placeholder for now).

2.  **Implement Tool Registry in `app/agents/registry.py`:**
    -   Define `TOOL_REGISTRY = {}` dictionary to store registered tools.
    -   Implement `register_tool(name: str, tool_callable)` function:
        -   This function should register a tool in the `TOOL_REGISTRY` with the given `name` and `tool_callable` (the function to execute when the tool is invoked).
    -   Implement `get_tool(name: str)` function:
        -   This function should retrieve a tool from the `TOOL_REGISTRY` by its `name`. Return `None` if the tool is not found.

    ```python
    # app/agents/registry.py
    TOOL_REGISTRY = {} # Tool registry dictionary

    def register_tool(name: str, tool_callable):
        """Register a tool in the tool registry."""
        TOOL_REGISTRY[name] = tool_callable

    def get_tool(name: str):
        """Retrieve a tool from the registry by name."""
        return TOOL_REGISTRY.get(name)
    ```

3.  **Implement Web Search Tool in `app/agents/tools/web_search.py`:**
    -   Import `openai` and `os` modules.
    -   Implement `perform_web_search(user_message: str, options: dict = None) -> dict` function:
        -   This function will perform a web search using OpenAI's API.
        -   Initialize OpenAI client with API key (for now, placeholder API key or env var).
        -   Call `openai.ChatCompletion.create` with model "gpt-4o-search-preview" (or similar search-enabled model) and `web_search_options=options or {}`. Pass the `user_message` as the user's message.
        -   Return the `completion.choices[0].message`.
    -   Register the `perform_web_search` tool in the `TOOL_REGISTRY` using `register_tool("web_search", perform_web_search)` at the end of the file.

    ```python
    # app/agents/tools/web_search.py
    from openai import OpenAI
    import os
    from app.agents.registry import register_tool # Import register_tool

    # Placeholder API key, configure via env var later
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")) # Replace with your API key or env var

    def perform_web_search(user_message: str, options: dict = None) -> dict:
        """Perform web search using OpenAI API."""
        completion = client.chat.completions.create(
            model="gpt-4o-search-preview",  # or "gpt-4o-mini-search-preview" based on context
            web_search_options=options or {},
            messages=[{"role": "user", "content": user_message}],
        )
        return completion.choices[0].message

    register_tool("web_search", perform_web_search) # Register the tool
    ```

4.  **Implement File Search Tool (Placeholder) in `app/agents/tools/file_search.py`:**
    -   For now, implement a placeholder `perform_file_search` function that simply returns a message indicating "File search not implemented yet."
    -   Register the `perform_file_search` tool in the `TOOL_REGISTRY` using `register_tool("file_search", perform_file_search)` at the end of the file.
    -   File search implementation will be added in a later phase.

    ```python
    # app/agents/tools/file_search.py
    from app.agents.registry import register_tool # Import register_tool

    def perform_file_search(query: str, vector_store_id: str, max_results: int = 3) -> dict:
        """Placeholder: File search tool - not implemented yet."""
        return {"content": "File search not implemented yet."} # Placeholder response

    register_tool("file_search", perform_file_search) # Register the tool
    ```

5.  **Integrate Tool Registry in `app/llm_provider.py`:**
    -   Import `registry` from `app.agents`.
    -   In `complete_chat` and `stream_chat` functions in `app/llm_provider.py`:
        -   (For now, basic integration for testing) After model routing logic, add a simple tool invocation example:
            -   If the model is "gpt-4o-search-preview", invoke the "web_search" tool with the user message as input and return the tool's response instead of calling `openai.ChatCompletion.create`.
            -   This is just for basic integration testing. Actual agentic workflow will be implemented in later phases.

    ```python
    # app/llm_provider.py (update complete_chat and stream_chat)
    import os
    import openai
    from app.agents import registry # Import registry

    openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

    async def complete_chat(model: str, messages: list, temperature: float = 1.0,
                            top_p: float = 1.0, n: int = 1, user_id: str = None) -> dict:
        """Calls OpenAI ChatCompletion API (non-streaming) or invokes tool."""
        if "gpt-4o" in model:
            llm_model = "gpt-4o-search-preview"
            if "search-preview" in model: # Basic tool invocation for testing
                web_search_tool = registry.get_tool("web_search") # Get web_search tool
                if web_search_tool:
                    tool_response = web_search_tool(user_message=messages[-1]["content"]) # Invoke web_search with user message
                    return {"choices": [{"message": tool_response}], "usage": {}} # Return tool response as LLM response
                else:
                    print("Web search tool not found in registry.") # Log if tool not registered

        else:
            llm_model = "o3-mini"

        try: # Fallback to regular ChatCompletion if tool not invoked or for o3-mini
            response = openai.ChatCompletion.create(
                model=llm_model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=False
            )
            return response
        except Exception as e:
            print(f"LLM API call failed: {e}")
            raise

    async def stream_chat(model: str, messages: list, temperature: float = 1.0, # Update stream_chat similarly if needed for testing
                          top_p: float = 1.0, n: int = 1, user_id: str = None):
        """Calls OpenAI ChatCompletion API (streaming) or invokes tool (streaming not implemented for tools yet)."""
        if "gpt-4o" in model:
            llm_model = "gpt-4o-search-preview"
            if "search-preview" in model: # Basic tool invocation for testing (non-streaming for now)
                web_search_tool = registry.get_tool("web_search")
                if web_search_tool:
                    tool_response = web_search_tool(user_message=messages[-1]["content"])
                    return {"choices": [{"message": tool_response}], "usage": {}} # Return tool response as LLM response (non-streaming)
                else:
                    print("Web search tool not found in registry.")

        else:
            llm_model = "o3-mini"

        response_iter = openai.ChatCompletion.create( # Fallback to regular streaming ChatCompletion
            model=llm_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=True
        )
        async def stream_generator():
            for chunk in response_iter:
                yield chunk
        return stream_generator()

    def get_embedding(text: str) -> list: # Keep get_embedding as is
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response["data"][0]["embedding"]
        return embedding
    ```

6.  **Create test file `tests/test_agents.py`:**
    -   Create `tests/test_agents.py` for agent SDK and tool registry tests.

7.  **Write tests for Agent SDK and Tool Registry in `tests/test_agents.py`:**
    -   Test Tool Registry:
        -   **Tool Registration and Retrieval:** Test that `register_tool` registers a tool and `get_tool` retrieves it correctly.
        -   **Tool Not Found:** Test that `get_tool` returns `None` for a non-registered tool.
    -   Test Web Search Tool:
        -   **Web Search Tool Invocation:** Mock `openai.ChatCompletion.create` in `perform_web_search` to simulate a successful web search API call. Test that `perform_web_search` function returns a dictionary and does not raise an exception. Verify the response structure (e.g., check for "content" key in the message). (More detailed response validation can be added later).

    ```python
    # tests/test_agents.py
    from app.agents import registry
    from app.agents.tools import web_search, file_search # Import tools for testing
    from unittest.mock import AsyncMock, patch
    import pytest

    def test_tool_registry_register_and_get_tool():
        def dummy_tool():
            return "Tool executed"
        registry.register_tool("dummy_tool", dummy_tool) # Register dummy tool
        tool = registry.get_tool("dummy_tool") # Get the tool
        assert tool == dummy_tool # Check if retrieved tool is the same
        assert tool() == "Tool executed" # Check if tool execution works

    def test_tool_registry_get_tool_not_found():
        tool = registry.get_tool("non_existent_tool")
        assert tool is None # Check if None is returned for non-existent tool

    @pytest.mark.asyncio
    async def test_web_search_tool_invocation():
        # Mock openai.ChatCompletion.create for web_search tool
        mock_chat_completion_create = AsyncMock(return_value={"choices": [{"message": {"content": "Web search results"}}], "usage": {}})
        with patch("openai.ChatCompletion.create", new=mock_chat_completion_create):
            response = web_search.perform_web_search(user_message="test query") # Invoke web_search tool
            assert isinstance(response, dict) # Check if response is a dict
            assert "content" in response # Check for 'content' key in response message
            assert response["content"] == "Web search results" # Check response content
```

8.  **Update `tests/test_api.py` to test Agent SDK/Tool Registry integration in API endpoint:**
    -   In `test_chat_completion_endpoint_exists` and `test_valid_api_key`:
        -   For requests with `model="gpt-4o-search-preview"`, assert that the API endpoint now invokes the "web_search" tool (mock `registry.get_tool` and `web_search.perform_web_search` to verify tool invocation).
        -   For other models (e.g., "o3-mini"), assert that the API endpoint does not invoke the web search tool and falls back to regular LLM call (which is currently skipped in `app/main.py` for cache miss, so for now, just check no errors).

9.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_agents.py tests/test_llm_provider.py tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/agents` directory and files.
-   [x] Step 2: Implement Tool Registry in `app/agents/registry.py`.
-   [x] Step 3: Implement Web Search Tool in `app/agents/tools/web_search.py`.
-   [x] Step 4: Implement File Search Tool (Placeholder) in `app/agents/tools/file_search.py`.
-   [x] Step 5: Integrate Tool Registry in `app/llm_provider.py` (basic tool invocation).
-   [x] Step 6: Create test file `tests/test_agents.py`.
-   [x] Step 7: Write tests for Agent SDK and Tool Registry in `tests/test_agents.py`.
-   [x] Step 8: Update `tests/test_api.py` to test Agent SDK/Tool Registry integration in API endpoint.
    - [ ] Step 8.1: Test web_search tool invocation for "gpt-4o-search-preview" model.
    - [ ] Step 8.2: Test no tool invocation for other models ("o3-mini").
-   [ ] Step 9: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement API Streaming for LLM and Cache (10-api_streaming.md)

---