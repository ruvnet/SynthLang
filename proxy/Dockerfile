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
    SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db

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

# Copy the application code
COPY . .

# Generate encryption key if not provided
RUN if [ -z "$ENCRYPTION_KEY" ]; then \
    export ENCRYPTION_KEY=$(openssl rand -hex 16); \
    echo "ENCRYPTION_KEY=$ENCRYPTION_KEY" >> .env; \
    fi

# Create a non-root user to run the application
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Initialize the database and set up roles
RUN python init_db_roles.py

# Expose the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]