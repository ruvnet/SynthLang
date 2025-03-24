# Docker Deployment for SynthLang Proxy

This document provides detailed instructions for deploying SynthLang Proxy using Docker.

## Dockerfile

SynthLang Proxy uses the following Dockerfile for containerization:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY .env.sample ./.env.sample
COPY init_db_roles.py .
COPY fix_admin_user.py .
COPY add_admin_role.py .
COPY check_roles.py .

# Create necessary directories
RUN mkdir -p /app/data

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables (these are defaults and should be overridden at runtime)
ENV PORT=8000 \
    HOST=0.0.0.0 \
    DEBUG=false \
    USE_SQLITE=1 \
    SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db \
    ENABLE_CACHE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose

For development and production deployments, Docker Compose provides a better solution:

```yaml
services:
  proxy:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
      - DEBUG=false
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/synthlang_proxy
      - USE_SQLITE=${USE_SQLITE:-1}
      - SQLITE_PATH=${SQLITE_PATH:-sqlite+aiosqlite:///./synthlang_proxy.db}
      - PREMIUM_RATE_LIMIT=${PREMIUM_RATE_LIMIT:-120}
      - USE_SYNTHLANG=${USE_SYNTHLANG:-1}
      - MASK_PII_BEFORE_LLM=${MASK_PII_BEFORE_LLM:-0}
      - MASK_PII_IN_LOGS=${MASK_PII_IN_LOGS:-1}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEFAULT_MODEL=${DEFAULT_MODEL:-gpt-4o-mini}
      - LLM_TIMEOUT=${LLM_TIMEOUT:-30}
      - ENABLE_CACHE=${ENABLE_CACHE:-1}
      - CACHE_SIMILARITY_THRESHOLD=${CACHE_SIMILARITY_THRESHOLD:-0.95}
      - CACHE_MAX_ITEMS=${CACHE_MAX_ITEMS:-1000}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - LOG_FILE=${LOG_FILE:-proxy.log}
      - API_KEY=${API_KEY}
      - ADMIN_API_KEY=${ADMIN_API_KEY}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    volumes:
      - ./:/app

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=synthlang_proxy
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Environment Variables

The Docker setup uses environment variables for configuration. These can be provided in a `.env` file in the project root directory:

```
PORT=8000
HOST=0.0.0.0
DEBUG=false
ENCRYPTION_KEY=your_encryption_key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/synthlang_proxy
USE_SQLITE=1
SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db
PREMIUM_RATE_LIMIT=120
USE_SYNTHLANG=1
MASK_PII_BEFORE_LLM=0
MASK_PII_IN_LOGS=1
OPENAI_API_KEY=your_openai_api_key
DEFAULT_MODEL=gpt-4o-mini
LLM_TIMEOUT=30
ENABLE_CACHE=1
CACHE_SIMILARITY_THRESHOLD=0.95
CACHE_MAX_ITEMS=1000
LOG_LEVEL=INFO
LOG_FILE=proxy.log
API_KEY=your_api_key
ADMIN_API_KEY=your_admin_api_key
```

## Building and Running

To build and run the Docker containers:

```bash
# Build the images
docker-compose build

# Start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

## Database Initialization

The database is automatically initialized when the container starts. However, you may need to run additional scripts to set up roles and users:

```bash
# Initialize database roles
docker-compose exec proxy python init_db_roles.py

# Fix admin user if needed
docker-compose exec proxy python fix_admin_user.py

# Add admin role to a user
docker-compose exec proxy python add_admin_role.py user_id

# Check roles
docker-compose exec proxy python check_roles.py
```

## Health Checks

The Docker setup includes health checks for both the proxy and database services. You can manually check the health of the proxy service:

```bash
curl http://localhost:8000/health
```

## Testing the Deployment

You can test the deployment with a simple API call:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Hello, world!"}
    ]
  }'
```

## Production Considerations

For production deployments:

1. Use a non-root user in the container
2. Set up proper logging and monitoring
3. Configure a reverse proxy (like Nginx) for SSL termination
4. Use Docker secrets or a secure vault for sensitive environment variables
5. Set up database backups
6. Configure proper resource limits for containers
7. Use Docker Compose profiles or Kubernetes for more complex deployments

## Troubleshooting

Common issues and solutions:

1. **Database connection errors**: Check that the database container is running and healthy
2. **API key errors**: Verify that the API keys are correctly set in the environment variables
3. **Permission issues**: Check that the container has the necessary permissions to access mounted volumes
4. **Memory issues**: Increase the memory limit for the container if you see out-of-memory errors