 
# SynthLang-Router: High-Speed LLM Proxy – Technical Specification

## Introduction  
A **high-speed LLM router and proxy** is a middleware service that sits between clients and large language model (LLM) providers (like OpenAI). Its goal is to **reduce latency, cut costs, and add enterprise features** (caching, multi-tenancy, security) while remaining compatible with the OpenAI API. This proxy will accept chat completion requests, optimize and compress prompts using SynthLang, check a semantic cache for similar past queries, and forward requests to the actual LLM if needed. It supports **streaming responses** (via Server-Sent Events) to deliver partial results with low latency. All interactions are logged and stored (with encryption) in a database for auditing. Key design features include:  

1. **Prompt Compression with SynthLang:** Uses the SynthLang CLI to compress/optimize user and system prompts, dramatically reducing token count and latency ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=To%20evaluate%20SynthLang%2C%20I%20implemented,workflows%20without%20choking%20on%20complexity)).  
2. **OpenAI-Compatible API Endpoints:** Exposes the same REST endpoints as OpenAI’s API (e.g. `/v1/chat/completions`), so existing OpenAI SDKs/clients work seamlessly. Supports optional streaming mode using SSE for real-time token output.  
3. **Vector Similarity Cache:** Integrates a semantic cache (using FAISS or Redis vector search) to reuse past responses for semantically similar queries, avoiding duplicate LLM calls ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=embeddings%20in%20in,confirming%20the)).  
4. **Multi-Tenancy & API Keys:** Supports multiple users via API key authentication (similar to OpenAI’s keys) and enforces optional per-user rate limits to prevent abuse.  
5. **Security & Privacy Features:** Encrypts all stored prompts and responses, performs audit logging of every API call, and can anonymize personally identifiable information (PII) in prompts/logs.  
6. **Persistent Storage:** Persists compressed prompts and final LLM outputs (along with metadata) in a **Supabase (Postgres) database** deployed on Fly.io. This provides a durable record for auditing, analytics, or retries.  
7. **Dockerized Deployment:** Delivered as a Docker container for easy deployment. Includes Fly.io-specific configuration (like a `fly.toml`) for running on Fly and scaling globally.  
8. **Test-Driven Implementation:** The project is developed with comprehensive tests (unit and integration) for prompt rewriting, caching logic, authentication, API proxying (including streaming), and database persistence.  
9. **Performance Optimization:** Emphasizes low-latency processing and cost efficiency through prompt token reduction, caching, asynchronous I/O, and careful resource management.  

This document details the system architecture, component designs, code examples, and test stubs for each major feature of the LLM proxy.

## Architecture Overview  
**System Architecture:** The LLM proxy consists of several components working in concert to handle requests efficiently: an API layer, a prompt optimizer, a cache, an LLM client, and persistence layers. When a request comes in, the flow is: **Client -> FastAPI Proxy -> (Prompt Optimizer -> Cache -> LLM API) -> Response -> Logging/DB**. The proxy is built with **FastAPI** (for web API and concurrency) and leverages **LiteLLM** to call underlying model APIs in a unified way. LiteLLM provides a Python SDK and FastAPI server that can call 100+ LLM APIs using the OpenAI API format ([LiteLLM: Call every LLM API like it's OpenAI [100+ LLMs] | Y Combinator](https://www.ycombinator.com/companies/litellm#:~:text=LiteLLM%20is%20an%20open,Combinator%2C%20Gravity%20Fund%20and%20Pioneer)), which allows easy routing to different model backends (OpenAI, Anthropic, etc.) if needed.  

Key components and their interactions:  
- **FastAPI API Layer:** Exposes REST endpoints (`/v1/chat/completions`) compatible with OpenAI’s API schema. It handles HTTP authentication (API keys), request validation (using Pydantic models), and response streaming.  
- **Prompt Optimizer (SynthLang):** A preprocessing step that compacts the system and user prompts using SynthLang’s token-efficient language. This dramatically reduces prompt size (e.g. 70%+ fewer tokens), cutting costs and latency ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=To%20evaluate%20SynthLang%2C%20I%20implemented,workflows%20without%20choking%20on%20complexity)). The optimized prompt retains the original meaning but in a concise form.  
- **Vector Similarity Cache:** An in-memory semantic cache of recent prompt→response pairs. Each incoming prompt is embedded into a vector; the cache is queried (via FAISS or a Redis vector index) for similar embeddings. If a high-similarity match is found, the cached response is returned immediately, bypassing the LLM call. This **semantic caching** can reduce redundant calls and latency significantly ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=embeddings%20in%20in,confirming%20the)).  
- **LLM Provider Client:** If no cache hit (or cache is disabled), the proxy forwards the (compressed) prompt to the target LLM API. This uses LiteLLM or an OpenAI SDK to call the model (e.g., GPT-4, GPT-3.5) and get a completion. Responses can be streamed token-by-token or collected fully.  
- **Security & Logging Layer:** All requests and responses are logged. Sensitive data can be masked out before logging. The content of prompts/responses is encrypted before being stored in the **Supabase Postgres** database. An audit log (with timestamp, user, endpoint, etc.) is maintained for every API call. Rate limiting (per API key) is enforced here if enabled.  
- **Persistence Layer:** A Postgres database (provided by Supabase on Fly.io) stores the optimized prompts, model responses, and metadata (user ID, model name, tokens used, etc.). This provides a history of interactions and enables analytics or fine-tuning data collection.  

## Prompt Optimization with SynthLang  
**Objective:** Reduce prompt token length and complexity using SynthLang, a hyper-efficient prompt language. By compressing verbose instructions into compact symbols, SynthLang can cut token usage dramatically (reports show 70–90% reduction in tokens, translating to major cost savings and speed gains ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=To%20evaluate%20SynthLang%2C%20I%20implemented,workflows%20without%20choking%20on%20complexity))). Both system messages (instructions) and user messages will be compressed before reaching the LLM. This ensures the LLM processes minimal text while preserving semantic meaning.

**SynthLang Overview:** SynthLang is a specialized prompt encoding that uses **logographic and symbolic compression** (inspired by languages like Kanji and Sanskrit) to pack meaning densely ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=the%20bottlenecks%20of%20verbose%20inputs%2C,is%20notoriously%20verbose%20by%20comparison)). For example, a long instruction like *“Analyze the current portfolio for risk exposure in five sectors and suggest reallocations”* might be encoded as a concise glyph sequence (as shown in the SynthLang documentation) ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=For%20instance%2C%20instead%20of%20saying%2C,safe)). This can slash the token count (e.g. by 70% or more) with only minimal overhead to decode it. The LLM can be instructed (via a system message) to interpret SynthLang glyphs, or SynthLang might rely on an external decoder before feeding to the LLM. In our design, we will use SynthLang primarily to compress text that the LLM will see, so the LLM must either be fine-tuned to understand SynthLang or we prepend a brief legend in a system message. In practice, an easier approach is to use SynthLang for *lossless compression*, then decompress back to English just before sending to the LLM (thus the LLM sees original content, but we saved tokens in transit/storage). We’ll consider both modes:
- **Mode 1:** LLM natively understands SynthLang tokens (requires the model to have been trained or prompted to understand SynthLang glyphs). If feasible, this yields maximum token savings end-to-end. 
- **Mode 2:** Use SynthLang as a compression buffer: compress prompt for caching/transit, but decompress to original text before final LLM call. This still saves cost on logging and any intermediate steps, though not on the final LLM call. 

For generality, we’ll implement Mode 2, assuming the LLM expects normal text. The proxy will compress the user input, use the compressed form for caching and storage, but will decompress it when sending to the LLM API (unless a future model can consume SynthLang directly).  

**Integration:** We use the **SynthLang CLI** to perform compression. The CLI can be invoked via a subprocess call from our FastAPI app. To minimize overhead, we might preload or warm up the SynthLang process. If performance is an issue, consider running the SynthLang service separately and calling it via an API or using an in-memory library function. For now, assume the CLI call is fast enough (it was designed for high performance, claiming 900% speedups in generation ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=token%20costs%20by%2090,up%20AI%20responses%20by%20900))). 

**Code Example – Prompt Compression:** Below is a helper function in `app/synthlang.py` that compresses a given text prompt using the SynthLang CLI. We assume the SynthLang CLI is installed and available in PATH as `synthlang` (with a command or flag for compression). 

```python
# app/synthlang.py

import subprocess
import shlex

# Optionally, we might have a toggle to disable SynthLang for debugging or if CLI is unavailable.
ENABLE_SYNTHLANG = True

def compress_prompt(text: str) -> str:
    """Compress a prompt using SynthLang CLI. Returns the compressed text."""
    if not ENABLE_SYNTHLANG:
        return text  # no compression if disabled
    try:
        # Run the synthlang CLI; for example, assume it reads from stdin and outputs compressed text
        proc = subprocess.run(
            ["synthlang", "compress"],  # hypothetical command
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        compressed = proc.stdout.strip()
        return compressed if compressed else text
    except Exception as e:
        # In case of any error, fallback to original text (and log the error)
        print(f"[SynthLang] Compression error: {e}")
        return text
```

This function would be called for each user message and system message in a chat request. The compression ratio is expected to be high – potentially shrinking large prompts by a factor of 3-5x or more ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=To%20evaluate%20SynthLang%2C%20I%20implemented,workflows%20without%20choking%20on%20complexity)). We will also provide a corresponding `decompress_prompt` if we need to revert to plain text (for Mode 2 as discussed). If Mode 1 (LLM understands SynthLang directly) is used, we’d instead ensure the system prompt instructs the LLM how to interpret SynthLang tokens.

**Example Usage:** If a user message is `"Explain the implications of the new tax policy on small businesses in simple terms."`, `compress_prompt()` might return a SynthLang-encoded string like `"税→SMB: impact, simplify?"` (hypothetical encoding). The content carries the same meaning but with far fewer characters/tokens. This compressed string is what we would use for caching and storage. Before calling the LLM, we might decompress it back or include a system note to interpret SynthLang. 

**Testing Prompt Optimization:** We will implement tests to ensure compression works and is beneficial. For example, in `tests/test_prompt_rewriting.py`:

```python
# tests/test_prompt_rewriting.py

from app.synthlang import compress_prompt

def test_compress_prompt_shortens_text():
    original = "Analyze the current portfolio for risk exposure in five sectors and suggest reallocations."
    compressed = compress_prompt(original)
    # The compressed version should be significantly shorter but not empty or identical
    assert isinstance(compressed, str) and compressed != ""
    assert len(compressed) < len(original) * 0.8  # expecting more than 20% reduction in length
    # (If SynthLang is deterministic, we could also test equality to an expected string pattern.)
```

This test verifies that `compress_prompt` returns a shorter string while preserving content (we might not decode it here, but if we had a decompress, we could check round-trip integrity). We also test edge cases (empty string, very short prompt, extremely long prompt) and that disabling SynthLang returns the original text unchanged.

## OpenAI-Compatible API & Streaming  
The proxy implements an **OpenAI-compatible REST API** so that any client code using OpenAI’s SDK can talk to this proxy without changes. Specifically, we will implement the **Chat Completions API** (`POST /v1/chat/completions`) as it covers our use-case. The request/response formats, status codes, and streaming behavior will mimic OpenAI. This includes support for **streaming responses** via Server-Sent Events (SSE) when the client sets `stream: true` in the request.

### API Endpoint Design  
We use **FastAPI** to define the endpoints. FastAPI’s Pydantic models will enforce the expected schema. For example, an OpenAI ChatCompletion request has a JSON body with fields like `model`, `messages`, `temperature`, `n`, `stream`, etc. We’ll define a Pydantic model for the incoming request (and possibly for the response if needed). We will handle only the fields necessary for our proxy functionality; unknown fields can be forwarded transparently to the underlying API.

**Pydantic Request Model (`app/models.py`):**  
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
    stream: Optional[bool] = False  # whether to stream the response
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    # ... (other OpenAI parameters can be added as needed)
```

This model ensures the incoming JSON has the required shape. The `messages` list will typically include one or more messages, with at least a user message (and often a system message for instructions). The proxy can inject its own system message if needed (for SynthLang decoding instructions, etc.).

**FastAPI Endpoint (`app/main.py` or `app/api.py`):**  
```python
# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.models import ChatRequest
from app import auth, synthlang, cache, llm_provider, db

app = FastAPI()

@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatRequest,
    api_key: str = Depends(auth.verify_api_key)  # dependency to authenticate user
):
    user_id = auth.get_user_id(api_key)  # assume we can get user or tenant ID from key
    # Rate limiting check
    if not auth.allow_request(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # 1. Prompt Compression
    compressed_messages = []
    for msg in request.messages:
        comp_content = synthlang.compress_prompt(msg.content) if msg.role in ("user", "system") else msg.content
        compressed_messages.append({"role": msg.role, "content": comp_content})
    # (If using Mode 2 as discussed, we will decompress before final LLM call; store compressed for caching.)
    
    # 2. Semantic Cache Lookup
    cache_key = cache.make_cache_key(compressed_messages, request.model)
    cached_response = cache.get_similar_response(cache_key)
    if cached_response:
        # If streaming was requested, we need to stream the cached response as chunks.
        if request.stream:
            def yield_cached():
                # Simulate SSE stream by yielding cached content as a single message or in parts
                # We chunk the cached response into at least one "data" event.
                yield f"data: {cached_response}\n\n"
                yield "data: [CACHE_END]\n\n"
            return StreamingResponse(yield_cached(), media_type="text/event-stream")
        else:
            # Non-streaming: return full response JSON similar to OpenAI's
            return {"id": "cached-resp", "object": "chat.completion", 
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": cached_response}, "finish_reason": "stop"}]}
    # 3. No cache hit: call LLM API via LiteLLM or OpenAI
    # If needed, decompress SynthLang in messages here for LLM call:
    final_messages = []
    for msg in compressed_messages:
        if msg["role"] in ("user", "system"):
            # decompress if using Mode 2
            final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
        else:
            final_messages.append(msg)
    # Prepare call to LLM (using liteLLM or openai library)
    try:
        if request.stream:
            # Use liteLLM or OpenAI with stream=True
            # For example, using OpenAI python sdk (if supporting our chosen model provider):
            import openai  # (assuming openai API is being proxied)
            openai.api_key = llm_provider.get_provider_api_key(request.model, user_id)
            response_iter = openai.ChatCompletion.create(model=request.model, messages=final_messages, stream=True, temperature=request.temperature or 1.0, top_p=request.top_p or 1.0, n=request.n or 1)
            def stream_generator():
                for chunk in response_iter:
                    # Each chunk is a partial message delta
                    if chunk['choices'][0].get('delta'):
                        content_piece = chunk['choices'][0]['delta'].get('content', '')
                        # Yield as SSE data events
                        yield f"data: {content_piece}\n\n"
                # Signal end of stream
                yield "data: [DONE]\n\n"
            # StreamingResponse will keep the connection open and send chunks as they are generated
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            # Non-streaming: one-shot call
            result = llm_provider.complete_chat(model=request.model, messages=final_messages, temperature=request.temperature, top_p=request.top_p, n=request.n)
            # `result` is expected to contain the assistant's reply in result["choices"][0]["message"]["content"]
            assistant_msg = result["choices"][0]["message"]["content"]
            # Format as OpenAI API response
            response_payload = {
                "id": result.get("id", ""),
                "object": "chat.completion",
                "created": result.get("created", 0),
                "model": request.model,
                "usage": result.get("usage", {}),
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": assistant_msg},
                        "finish_reason": result["choices"][0].get("finish_reason", "stop")
                    }
                ]
            }
            # Fall through to after try: we will log and cache below
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM provider call failed: {e}")
    # 4. (for non-streaming) Cache and persist result, then return JSON
    assistant_content = assistant_msg  # from above
    # Add to cache
    cache.store(cache_key, assistant_content)
    # Log & persist in DB (async)
    db.save_interaction(user_id, request.model, compressed_messages, assistant_content, cache_hit=False)
    return JSONResponse(content=response_payload)
```

In the above code, we outline the core logic: 
1. **Authentication & Rate limiting:** Handled via FastAPI dependencies (`verify_api_key` and `allow_request` logic in `app/auth.py`, see next sections for details). If the request exceeds rate limits, we return HTTP 429. 
2. **Prompt Compression:** We iterate over each message in the conversation and compress its content if it’s a user or system message. We leave assistant messages (from prior turns, if provided) unchanged. We collect these into `compressed_messages`. (Note: In a typical chat completion request, the user provides all prior messages including the assistant’s last reply if continuing a conversation. We compress only the actual text parts we are about to send again.)
3. **Cache Lookup:** We generate a `cache_key` or embedding for the conversation. A simple approach is to embed the latest **user question** only (as that is usually what we want to semantically match) – more on caching strategy later. If a similar query exists in cache, we immediately return the cached answer. For streaming requests, we simulate a stream by chunking the cached result (and mark it with a special `[CACHE_END]` or similar). For non-stream, we directly return the JSON payload containing the cached answer. In either case, we identify it as cached (for debugging, e.g. using an `"id": "cached-..."` or adding a custom header, though not strictly needed).
4. **LLM API Call:** If no cache hit, we proceed to call the actual LLM. We use either the OpenAI SDK or LiteLLM’s client. The example shows using OpenAI’s Python SDK for simplicity (in practice, LiteLLM’s abstraction could be used to support multiple providers). We pass the **decompressed** messages if we had compressed them (ensuring the model gets full text). We handle both streaming and non-streaming cases:
   - For streaming, we iterate over the streaming response from OpenAI and forward each chunk as an SSE `data:` event. We terminate the stream with a `[DONE]` event or simply by closing the connection as OpenAI does. In SSE, each message is prefixed with `data: ` and an empty line denotes the message boundary.
   - For non-streaming, we get the full response and package it into a JSON matching OpenAI’s format (including usage, choices, etc.).  
5. **Caching & Persistence:** After obtaining the LLM’s answer (for non-stream responses), we store the question→answer pair in our semantic cache for future reuse. We then asynchronously (or synchronously at the end of request) log the interaction to the database via `db.save_interaction`. In streaming mode, caching and DB logging can be done once the stream is finished (since we have to collect the response content as it streams; we could accumulate it or rely on the underlying SDK’s events that indicate end of completion). Logging can also record that it was a stream and how many tokens were streamed.

**Note:** The actual implementation might structure this logic differently (e.g., break into smaller functions for readability). But this outline covers the main functionality.

**Streaming via SSE:** The use of `StreamingResponse` in FastAPI allows sending incremental data. We specify `media_type='text/event-stream'`. The `stream_generator()` yields strings that are sent as chunks. We prefix each chunk with `data: ` to comply with SSE format. Clients (like browsers or OpenAI SDK if adapted) will receive these as stream events. We ensure to send the terminating event. Optionally, we could also send periodic heartbeat comments (`: ping\n\n`) to keep the connection alive; this is sometimes done but not strictly required if data flows quickly.

**Testing API and Streaming:** We will write tests to ensure the API behaves like OpenAI’s. For example, using FastAPI’s TestClient, we can simulate requests:

```python
# tests/test_api_proxy.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_completion_non_stream(monkeypatch):
    # Monkeypatch the LLM provider to avoid actual external API call
    async def fake_complete_chat(model, messages, **kwargs):
        return {
            "id": "test-id",
            "choices": [{"message": {"content": "Hello there!"}, "finish_reason": "stop"}],
            "created": 1234567890,
            "model": model,
            "usage": {"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7}
        }
    monkeypatch.setattr(app.llm_provider, "complete_chat", fake_complete_chat)
    # Use a dummy API key that passes auth
    headers = {"Authorization": "Bearer test_api_key_123"}
    req_body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False
    }
    res = client.post("/v1/chat/completions", json=req_body, headers=headers)
    data = res.json()
    assert res.status_code == 200
    # Check structure
    assert "choices" in data and data["choices"][0]["message"]["content"] == "Hello there!"

def test_chat_completion_stream(monkeypatch):
    # Monkeypatch the OpenAI stream response
    class DummyStream:
        def __iter__(self):
            # Simulate two chunks and then end
            yield {"choices": [{"delta": {"content": "Hello"}}]}
            yield {"choices": [{"delta": {"content": " world"}}]}
            yield {}  # end of stream (simulate no 'delta')
    async def fake_stream_chat(*args, **kwargs):
        return DummyStream()
    monkeypatch.setattr(app.openai.ChatCompletion, "create", fake_stream_chat)
    headers = {"Authorization": "Bearer test_api_key_123"}
    req_body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": True
    }
    res = client.post("/v1/chat/completions", json=req_body, headers=headers, stream=True)
    # The response should be a streaming response (status code 200, no JSON, chunks available)
    assert res.status_code == 200
    # Combine streamed chunks
    streamed_text = ""
    for chunk in res.iter_lines(decode_unicode=True):
        if chunk:  # filter heartbeat empty lines
            assert chunk.startswith("data: ")
            # Remove "data: " prefix and combine content
            streamed_text += chunk.replace("data: ", "")
    assert "Hello world" in streamed_text
```

These tests use monkeypatching to simulate the LLM provider, so we don’t call external APIs in tests. The non-stream test verifies that a correct JSON structure is returned and the content is as expected. The stream test reads the event stream and reconstructs the message to ensure the streaming works chunk by chunk. We would also test error cases (e.g., invalid API key returns 401, exceeding rate limit returns 429, invalid request fields return 400, etc., which will be covered in authentication tests).

## Vector Similarity Cache (Semantic Caching)  
To minimize repeated LLM calls, the proxy implements a **vector similarity cache**. The idea is to cache prior question→answer results such that if a new query is semantically similar to a past query, we can return the previous answer immediately ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=Building%20upon%20these%20ideas%2C%20we,API%20call%20to%20the%20LLM)) ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=)). This technique reduces latency (no call to external API) and saves cost on LLM usage ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=)). Unlike a traditional cache (exact string match), we use embeddings to capture semantic meaning, enabling matches even if wording differs (e.g., “What is the capital of Brazil?” vs “Can you tell me the capital of Brazil?” should hit the same answer). 

 ([Semantic Cache: Accelerating AI with Lightning-Fast Data Retrieval - Qdrant](https://qdrant.tech/articles/semantic-cache-ai-data-retrieval/)) *Semantic caching matches queries by meaning rather than exact text. In the illustration above, two differently phrased questions map to the same stored answer (“Brasília”). By comparing new queries to cached ones via embeddings, the proxy can serve answers to rephrased queries without a new LLM call.* 

### Cache Implementation Choices  
We have two primary options for the vector store:
- **In-Memory FAISS:** FAISS is a high-speed similarity search library. We can use FAISS to store embeddings in memory (or disk) and perform k-NN searches for each new query. FAISS is efficient in C++ and can handle large volumes of vectors. This is suitable if the cache is primarily in-memory and resets on restart (though we could persist the index to disk periodically).
- **Redis Vector Store:** Newer versions of Redis (with the RedisAI or RediSearch module) support vector similarity search natively. Alternatively, we can store embeddings in Redis as a key (embedding) and use an approximate nearest neighbor library or brute force search on retrieval. Redis offers persistence and easy sharing across multiple app instances (good for distributed environments). 

For simplicity and speed, we’ll start with an in-process FAISS index. In a multi-instance deployment, we might use Redis or a shared vector DB so that cache is global across instances (on Fly.io, if scaling horizontally, a Redis instance could be used as a centralized cache).

### What to Cache  
A key question is *what part of the conversation to embed for caching*. Options:
- **Embed the entire conversation context (system + all messages)**: This captures full context but slight differences in any part (like user name mentioned) could reduce similarity. It’s high-dimensional and might be overkill.
- **Embed only the latest user query (and maybe the system role)**: Most semantic caching focuses on the user’s question itself, since that usually determines the answer. We assume if the user asks essentially the same question, even in a different conversation, we can reuse the answer (which might not include context from previous turns though). Since our proxy might be stateless per request (unless we allow multi-turn context), focusing on the user prompt is reasonable.
- **Embed a truncated representation**: Some caches use a hashed or summarized version of the prompt. But using embeddings directly is more flexible.

We will **embed the user’s prompt (after compression)** as the cache key. We also consider the model name as part of the key, since different models might produce different style answers or knowledge cutoff. So, the cache key conceptually is (model, embedded_user_prompt). In code, we can maintain a FAISS index of vectors and a parallel list of (model, answer) pairs or a lookup structure.

### Using FAISS  
We’ll initialize a FAISS index for cosine similarity (or L2). Assuming we use OpenAI’s embedding (e.g., 1536-d vector for text-embedding-ada-002) or another embedding model via LiteLLM. We need a function to get embeddings for a given text. We can use LiteLLM’s embedding API which wraps many providers, or directly call OpenAI’s embedding endpoint if available. (Since this is a proxy in front of OpenAI, calling OpenAI’s embed API for caching somewhat eats into cost savings, but embedding is cheaper than a completion. Alternatively, we could use a local embedding model or a small transformer for this task to avoid external calls. For now, assume we use OpenAI embeddings to ensure good semantic representation.)

**Cache Data Structures (`app/cache.py`):**  
```python
# app/cache.py

import faiss
import numpy as np
from typing import Optional, Tuple

# Dimension of embeddings (e.g., 1536 for OpenAI's ada-002)
EMBED_DIM = 1536
# FAISS index (in-memory) and storage for responses
_index = faiss.IndexFlatIP(EMBED_DIM)  # using Inner Product (cosine if vectors normalized)
_stored_embeddings = []  # list of numpy vectors (to reconstruct index if needed)
_cached_pairs = []  # list of tuples (embedding_id, model, answer)

# Threshold for considering a cache hit (cosine similarity)
SIMILARITY_THRESHOLD = 0.9

def get_embedding(text: str) -> np.ndarray:
    """Get embedding vector for the given text using an embedding model."""
    # For demonstration, this might call an external API or local model.
    # Here we assume a function llm_provider.get_embedding exists.
    vector = llm_provider.get_embedding(text)  # returns a list[float] of length EMBED_DIM
    # Convert to numpy array
    vec = np.array(vector, dtype='float32')
    # Normalize vector for cosine similarity (so dot == cosine)
    faiss.normalize_L2(vec.reshape(1, -1))
    return vec

def make_cache_key(messages: list, model: str) -> Tuple[str, np.ndarray]:
    """Derive an embedding-based key for caching from the conversation messages and model."""
    # We will embed the last user message content
    user_content = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_content = msg["content"]
            break
    if not user_content:
        return None  # no user content found
    emb = get_embedding(user_content)
    return model, emb

def get_similar_response(cache_key: Tuple[str, np.ndarray]) -> Optional[str]:
    """Check cache for a semantically similar query. Returns the cached answer if hit."""
    if cache_key is None:
        return None
    model, emb = cache_key
    if _index.ntotal == 0:
        return None  # empty cache
    # Search in FAISS index
    D, I = _index.search(emb.reshape(1, -1), k=1)
    # I is the index of nearest neighbor, D is distance (similarity since normalized)
    if I[0][0] == -1:
        return None
    sim_score = D[0][0]
    if sim_score >= SIMILARITY_THRESHOLD:
        idx = I[0][0]
        cached_model, answer = _cached_pairs[idx][1], _cached_pairs[idx][2]
        if cached_model == model:
            return answer
    return None

def store(cache_key: Tuple[str, np.ndarray], answer: str):
    """Store a new Q/A pair in the cache."""
    if cache_key is None:
        return
    model, emb = cache_key
    idx = _index.ntotal  # next index position
    _stored_embeddings.append(emb)
    _cached_pairs.append((idx, model, answer))
    # Add to FAISS index
    _index.add(emb.reshape(1, -1))
```

In this code:
- We maintain `_cached_pairs` which holds entries of the form `(id, model, answer)`. The `id` corresponds to the index in the FAISS index (which is just an incremental counter in this simple setup).
- We normalize embeddings so that using `IndexFlatIP` (inner product) effectively gives cosine similarity. We require a similarity above 0.9 to count as a hit (this threshold can be tuned).
- `make_cache_key` finds the last user message’s content to represent the query. We might refine this to include system instructions if they drastically change answer, but often the user question is enough.
- On a query, `get_similar_response` searches for the nearest neighbor in the vector space. If the top hit has a high similarity and the model matches, we return the cached answer.
- `store` adds a new embedding and answer to the index and cache list. (We assume the number of cached items is manageable; in production we might want to cap the cache size or periodically remove old entries. This could be extended with an LRU policy or time-based eviction.)

**Note:** Instead of `IndexFlatIP`, we could use `IndexIVFFlat` (inverted file) or HNSW index for scalability if needed. Also, using `faiss.IndexFlatL2` with normalized vectors achieves same result as `IP` with pre-normalization. The above is a simple approach.

With Redis, the approach would differ (we might use a Redis vector store via `redis-py` and its `FT.SEARCH` with vector similarity, or a library like **GPTCache** which abstracts this). However, FAISS is self-contained for our purposes.

**Testing the Cache:** We need to verify that semantically similar inputs hit the cache. This is tricky to test without real embeddings; we can stub `get_embedding` to produce known vectors. For example, treat identical text as identical vector and different text as orthogonal vector for a simplistic test.

```python
# tests/test_cache.py

from app import cache

def test_cache_hit_and_miss(monkeypatch):
    # Monkeypatch cache.get_embedding to return deterministic small vectors for test
    test_vectors = {
        "Hi": np.array([1.0, 0.0], dtype='float32'),
        "Hello": np.array([0.9, 0.1], dtype='float32'),
        "Bye": np.array([0.0, 1.0], dtype='float32'),
    }
    monkeypatch.setattr(cache, "EMBED_DIM", 2)
    monkeypatch.setattr(cache, "_index", faiss.IndexFlatIP(2))
    monkeypatch.setattr(cache, "get_embedding", lambda text: test_vectors[text])

    # Store a question-answer pair
    model = "test-model"
    key = cache.make_cache_key([{"role": "user", "content": "Hi"}], model)
    cache.store(key, "Hello there!")  # answer for "Hi"

    # Now query with a semantically similar prompt "Hello"
    key2 = cache.make_cache_key([{"role": "user", "content": "Hello"}], model)
    ans = cache.get_similar_response(key2)
    assert ans == "Hello there!"  # should retrieve cached answer due to similarity

    # Query with a different prompt "Bye"
    key3 = cache.make_cache_key([{"role": "user", "content": "Bye"}], model)
    ans2 = cache.get_similar_response(key3)
    assert ans2 is None  # different vector, should be a miss
```

In this test, we simulate embedding vectors in 2D for simplicity. "Hi" and "Hello" are made similar, so the cache returns the stored answer for "Hi" when asked "Hello". "Bye" is different and yields no hit. This verifies the caching logic at a high level.

Additionally, we should test that the cache does not return an answer for a different model or below threshold. We can also test that after a cache miss (which triggers an LLM call in integration), the store function indeed makes the next similar query a hit.

**Cache and Cost Savings:** By using this semantic cache, we expect to save a significant fraction of calls. Research has shown that caching can eliminate a large portion of redundant queries (e.g., one approach achieved ~60–68% cache hit rates with corresponding cost reductions ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=optimizing%20LLM,powered%20applications))). Even if our threshold is high (to ensure answer relevance), any repeated queries from the same user or across users will hit, benefiting multi-tenant scenarios where different users ask similar questions. 

One must be cautious: if the knowledge might have changed or if answers could become outdated, cache entries might need an expiration. For our initial design, we will keep it simple and potentially add a TTL for cached entries configurable (or allow manual cache flush). In a dynamic knowledge environment, integration with Retrieval Augmented Generation might be needed, but that’s out of scope here.

## Multi-Tenancy: API Keys and Rate Limiting  
The proxy is designed for **multi-tenant use**, meaning multiple users or clients can use it simultaneously with isolation. We achieve this via **API key authentication**, similar to how OpenAI issues secret API keys to users. Each request must include a valid API key to be processed. Additionally, we can enforce **per-user rate limits** to prevent abuse or to throttle usage based on subscription levels.

### API Key Authentication  
We’ll implement an API key system as follows:
- The proxy will expect an `Authorization` header with value `Bearer <API_KEY>` on each request (just like OpenAI’s API). Alternatively, a query parameter `api_key=<KEY>` could be supported for convenience (though less secure in GET logs, etc.).
- We will maintain a list or database table of valid API keys and their associated user or tenant identifiers, along with possibly permissions or rate limit settings.
- A FastAPI dependency (`verify_api_key`) will check the header, verify the key, and if valid, allow the request to proceed (attaching the user identity in context). If invalid or missing, it will return a 401 Unauthorized.

**API Key Storage:** For simplicity, we might start with an in-memory dictionary or a config file mapping keys to users (especially in testing). In production, a database table `users(api_key, user_id, ... , rate_limit)` would be used. Since we already have a Supabase Postgres, we can store user records there and load them into memory on startup or query on each request (with caching).

**Example auth implementation (`app/auth.py`):**  
```python
# app/auth.py

from fastapi import Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS
import time

# Example in-memory API key store (in practice, replace with DB lookup)
API_KEYS = {
    "sk_test_user1": {"user_id": "user1", "rate_limit_qpm": 60},  # 60 requests per minute
    "sk_test_user2": {"user_id": "user2", "rate_limit_qpm": 5},   # e.g., a low rate limit user
}
# Simple rate-limiter data: track requests in current minute for each user
_request_counts = {}  # {user_id: (window_start_timestamp, count)}

def verify_api_key(authorization: str = Header(...)):
    """FastAPI dependency to verify the provided API key and return the API key if valid."""
    if not authorization or not authorization.startswith("Bearer "):
        # No auth provided
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing API key")
    api_key = authorization.split(" ", 1)[1]
    if api_key not in API_KEYS:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

def get_user_id(api_key: str) -> str:
    """Retrieve user identifier from API key (assumes verify_api_key passed)."""
    return API_KEYS[api_key]["user_id"]

def allow_request(user_id: str) -> bool:
    """Implements a simple rate limiting: returns True if request is allowed for user, False if rate limit exceeded."""
    if user_id not in _request_counts:
        # initialize window for this user
        _request_counts[user_id] = [time.time(), 0]  # [window_start, count]
    window_start, count = _request_counts[user_id]
    limit = API_KEYS[next(k for k,v in API_KEYS.items() if v['user_id']==user_id)]["rate_limit_qpm"]
    current_time = time.time()
    # Reset count if a minute has passed
    if current_time - window_start > 60:
        _request_counts[user_id] = [current_time, 0]
        return True
    if count < limit:
        _request_counts[user_id][1] += 1
        return True
    else:
        return False
```

In this snippet:
- `API_KEYS` is a dict with API key strings mapping to a user record (with user_id and rate limit info). In practice, this might be loaded from an environment variable or DB on startup.
- `verify_api_key` is intended to be used with FastAPI’s `Depends`. It extracts the API key and validates it. On success, it returns the `api_key` (which gets passed to the route function).
- `get_user_id` then maps that key to an internal user ID (which might be used for logging or DB storage).
- `allow_request` implements a basic **token bucket** or fixed-window rate limiter per user. This one uses a fixed 60-second window for simplicity. If the user has remaining quota in the current minute, it increments count and returns True; if not, returns False. A more robust implementation might use an external store or the `fastapi-limiter` package which integrates with Redis for distributed rate limiting.

We should ensure thread-safety of `_request_counts` if using in async context (though FastAPI single-thread per request should be fine, but multiple workers might conflict — using a lock or using an atomic Redis counter is more robust).

**Testing Authentication & Rate Limits:** We will have tests that check that valid keys allow access and invalid ones are rejected, and that exceeding the limit yields 429:

```python
# tests/test_auth_rate_limit.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_missing_api_key():
    resp = client.post("/v1/chat/completions", json={"model":"gpt-3.5-turbo","messages":[]})
    assert resp.status_code == 401

def test_invalid_api_key():
    headers = {"Authorization": "Bearer invalid_key"}
    resp = client.post("/v1/chat/completions", json={"model":"x","messages":[]}, headers=headers)
    assert resp.status_code == 401

def test_valid_api_key_allows():
    headers = {"Authorization": "Bearer sk_test_user1"}
    resp = client.post("/v1/chat/completions", json={"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hi"}]}, headers=headers)
    # We expect a different error possibly because we didn't monkeypatch the LLM call here, but if everything was stubbed it would be 200.
    assert resp.status_code != 401  # Should not be unauthorized

def test_rate_limit_exceeded(monkeypatch):
    # Set a low rate limit for testing
    from app import auth
    auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 2  # allow only 2 per minute
    headers = {"Authorization": "Bearer sk_test_user1"}
    # First request
    res1 = client.post("/v1/chat/completions", json={"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Test"}]}, headers=headers)
    # Second request
    res2 = client.post("/v1/chat/completions", json={"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Test 2"}]}, headers=headers)
    # Third request should hit the limit
    res3 = client.post("/v1/chat/completions", json={"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Test 3"}]}, headers=headers)
    assert res3.status_code == 429
    # Clean up: reset rate limit
    auth.API_KEYS["sk_test_user1"]["rate_limit_qpm"] = 60
```

These tests ensure that:
- Without a key or with an incorrect key, we get a 401.
- With a valid key, the request goes through (the exact status might be 200 or something else depending on the rest of the pipeline, but it shouldn’t be 401).
- After sending more requests than allowed in the window, the next request returns 429 Too Many Requests.

**Expansion:** In a real setup, one might integrate `fastapi-limiter` which uses Redis to handle rate limiting in a distributed manner. This would remove the need for our manual `_request_counts`. But our approach suffices for demonstration and tests.

## Security & Privacy: Encryption, Logging, and PII Masking  
Security and privacy are first-class concerns for this proxy since it will handle potentially sensitive user data (prompts may include private or confidential info). We implement multiple layers of protection:

- **Encryption of Data at Rest:** All prompts and responses stored in the database are encrypted using a symmetric key. This ensures that even if the database is compromised or accessed by unauthorized parties, the content of prompts and responses remains confidential. Only the proxy service (with the key) can decrypt the data.
- **Audit Logging:** Every API call is logged with relevant metadata (timestamp, user ID, endpoint, prompt length, etc.). This log can be stored in the database or an append-only log file for audit purposes. Logging helps in monitoring usage, debugging issues, and detecting misuse. The logs should exclude raw sensitive data if possible or store references to encrypted entries.
- **PII Masking (Anonymization):** Optionally, the proxy will detect and redact PII (Personally Identifiable Information) from prompts and completions, especially before logging or sending to external LLM APIs. This can prevent sensitive identifiers (like emails, phone numbers, names) from leaving the proxy or being stored in plain form. 

 ([Removing PII Data from OpenAI API Calls with Presidio and FastAPI](https://ploomber.io/blog/pii-openai/)) *All sensitive data (e.g., email addresses, phone numbers) can be masked before processing. In the example above, the proxy replaces actual PII like “peter.doe@corporation.com” with placeholders like “<EMAIL_ADDRESS>” before forwarding to the LLM or saving logs.* This approach protects user privacy and can help comply with data protection regulations.

### Data Encryption  
We use symmetric encryption (e.g., AES) via a library like **Cryptography** (Fernet) to encrypt prompt and response text. We’ll have an encryption key (32-byte base64) set as an environment variable (e.g., `ENCRYPTION_KEY`). The proxy will use this key to create a Fernet cipher. Before saving any prompt or response to the database, it will encrypt it. When reading from DB (for any reason, e.g., future analysis), it can decrypt. Note that while encrypted in DB, we cannot do plaintext search on it – but that’s fine since we use embeddings for semantic search rather than DB text queries.

**Encryption Utility (`app/security.py`):**  
```python
# app/security.py

from cryptography.fernet import Fernet
import os

# Initialize Fernet cipher
FERNET_KEY = os.environ.get("ENCRYPTION_KEY")
if not FERNET_KEY:
    # If not provided, generate one (in practice, this should be set explicitly)
    FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

def encrypt_text(plain: str) -> bytes:
    """Encrypt text to bytes using Fernet symmetric encryption."""
    return cipher.encrypt(plain.encode('utf-8'))

def decrypt_text(token: bytes) -> str:
    """Decrypt bytes to text using Fernet."""
    return cipher.decrypt(token).decode('utf-8')
```

We will use `encrypt_text` before writing to DB, and `decrypt_text` when reading (if needed for audit display). Note that encryption keys must be kept secret – on Fly.io, we will store it as a secret env var.

### Audit Logging  
We want to log each request. We have a couple of levels of logging: 
- **Application logs:** using Python’s `logging` module, we can output logs for each request with key details. These can be streamed to stdout (and captured by Fly.io or any log aggregator).
- **Database logging:** We will store each interaction in the DB via `db.save_interaction` (see next section). This includes the user, model, prompt, response, token counts, cache usage, etc. This effectively serves as an audit log/history of all queries. Because prompts and responses may contain sensitive data, we *encrypt* them in this log table. Alternatively, if PII masking is enabled, the stored content might already have sensitive parts replaced with placeholders, adding another layer of safety.

To implement audit logging, we don’t need a separate mechanism beyond ensuring `db.save_interaction` is called for every request (cache hit or not). For cache hits, we may still log that a request was served from cache (with no LLM call). For streams, we log once the stream is completed (or started, with a marker that it was a stream). We may also log partially (like prompt immediately, and completion once ready).

Example logging (in `db.save_interaction`, to be elaborated in next section) might be:
```python
# in db.save_interaction (pseudocode)
encrypted_prompt = security.encrypt_text(full_prompt_text)
encrypted_response = security.encrypt_text(response_text)
# insert into interactions table (user_id, model, prompt_enc, response_enc, tokens_prompt, tokens_response, cache_hit, timestamp)
```
Additionally, using the `logging` module:
```python
import logging
logger = logging.getLogger("proxy")
logger.setLevel(logging.INFO)
...
logger.info(f"User {user_id} request model={model} prompt_tokens={p_tokens} completion_tokens={c_tokens} cache_hit={cache_hit}")
```
These logs can help monitor usage and performance. We would include such logging statements in appropriate places (after getting response, etc.).

### PII Masking (Anonymization)  
To protect sensitive user information, we include an **optional PII anonymization step**. If enabled (via a config flag), the proxy will scan the prompt (and possibly the LLM response) for PII and replace it with neutral placeholders before logging or sending out. Common PII includes:
- Email addresses
- Phone numbers
- Physical addresses
- Person names
- Credit card or account numbers

We can use **Microsoft Presidio**, an open-source library specialized for PII detection and anonymization. Presidio provides fast analyzers for PII entities (using regex, NLP, and context) and can replace them with generic tags ([GitHub - microsoft/presidio: Context aware, pluggable and customizable data protection and de-identification SDK for text and images](https://github.com/microsoft/presidio#:~:text=Presidio%20,numbers%2C%20financial%20data%20and%20more)). Alternatively, for simplicity, we might implement a basic version covering a few types using regex:
```python
import re
PII_PATTERNS = [
    (re.compile(r'[0-9]{3}-[0-9]{2}-[0-9]{4}'), '<SSN>'),  # simplistic SSN pattern
    (re.compile(r'\b\d{10}\b'), '<PHONE_NUMBER>'),  # 10-digit number
    (re.compile(r'\b\d{3}-\d{3}-\d{4}\b'), '<PHONE_NUMBER>'),  # phone 123-456-7890
    (re.compile(r'\S+@\S+\.\S+'), '<EMAIL_ADDRESS>'),  # email pattern
    (re.compile(r'\b[0-9]{16}\b'), '<CREDIT_CARD>')  # 16-digit number
]

def mask_pii(text: str) -> str:
    masked = text
    for pattern, placeholder in PII_PATTERNS:
        masked = pattern.sub(placeholder, masked)
    return masked
```
This is a naive implementation; Presidio would be more comprehensive (detecting names, etc., using NLP). For demonstration, this is acceptable. We would call `mask_pii` on user prompts before sending to the LLM (if we want to avoid sending real PII to OpenAI) and on responses before logging if needed. Note that masking before the LLM call could alter the answer (e.g., if the user asked the model to output someone’s email, it would instead see `<EMAIL_ADDRESS>`). This is a trade-off between privacy and functionality. A safer approach might be to mask only in logs, not in the query to the model, unless required. We make it configurable:
- `MASK_PII_BEFORE_LLM = False` (default) – do not alter the query sent to the model.
- `MASK_PII_IN_LOGS = True` (default) – mask PII in content that we store or log.

So, in code, we could do:
```python
if MASK_PII_BEFORE_LLM:
    for msg in final_messages:
        if "content" in msg:
            msg["content"] = mask_pii(msg["content"])
# ... after getting assistant_content:
if MASK_PII_IN_LOGS:
    log_prompt = mask_pii(full_prompt_text)
    log_response = mask_pii(assistant_content)
else:
    log_prompt = full_prompt_text
    log_response = assistant_content
# then encrypt log_prompt, log_response and save
```

We should expose these settings via config (env vars or config file) for flexibility.

**Testing PII Masking:** If we implement a simple mask function, we test it:

```python
# tests/test_pii.py

from app.security import mask_pii

def test_mask_pii_basic():
    text = "Contact John Doe at john.doe@example.com or 555-123-4567."
    masked = mask_pii(text)
    assert "john.doe@example.com" not in masked
    assert "555-123-4567" not in masked
    assert "<EMAIL_ADDRESS>" in masked and "<PHONE_NUMBER>" in masked

def test_mask_pii_no_false_positives():
    text = "This text has no PII."
    masked = mask_pii(text)
    assert masked == text  # unchanged
```

This ensures that emails and phone numbers are replaced, and that normal text is unaffected.

## Persistence with Supabase (Postgres)  
All optimized prompts and final responses are stored in a **Postgres database** for persistence. We use Supabase (a hosted Postgres solution) deployed on Fly.io. The database will have at least one table for chat interactions. Each row can contain:
- A unique ID
- User ID (foreign key to a users table if needed)
- Model name
- Compressed prompt (encrypted)
- LLM response (encrypted)
- Whether it was a cache hit or a real LLM call
- Token usage metadata (prompt tokens, response tokens, total cost maybe)
- Timestamp

Storing this data serves multiple purposes:
- **Audit trail:** record of what was asked and answered, by whom, when.
- **Analytics:** one can analyze usage patterns, most common queries, etc.
- **Cache Warm Start:** theoretically, we could pre-populate the cache from the DB on startup, or share data between instances.
- **User history:** if the application wants to show users their past queries, it can decrypt and display them (with proper permission checks).

We will use an **async database client** since FastAPI is async. Possible choices: SQLAlchemy (with async extension), `asyncpg` directly, or Supabase’s Python client (which is essentially a wrapper but we can use standard SQL for simplicity). We will illustrate with SQLAlchemy for structured interaction.

**Database Model:** Using SQLAlchemy (declarative):

```python
# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, DateTime, func

DATABASE_URL = os.environ.get("DATABASE_URL")  # e.g., "postgresql+asyncpg://user:pass@host/dbname"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    model = Column(String)
    prompt_enc = Column(LargeBinary)    # encrypted prompt
    response_enc = Column(LargeBinary)  # encrypted response
    cache_hit = Column(Boolean)
    prompt_tokens = Column(Integer)
    response_tokens = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
```

We define `prompt_enc` and `response_enc` as binary to hold the encrypted bytes from Fernet. The `user_id` and `model` are stored in plaintext for indexing/filtering (these are not particularly sensitive by themselves). Token counts and timestamp give useful info.

We will have to create this table in the database (via migrations or a simple create if not exists). In tests, we might use an in-memory SQLite for convenience, but since SQLite might not support LargeBinary well, we could adjust or skip encryption in tests.

**Saving Interactions:** Provide a function to save an interaction after it's processed:

```python
# app/db.py

from app.database import SessionLocal, Interaction
from app import security

async def save_interaction(user_id: str, model: str, messages: list, response_text: str, cache_hit: bool):
    """Save the interaction (prompt and response) to the database."""
    # Flatten the messages into one prompt text for storage (concatenate roles and content)
    prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    # Optional: mask PII in prompt_text and response_text if configured
    if security.MASK_PII_IN_LOGS:
        prompt_text = security.mask_pii(prompt_text)
        response_text = security.mask_pii(response_text)
    # Encrypt the prompt and response
    prompt_encrypted = security.encrypt_text(prompt_text)
    response_encrypted = security.encrypt_text(response_text)
    # Token counting (if the underlying LLM returned usage info or we can count ourselves via tiktoken)
    prompt_tokens = len(prompt_text.split())  # simplistic token count via words (placeholder)
    response_tokens = len(response_text.split())
    # Save to DB
    async with SessionLocal() as session:
        interaction = Interaction(
            user_id=user_id,
            model=model,
            prompt_enc=prompt_encrypted,
            response_enc=response_encrypted,
            cache_hit=cache_hit,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens
        )
        session.add(interaction)
        await session.commit()
```

This function takes the compressed messages list and the final response, then:
- Combines all messages into a single text blob for logging (including roles for clarity).
- Masks PII if configured to do so in logs.
- Encrypts the prompt and response.
- Estimates token counts (here we used a naive word count; in reality, we should use the same tokenizer as the model to count tokens properly. OpenAI returns this in the API, or we could use `tiktoken` library).
- Inserts a new record into the `interactions` table.

We should call `save_interaction` asynchronously (but since FastAPI can call async functions, that’s fine). If we don’t want to slow down the response, we could spawn it as a background task via `import asyncio; asyncio.create_task(save_interaction(...))` so that it doesn’t delay returning the response.

**Retrieving/Decrypting:** While not explicitly required, we could have a function to retrieve interactions for an audit or user interface, which would decrypt the prompt and response for reading. But in this scope, saving is the main part.

**Testing Persistence:** We can either use a real test database (requiring connection) or mock the DB calls. Given this is a design spec, we can outline a test stub:

```python
# tests/test_db.py

import asyncio
from app import db, database, security

# Use an in-memory SQLite for test (synchronous, to avoid needing a running Postgres)
# Overwrite SessionLocal for tests
database.engine = create_async_engine("sqlite+aiosqlite:///:memory:")
database.SessionLocal = sessionmaker(bind=database.engine, class_=AsyncSession, expire_on_commit=False)
# Create tables
asyncio.run(database.Base.metadata.create_all(bind=database.engine))

def test_save_and_retrieve_interaction():
    # Prepare dummy data
    user_id = "user1"
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
    response_text = "Hi"
    # Save the interaction
    asyncio.run(db.save_interaction(user_id, model, messages, response_text, cache_hit=False))
    # Retrieve it back
    async def get_last_interaction():
        async with database.SessionLocal() as session:
            result = await session.execute("SELECT user_id, model, prompt_enc, response_enc FROM interactions")
            row = result.fetchone()
            return row
    row = asyncio.run(get_last_interaction())
    assert row is not None
    db_user, db_model, prompt_enc, response_enc = row
    assert db_user == user_id and db_model == model
    # Decrypt and verify content
    prompt_text = security.decrypt_text(prompt_enc)
    response_text_dec = security.decrypt_text(response_enc)
    assert "user: Hello" in prompt_text  # roles and content included
    assert "assistant: Hi" in prompt_text
    assert response_text_dec == "Hi"
```

This test creates an in-memory SQLite database, creates the interactions table, then tests that saving an interaction indeed stores an encrypted record which can be decrypted correctly. We verify that the decrypted content matches the original messages.

In practice, one might separate the logic to easier unit test (for example, test that encryption and decryption are inverses with known input, test that mask_pii is applied, etc., rather than doing full DB integration). But the above gives an end-to-end idea.

## Deployment (Docker & Fly.io Configuration)  
The application is designed to be easily deployable via Docker. We will containerize the FastAPI app along with all required dependencies (FastAPI, uvicorn server, litellm, FAISS, etc.). The container can then be run on Fly.io. Fly.io uses a `fly.toml` for app configuration and supports scaling, secrets injection, etc. We’ll provide that as well.

### Project Structure  
We organize the code into a clear structure:
```
synthlang_router/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, routing and endpoints
│   ├── config.py               # Environment variables and constants
│   ├── models.py               # Pydantic models for requests/responses
│   ├── auth.py                 # API key authentication and rate limiting
│   ├── synthlang.py            # SynthLang CLI integration for prompt compression/decompression
│   ├── cache.py                # FAISS-based semantic cache implementation
│   ├── llm_provider.py         # LLM client with dynamic routing (GPT‑4o vs o3‑mini)
│   ├── security.py             # Encryption, PII masking, and audit logging utilities
│   ├── db.py                   # Database persistence functions (SQLAlchemy)
│   ├── database.py             # SQLAlchemy models and engine setup (Supabase/Postgres)
│   └── agents/                 # OpenAI Agents SDK integration
│       ├── __init__.py
│       ├── registry.py         # Tool registry for pluggable modules
│       └── tools/              # External tools
│           ├── __init__.py
│           ├── web_search.py   # Web search tool integration
│           └── file_search.py  # File search tool integration
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_cache.py
│   ├── test_db.py
│   ├── test_llm_provider.py
│   ├── test_synthlang.py
│   └── test_api.py
├── Dockerfile
├── fly.toml
├── requirements.txt
└── README.md

```

This structure groups related functionality. For example, `llm_provider.py` can use **LiteLLM** to route requests to the correct LLM API. It might read environment variables for API keys (e.g., OpenAI API key, etc.) or configuration about which provider to use for which model. We can also implement simple logic: if model name contains `"gpt-4"` use OpenAI, if `"llama"` use another, etc., or leave that to LiteLLM configuration.

**Sample Config (app/config.py):** This might parse environment variables or a YAML for things like:
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_SYNTHLANG = bool(int(os.getenv("USE_SYNTHLANG", "1")))
MASK_PII_BEFORE_LLM = bool(int(os.getenv("MASK_PII_BEFORE_LLM", "0")))
MASK_PII_IN_LOGS = bool(int(os.getenv("MASK_PII_IN_LOGS", "1")))
DEFAULT_RATE_LIMIT_QPM = int(os.getenv("DEFAULT_RATE_LIMIT_QPM", "60"))
# etc.
```
Also model routing if needed:
```python
MODEL_PROVIDER = {
    "gpt-3.5-turbo": "openai",
    "gpt-4": "openai",
    "claude-v1": "anthropic",
    # etc.
}
```
This could inform `llm_provider.py` how to handle each model. However, if using liteLLM, it may auto-detect by model name or allow specifying provider via an argument.

**Dockerfile:** For example:
```
FROM python:3.11-slim

# Install system packages (if needed for FAISS or others)
RUN apt-get update && apt-get install -y build-essential libaio-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/
COPY main.py .
# (Alternatively, if main is in app, adjust accordingly)

# Expose port
ENV PORT 8080
EXPOSE 8080

# Command to run the app (using Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```
In the above, we assume `app.main:app` is the ASGI app. We ensure all dependencies (fastapi, uvicorn, litellm, faiss-cpu, redis-py, cryptography, etc.) are in requirements.txt.

We might need to install FAISS via pip (`faiss-cpu`), and for Redis usage (if any) ensure `redis` library. Also, install `litellm` (`pip install litellm`).

**fly.toml:** A basic Fly.io config might look like:
```toml
app = "llm-proxy-app-name"  # replace with actual app name

[env]
  PORT = "8080"
  OPENAI_API_KEY = "sk-..."       # These could also be set via fly secrets
  ENCRYPTION_KEY = "base64key..." # Should be set via secrets for security
  DATABASE_URL = "[connection string]"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20
  [[services.ports]]
    handlers = ["http"]
    port = 80
  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```
This configuration sets the app port and optionally environment variables. Usually, one would run `fly secrets set OPENAI_API_KEY=...` etc. so they are not in plain text in the file.

We also ensure the service will accept HTTP on 80/443 and route internally to 8080 where uvicorn runs. The concurrency limits can be adjusted to tune how many simultaneous connections (streams) to allow per instance.

**Deployment Instructions:** 
1. Build the Docker image: `docker build -t llm-proxy .`
2. Test locally (if needed): `docker run -p 8080:8080 -e OPENAI_API_KEY=... -e ENCRYPTION_KEY=... llm-proxy`
3. Create and deploy on Fly: `fly launch` (if starting new) or `fly deploy` (for existing app).
4. Set secrets on Fly (API keys, DB URL, encryption key): `fly secrets set OPENAI_API_KEY=... ENCRYPTION_KEY=... DATABASE_URL=...`
5. Scale as needed: by default one instance, but can scale out with `fly scale count 2` or use Fly’s autoscaling.

Fly.io will take care of provisioning a Postgres if we use `fly postgres create` and attach it, giving a DATABASE_URL. If using Supabase’s hosted Postgres, then DATABASE_URL would be that connection string.

**Continuous Integration:** We also include a basic CI configuration (e.g., GitHub Actions YAML in `.github/workflows/ci.yml`) to run tests on each push. The CI would:
- Setup Python,
- Install dependencies,
- Run `pytest` to execute all tests in the `tests/` directory.
We won’t detail the YAML here, but will provide test stubs as we’ve done in this document. Ensuring tests pass gives confidence in each component.

## Monitoring & Observability  
To maintain and scale the service, monitoring is important. We will integrate basic observability features:
- **Metrics:** We can use Prometheus to scrape metrics. A library like `prometheus_fastapi_instrumentator` can automatically expose metrics for request count, latency, etc., at an endpoint (e.g., `/metrics`). We include this integration so that if deployed, a Prometheus server can pull metrics. On Fly.io, one could deploy a separate metrics collector or use a service like Grafana Cloud to scrape.
- **Logging:** As mentioned, we use structured logging for each request (including user, model, timing, tokens). These logs can be shipped to a logging service or watched via `fly logs`. They help detect errors or anomalies. We may include trace IDs in logs if needed.
- **Tracing:** Optionally, one could integrate OpenTelemetry to trace requests through the proxy and to the external LLM API. This might be advanced for now. 
- **Langfuse (optional):** Langfuse is a tool for LLM observability that tracks prompts and responses for debugging. If desired, we could integrate Langfuse SDK to send events about each request (prompt, response, latency, errors) to a Langfuse server for analysis. This is optional and mostly for debugging complex LLM apps.

For our implementation, we ensure that:
- The `/metrics` endpoint is not exposed to unauthorized users (maybe behind an auth or only internally accessible). But for simplicity, it could be open if not sensitive.
- We handle exceptions globally to return proper JSON errors and log them.

## Testing Strategy (TDD)  
We adopted a **Test-Driven Development** approach, writing tests for each major component as it’s designed. The test suite covers:
- **Prompt Compression (SynthLang):** Verify that prompts are being shortened and not losing content entirely.
- **API Proxying:** Ensure the FastAPI endpoints accept input and produce output in the correct format. This includes testing both streaming and non-streaming responses, and that streaming responses accumulate to the expected full answer.
- **Caching Logic:** Test the cache hit/miss behavior with simulated embeddings to ensure that semantically similar queries return cached answers and others do not. Also test that cached answers actually get returned in place of calling the LLM (this can be done by counting LLM call invocations via a stub).
- **Authentication & Rate Limits:** Test that missing/invalid keys are rejected, valid keys pass, and rate limiting triggers after the specified number of requests.
- **PII Masking & Encryption:** Test that PII is properly masked by our functions and that encryption/decryption works round-trip. Also test that enabling/disabling the mask flags has the intended effect on stored data (maybe via logs or DB entries).
- **Database Writes (Supabase):** If using a test database, test that interactions are saved correctly and can be retrieved/decoded. Ensure that `cache_hit` flags and token counts are stored accurately.
- **Overall integration:** Possibly a test that runs through a full flow: a fake user request goes through compression -> cache miss -> model stub -> response -> stored in DB, and then a second similar request hits cache. This would combine multiple pieces.

We have shown example test stubs in each section. These would be run with `pytest` or similar. In CI, after running tests, we could also run a linter (flake8) and a type checker (mypy) to maintain code quality.

By covering these aspects, the test suite ensures that changes to one part (e.g., caching or auth) won’t break others without detection. It also documents the expected behavior clearly.

## Performance and Cost Considerations  
Finally, let’s highlight how this design achieves **low latency and cost efficiency**:
- **Prompt Token Optimization:** Using SynthLang to compress prompts means we send fewer tokens to the LLM, which reduces latency (less to transmit and parse) and cost (OpenAI charges by tokens). A reduction of even 50% of tokens can halve the cost per request. SynthLang’s creator reported cutting token costs by 70% and seeing 233% faster responses in their trials ([ Introducing 効 SynthLang a hyper-efficient prompt language inspired by Japanese Kanji cutting token costs by 90%, speeding up AI responses by 900% : r/aipromptprogramming](https://www.reddit.com/r/aipromptprogramming/comments/1hv6iiw/introducing_%E5%8A%B9_synthlang_a_hyperefficient_prompt/#:~:text=To%20evaluate%20SynthLang%2C%20I%20implemented,workflows%20without%20choking%20on%20complexity)).
- **Semantic Caching:** By avoiding repeated LLM calls for similar queries, we save on API costs (fewer calls to pay for) and significantly reduce response time for those queries (a cache hit is served in milliseconds from memory vs possibly seconds from the LLM) ([GPT Semantic Cache: Reducing LLM Costs and Latency via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2#:~:text=)). High cache hit rates can drive down average latency and cost per request.
- **Streaming Responses:** Streaming allows the user to start seeing the answer as it’s generated, improving perceived performance (the first token can arrive within a second or two, even if full completion takes longer). This keeps clients responsive.
- **FastAPI & Async IO:** The server uses asynchronous I/O so it can handle many concurrent connections (particularly important for streaming, where one request might remain open for many seconds). By releasing the worker to handle other requests while awaiting LLM response, we maximize throughput.
- **LiteLLM / Multi-provider support:** This can allow cost-optimization strategies like routing to different models. For example, one could configure that if the prompt is short or a lesser quality answer is acceptable, route to a cheaper model (like an open-source model) vs routing to GPT-4 for more complex queries. This proxy could in the future incorporate logic to choose models dynamically (not implemented initially, but the routing capability is there).
- **Token counting and limits:** We keep an eye on prompt sizes and could refuse or trim extremely long prompts to prevent very expensive calls. We might enforce a max token length after compression.
- **Scaling:** On Fly.io, we can run multiple instances in different regions to serve users with lower network latency, and use the Fly global proxy to route to nearest instance. The caching could be global if using Redis (we might consider using a Redis cache that all instances share, to increase hit rates across instances).

All these measures contribute to a proxy that is fast, cost-effective, and user-isolated. 

With this design and implementation plan, we have a clear path to build a high-speed LLM proxy that extends OpenAI’s API with caching, prompt optimization, security, and multi-tenancy. The following code and configurations provide a solid starting point for implementation, and the included tests will help validate correctness and performance as the development progresses. The system can be iteratively improved (for example, more advanced caching eviction, dynamic model selection, etc.), but the foundation addresses the core requirements and ensures a robust, efficient service.



# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.models import ChatRequest
from app import auth, synthlang, cache, llm_provider, db
from app.agents import registry  # tool registry

app = FastAPI()

@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatRequest,
    api_key: str = Depends(auth.verify_api_key)
):
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
    if cached_response:
        if request.stream:
            def yield_cached():
                yield f"data: {cached_response}\n\n"
                yield "data: [CACHE_END]\n\n"
            return StreamingResponse(yield_cached(), media_type="text/event-stream")
        else:
            return JSONResponse(content={
                "id": "cached-resp",
                "object": "chat.completion",
                "choices": [{"index": 0, "message": {"role": "assistant", "content": cached_response}, "finish_reason": "stop"}]
            })

    # 3. Prepare final messages: decompress if using Mode 2.
    final_messages = []
    for msg in compressed_messages:
        if msg["role"] in ("user", "system"):
            final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
        else:
            final_messages.append(msg)

    # 4. Route to LLM provider: dynamically choose GPT-4o or o3-mini.
    try:
        if request.stream:
            response_iter = await llm_provider.stream_chat(model=request.model, messages=final_messages,
                                                             temperature=request.temperature or 1.0,
                                                             top_p=request.top_p or 1.0,
                                                             n=request.n or 1, user_id=user_id)
            def stream_generator():
                for chunk in response_iter:
                    if 'delta' in chunk.get('choices', [{}])[0]:
                        content_piece = chunk['choices'][0]['delta'].get('content', '')
                        yield f"data: {content_piece}\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            result = await llm_provider.complete_chat(model=request.model, messages=final_messages,
                                                      temperature=request.temperature,
                                                      top_p=request.top_p,
                                                      n=request.n, user_id=user_id)
            assistant_msg = result["choices"][0]["message"]["content"]
            response_payload = {
                "id": result.get("id", ""),
                "object": "chat.completion",
                "created": result.get("created", 0),
                "model": request.model,
                "usage": result.get("usage", {}),
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": assistant_msg},
                    "finish_reason": result["choices"][0].get("finish_reason", "stop")
                }]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM provider call failed: {e}")

    # 5. Cache and persist the result.
    cache.store(cache_key, assistant_msg)
    # Persist asynchronously (fire and forget).
    import asyncio
    asyncio.create_task(db.save_interaction(user_id, request.model, compressed_messages, assistant_msg, cache_hit=False))
    return JSONResponse(content=response_payload)
