# Phase 12: Dockerfile and Fly.io Deployment (12-docker_flyio_deployment.md)

## Objective
Create a Dockerfile for containerizing the application and configure Fly.io deployment.

## Steps

1.  **Create `Dockerfile` in the project root:**
    -   Create a `Dockerfile` in the root directory of the `synthlang_router/` project.
    -   Use a Python 3.11 slim base image (`FROM python:3.11-slim`).
    -   Install system dependencies if needed (e.g., `build-essential`, `libaio-dev` for FAISS).
    -   Set working directory to `/app` (`WORKDIR /app`).
    -   Copy `requirements.txt` and install Python dependencies using `pip install -r requirements.txt`.
    -   Copy the `app/` directory, `fly.toml`, and `README.md` into the container.
    -   Expose port 8080 (`EXPOSE 8080`).
    -   Set environment variable `PORT=8080` (`ENV PORT=8080`).
    -   Define the command to run the application using Uvicorn: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]`.

    ```dockerfile
    # Dockerfile
    FROM python:3.11-slim

    RUN apt-get update && apt-get install -y build-essential libaio-dev # Install system deps if needed

    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY app/ ./app/
    COPY fly.toml .
    COPY README.md .

    EXPOSE 8080
    ENV PORT=8080

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
    ```

2.  **Create `fly.toml` file in the project root:**
    -   Create a `fly.toml` file in the root directory of the `synthlang_router/` project for Fly.io app configuration.
    -   Configure basic app settings:
        -   `app = "synthlang-router"` (or your desired app name)
        -   `[env]` section to set environment variables:
            -   `PORT = "8080"`
            -   `OPENAI_API_KEY = "sk-..."` (placeholder, set via `fly secrets`)
            -   `ENCRYPTION_KEY = "your_base64_fernet_key_here"` (placeholder, set via `fly secrets`)
            -   `DATABASE_URL = "postgresql+asyncpg://user:pass@dbhost/dbname"` (placeholder, set via `fly secrets`)
            -   `USE_SYNTHLANG = "1"` (or "0" to disable SynthLang)
            -   `MASK_PII_BEFORE_LLM = "0"` (or "1" to enable PII masking before LLM)
            -   `MASK_PII_IN_LOGS = "1"` (or "0" to disable PII masking in logs)
        -   `[[services]]` section to define service settings:
            -   `internal_port = 8080`
            -   `protocol = "tcp"`
            -   `[[services.ports]]` for HTTP (port 80) and HTTPS (port 443) handlers.
            -   `[services.concurrency]` to configure concurrency settings (e.g., `type = "connections"`, `hard_limit = 25`, `soft_limit = 20`).

    ```toml
    # fly.toml
    app = "synthlang-router" # Replace with your app name

    [env]
      PORT = "8080"
      OPENAI_API_KEY = "sk-..."             # Set via fly secrets
      ENCRYPTION_KEY = "your_base64_fernet_key_here" # Set via fly secrets
      DATABASE_URL = "postgresql+asyncpg://user:pass@dbhost/dbname" # Set via fly secrets
      USE_SYNTHLANG = "1"
      MASK_PII_BEFORE_LLM = "0"
      MASK_PII_IN_LOGS = "1"

    [[services]]
      internal_port = 8080
      protocol = "tcp"
      
      [[services.ports]]
        handlers = ["http"]
        port = 80

      [[services.ports]]
        handlers = ["tls", "http"]
        port = 443

      [services.concurrency]
        type = "connections"
        hard_limit = 25
        soft_limit = 20
    ```

3.  **Update `requirements.txt`:**
    -   Ensure all necessary dependencies are listed in `requirements.txt`, including:
        -   `fastapi`
        -   `uvicorn`
        -   `openai`
        -   `pydantic`
        -   `SQLAlchemy`
        -   `asyncpg` (or other async Postgres driver)
        -   `faiss-cpu` (or `faiss-gpu` if using GPU)
        -   `cryptography`
        -   `python-multipart` (for FastAPI file uploads if needed, though not in current design)

    ```text
    fastapi
    uvicorn
    openai
    pydantic
    SQLAlchemy
    asyncpg
    faiss-cpu
    cryptography
    ```

4.  **Test Docker build locally:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `docker build -t synthlang-router .` to build the Docker image.
    -   Check if the image builds successfully without errors.
    -   (Optional) Run the Docker image locally to test the application:
        -   `docker run -p 8080:8080 -e OPENAI_API_KEY=YOUR_OPENAI_API_KEY -e ENCRYPTION_KEY=YOUR_ENCRYPTION_KEY -e DATABASE_URL=YOUR_DATABASE_URL synthlang-router`
        -   Test API endpoints using `curl` or a browser to verify it's working in Docker.

5.  **Deploy to Fly.io:**
    -   Install Flyctl CLI if not already installed.
    -   Login to Flyctl: `flyctl auth login`.
    -   Launch a new Fly.io app (if not already created): `flyctl launch`. Follow the prompts, choose the Dockerfile deployment option, and select a region.
    -   If an app already exists, deploy using: `flyctl deploy`.
    -   Set Fly.io secrets for API keys, encryption key, and database URL:
        ```bash
        fly secrets set OPENAI_API_KEY="your_openai_api_key" ENCRYPTION_KEY="your_fernet_key_base64" DATABASE_URL="your_database_url"
        ```
    -   Monitor deployment logs using `flyctl logs` to check for any errors during deployment or startup.
    -   Access the deployed application URL provided by Fly.io and test the API endpoints.

6.  **Testing Deployment:**
    -   After deployment, test the API endpoints of the deployed application to ensure it's working correctly in the Fly.io environment.
    -   Test both streaming and non-streaming requests, authentication, rate limiting, and basic functionality.

## Test-Driven Development Checklist

-   [x] Step 1: Create `Dockerfile` in the project root.
-   [x] Step 2: Create `fly.toml` file in the project root.
-   [x] Step 3: Update `requirements.txt` with dependencies.
-   [x] Step 4: Test Docker build locally.
-   [x] Step 5: Deploy to Fly.io.
-   [ ] Step 6: Testing Deployment on Fly.io.

**Next Phase:** Implement Monitoring and Observability (13-monitoring_observability.md)

---