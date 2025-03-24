# Phase 11: Configuration and Environment Variables (11-configuration_env_vars.md)

## Objective
Implement configuration management using environment variables and a `config.py` module to load settings.

## Steps

1.  **Create `app/config.py` file:**
    -   Create `app/config.py` to house configuration loading logic.

2.  **Load Configuration from Environment Variables in `app/config.py`:**
    -   Define variables for:
        -   `OPENAI_API_KEY` (str, required, OpenAI API key)
        -   `DATABASE_URL` (str, required, Database connection URL)
        -   `ENCRYPTION_KEY` (str, required, Encryption key for Fernet)
        -   `USE_SYNTHLANG` (bool, optional, default `True`, Enable/disable SynthLang)
        -   `MASK_PII_BEFORE_LLM` (bool, optional, default `False`, Mask PII before sending to LLM)
        -   `MASK_PII_IN_LOGS` (bool, optional, default `True`, Mask PII in logs/database)
        -   `DEFAULT_RATE_LIMIT_QPM` (int, optional, default `60`, Default rate limit per minute)
    -   Load these variables from environment variables using `os.getenv()`.
    -   Convert string values to appropriate types (bool, int) where needed.
    -   Provide default values for optional variables.
    -   Make these configuration variables accessible as module-level constants in `app/config.py`.

    ```python
    # app/config.py
    import os

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # Required
    DATABASE_URL = os.environ.get("DATABASE_URL") # Required
    ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY") # Required

    USE_SYNTHLANG = bool(int(os.getenv("USE_SYNTHLANG", "1"))) # Optional, default True
    MASK_PII_BEFORE_LLM = bool(int(os.getenv("MASK_PII_BEFORE_LLM", "0"))) # Optional, default False
    MASK_PII_IN_LOGS = bool(int(os.getenv("MASK_PII_IN_LOGS", "1"))) # Optional, default True
    DEFAULT_RATE_LIMIT_QPM = int(os.getenv("DEFAULT_RATE_LIMIT_QPM", "60")) # Optional, default 60

    # Model routing configuration (example, can be expanded)
    MODEL_PROVIDER = {
        "gpt-4o-search-preview": "openai",
        "gpt-4o-mini-search-preview": "openai",
        "o3-mini": "openai" 
    }
    ```

3.  **Use Configuration Variables in `app` modules:**
    -   **`app/llm_provider.py`:**
        -   Instead of hardcoding API keys, load `OPENAI_API_KEY` from `app.config`.
        -   (For future: Implement model routing based on `MODEL_PROVIDER` config).
    -   **`app/database.py`:**
        -   Load `DATABASE_URL` from `app.config` for database engine creation.
    -   **`app/security.py`:**
        -   Load `ENCRYPTION_KEY` from `app.config` for Fernet cipher initialization.
    -   **`app/synthlang.py`:**
        -   Load `USE_SYNTHLANG` from `app.config` to control SynthLang enable/disable toggle.
    -   **`app/auth.py`:**
        -   (For future: Load API keys and rate limits from a more configurable source, potentially database or config file, instead of hardcoded `API_KEYS` dict. For now, keep `API_KEYS` hardcoded, but consider `DEFAULT_RATE_LIMIT_QPM` from config).
    -   **`app/main.py`:**
        -   (No direct config usage in `main.py` initially, but it imports modules that use config).

4.  **Update Test Environment (for local testing):**
    -   Create a `.env.sample` file in the `synthlang_router/` directory (or project root) with sample environment variables:
        ```
        OPENAI_API_KEY=your_openai_api_key_here
        DATABASE_URL=postgresql+asyncpg://user:password@host:port/database_name
        ENCRYPTION_KEY=your_fernet_encryption_key_base64
        USE_SYNTHLANG=1
        MASK_PII_BEFORE_LLM=0
        MASK_PII_IN_LOGS=1
        DEFAULT_RATE_LIMIT_QPM=60
        ```
    -   Instruct users to copy `.env.sample` to `.env` and fill in their actual API keys, database URL, and encryption key for local development and testing. (For production deployment on Fly.io or similar, environment variables/secrets will be set in the deployment environment).

5.  **Update tests (if needed):**
    -   If any tests rely on hardcoded API keys or database URLs, update them to either:
        -   Mock the configuration values for testing.
        -   Set environment variables programmatically within the test setup (if needed for integration tests, but avoid for unit tests).
    -   For now, no specific tests for configuration module itself are needed, as it's mostly about loading env vars. We'll test the modules that *use* the config in their respective test files.

6.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest` (or specific test files) to ensure all tests still pass after configuration integration.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/config.py` file.
-   [x] Step 2: Load Configuration from Environment Variables in `app/config.py`.
-   [x] Step 3: Use Configuration Variables in `app` modules (`llm_provider.py`, `database.py`, `security.py`, `synthlang.py`).
-   [x] Step 4: Update Test Environment with `.env.sample` file.
-   [ ] Step 5: Update tests (if needed) to handle configuration.
-   [ ] Step 6: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement Dockerfile and Fly.io Deployment (12-docker_flyio_deployment.md)

---