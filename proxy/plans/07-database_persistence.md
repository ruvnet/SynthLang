# Phase 7: Database Persistence (07-database_persistence.md)

## Objective
Implement database persistence using SQLAlchemy and Supabase (Postgres) to store interactions (prompts, responses, metadata).

## Steps

1.  **Create `app/database.py` file:**
    -   Create `app/database.py` to define SQLAlchemy models and database setup.

2.  **Define SQLAlchemy Model in `app/database.py`:**
    -   Define `Interaction` SQLAlchemy model with columns:
        -   `id` (Integer, primary key, index)
        -   `user_id` (String, index)
        -   `model` (String)
        -   `prompt_enc` (LargeBinary, for encrypted prompt)
        -   `response_enc` (LargeBinary, for encrypted response)
        -   `cache_hit` (Boolean)
        -   `prompt_tokens` (Integer)
        -   `response_tokens` (Integer)
        -   `timestamp` (DateTime(timezone=True), server_default=func.now())
    -   Define database connection URL (for now, placeholder, will be configured via env var later).
    -   Create `AsyncEngine` and `AsyncSessionLocal` using SQLAlchemy.
    -   Create `Base = declarative_base()`.

    ```python
    # app/database.py
    import os
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker, declarative_base
    from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, DateTime, func

    DATABASE_URL = "postgresql+asyncpg://user:password@host:port/database_name" # Placeholder, configure via env var later
    engine = create_async_engine(DATABASE_URL, echo=False) # Set echo=True for debugging SQL
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    Base = declarative_base()

    class Interaction(Base):
        __tablename__ = "interactions"
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(String, index=True)
        model = Column(String)
        prompt_enc = Column(LargeBinary)
        response_enc = Column(LargeBinary)
        cache_hit = Column(Boolean)
        prompt_tokens = Column(Integer)
        response_tokens = Column(Integer)
        timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ```

3.  **Create `app/db.py` file:**
    -   Create `app/db.py` to house database interaction functions.

4.  **Implement `save_interaction` function in `app/db.py`:**
    -   Import `SessionLocal` and `Interaction` from `app/database.py`.
    -   Import `security` (for encryption, will be implemented in next phase, for now, placeholder encryption).
    -   Implement `save_interaction(user_id: str, model: str, messages: list, response_text: str, cache_hit: bool)` function:
        -   This function should take interaction details and save them to the database.
        -   Combine messages into a single prompt text.
        -   For now, placeholder encryption: just encode prompt and response to bytes. Encryption will be properly implemented in the security phase.
        -   Placeholder token counting: use simple `len(text.split())` for token counts.
        -   Create an `Interaction` object with the provided data.
        -   Use `AsyncSessionLocal` to create an async session.
        -   Add the `Interaction` object to the session and commit to save to the database.

    ```python
    # app/db.py
    from app.database import SessionLocal, Interaction
    # from app import security # Import security later, placeholder encryption for now

    async def save_interaction(user_id: str, model: str, messages: list, response_text: str, cache_hit: bool):
        """Save the interaction (prompt and response) to the database."""
        prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages]) # Combine messages to prompt text
        # Placeholder encryption (replace with security.encrypt_text later)
        prompt_enc = prompt_text.encode('utf-8') # Placeholder: encode to bytes
        response_enc = response_text.encode('utf-8') # Placeholder: encode to bytes
        prompt_tokens = len(prompt_text.split()) # Placeholder token count
        response_tokens = len(response_text.split()) # Placeholder token count

        async with SessionLocal() as session: # Async session
            interaction = Interaction( # Create Interaction object
                user_id=user_id,
                model=model,
                prompt_enc=prompt_enc,
                response_enc=response_enc,
                cache_hit=cache_hit,
                prompt_tokens=prompt_tokens,
                response_tokens=response_tokens
            )
            session.add(interaction) # Add to session
            await session.commit() # Commit transaction
    ```

5.  **Integrate Database Persistence in `app/main.py`:**
    -   Import `db` from `app.db`.
    -   In `create_chat_completion` function:
        -   After getting the LLM response (or cached response), call `db.save_interaction(user_id, request.model, compressed_messages, assistant_msg, cache_hit=bool(cached_response))` to persist the interaction data.
        -   For now, call `save_interaction` synchronously (without `asyncio.create_task`). Asynchronous persistence will be implemented in a sub-step or next phase if needed.

    ```python
    # app/main.py
    from fastapi import FastAPI, Depends, HTTPException, Request # Import Request
    from fastapi.responses import StreamingResponse, JSONResponse
    from app.models import ChatRequest
    from app import auth, synthlang, cache, llm_provider, db # Import db

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
            response_content = cached_response # Use cached response
            cache_hit_flag = True
        else: # Cache miss, call LLM
            final_messages = []
            for msg in compressed_messages: # Decompress for LLM call
                if msg["role"] in ("user", "system"):
                    final_messages.append({"role": msg["role"], "content": synthlang.decompress_prompt(msg["content"])})
                else:
                    final_messages.append(msg)
            try:
                result = await llm_provider.complete_chat(model=request.model, messages=final_messages, temperature=request.temperature, top_p=request.top_p, n=request.n, user_id=user_id) # Call LLM
                response_content = result["choices"][0]["message"]["content"] # Extract assistant message
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"LLM provider call failed: {e}") # Handle LLM errors
            cache_hit_flag = False

        # 4. Store in cache (after successful LLM call if cache miss)
        if not cache_hit_flag:
            cache.store(cache_key, response_content) # Store LLM response in cache

        # 5. Persist interaction to database
        await db.save_interaction(user_id, request.model, compressed_messages, response_content, cache_hit=cache_hit_flag) # Save interaction

        return {
            "message": "LLM response",
            "request_model_valid": True,
            "api_key_verified": True,
            "user_id": user_id,
            "rate_limit_allowed": True,
            "compressed_messages": compressed_messages,
            "cache_hit": cache_hit_flag,
            "llm_response_content": response_content # Include LLM response content
        }
    ```

6.  **Create test file `tests/test_db.py`:**
    -   Create `tests/test_db.py` for database persistence tests.

7.  **Write tests for Database Persistence in `tests/test_db.py`:**
    -   Test `save_interaction` function:
        -   **Save Interaction Successfully:**
            -   Call `save_interaction` with sample data.
            -   Query the database to retrieve the last inserted interaction.
            -   Assert that the retrieved interaction data matches the saved data (user_id, model, cache_hit, prompt/response content - for now, check encoded content).
        -   Use an in-memory SQLite database for testing to avoid external database dependency. Configure SQLAlchemy to use SQLite in tests.

    ```python
    # tests/test_db.py
    import asyncio
    from app import db, database
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    # Use an in-memory SQLite database for tests
    DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"
    engine_test = create_async_engine(DATABASE_URL_TEST)
    TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db(): # Dependency override for tests
        async with TestingSessionLocal() as session:
            yield session

    database.SessionLocal = TestingSessionLocal # Override SessionLocal for tests
    database.engine = engine_test # Override engine for tests

    @pytest.fixture(scope="function", autouse=True) # Create and drop tables for each test function
    async def create_test_db():
        async with database.engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.create_all)
        yield
        async with database.engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.drop_all)

    @pytest.mark.asyncio
    async def test_save_interaction_success():
        user_id = "test_user"
        model = "test-model"
        messages = [{"role": "user", "content": "Test prompt"}]
        response_text = "Test response"
        cache_hit = False
        await db.save_interaction(user_id, model, messages, response_text, cache_hit) # Save interaction

        async def get_last_interaction(): # Helper to get last interaction from DB
            async with TestingSessionLocal() as session:
                result = await session.execute("SELECT user_id, model, prompt_enc, response_enc, cache_hit FROM interactions ORDER BY id DESC LIMIT 1") # Get last inserted
                row = result.fetchone()
                return row

        row = await get_last_interaction()
        assert row is not None # Check if row is returned
        db_user_id, db_model, db_prompt_enc, db_response_enc, db_cache_hit = row # Unpack row
        assert db_user_id == user_id
        assert db_model == model
        assert db_cache_hit == cache_hit
        assert db_prompt_enc == "\nuser: Test prompt".encode('utf-8') # Check encoded prompt content
        assert db_response_enc == response_text.encode('utf-8') # Check encoded response content
```

8.  **Update `tests/test_api.py` to test Database Persistence integration in API endpoint:**
    -   In `test_chat_completion_endpoint_exists` and `test_valid_api_key`:
        -   After sending a request to the API endpoint, assert that `db.save_interaction` function is called (using mock or spy).
        -   (Optional) Query the test database to verify that the interaction is actually saved with correct data.

9.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_db.py tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/database.py` file.
-   [x] Step 2: Define SQLAlchemy Model in `app/database.py`.
-   [x] Step 3: Create `app/db.py` file.
-   [x] Step 4: Implement `save_interaction` function in `app/db.py`.
-   [x] Step 5: Integrate Database Persistence in `app/main.py`.
-   [x] Step 6: Create test file `tests/test_db.py`.
-   [x] Step 7: Write tests for Database Persistence in `tests/test_db.py`.
-   [x] Step 8: Update `tests/test_api.py` to test DB Persistence in API endpoint.
    - [ ] Step 8.1: Test `db.save_interaction` is called after API call.
    - [ ] Step 8.2: (Optional) Verify data saved in test DB.
-   [ ] Step 9: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Security - Encryption and PII Masking (08-security_encryption_pii.md)

---