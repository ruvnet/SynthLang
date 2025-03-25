FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    DEBUG=false \
    USE_SQLITE=1 \
    SQLITE_PATH=sqlite+aiosqlite:///./data/synthlang_proxy.db \
    DATABASE_URL=sqlite+aiosqlite:///./data/synthlang_proxy.db

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    openssl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite database
RUN mkdir -p /app/data && \
    touch /app/data/.keep

# Generate encryption key if not provided
RUN if [ -z "$ENCRYPTION_KEY" ]; then \
    export ENCRYPTION_KEY=$(openssl rand -hex 16); \
    echo "ENCRYPTION_KEY=$ENCRYPTION_KEY" >> .env; \
    fi

# Copy the application code
COPY . .

# Create a start script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Check if the database directory exists and is writable' >> /app/start.sh && \
    echo 'if [ ! -d "/app/data" ]; then' >> /app/start.sh && \
    echo '    echo "Error: /app/data directory does not exist"' >> /app/start.sh && \
    echo '    exit 1' >> /app/start.sh && \
    echo 'fi' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo 'if [ ! -w "/app/data" ]; then' >> /app/start.sh && \
    echo '    echo "Error: /app/data directory is not writable"' >> /app/start.sh && \
    echo '    exit 1' >> /app/start.sh && \
    echo 'fi' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Initialize the database if it does not exist' >> /app/start.sh && \
    echo 'if [ ! -f "/app/data/synthlang_proxy.db" ]; then' >> /app/start.sh && \
    echo '    echo "Initializing database..."' >> /app/start.sh && \
    echo '    python init_db_roles.py' >> /app/start.sh && \
    echo 'else' >> /app/start.sh && \
    echo '    echo "Database already exists, skipping initialization"' >> /app/start.sh && \
    echo 'fi' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start the application' >> /app/start.sh && \
    echo 'exec uvicorn src.app.main:app --host 0.0.0.0 --port 8000' >> /app/start.sh && \
    chmod +x /app/start.sh

# Create a non-root user to run the application
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Use the start script as the entrypoint
CMD ["/app/start.sh"]