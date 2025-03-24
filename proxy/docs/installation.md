# SynthLang Proxy Installation Guide

This guide provides detailed instructions for installing SynthLang Proxy in various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Installation from PyPI](#installation-from-pypi)
  - [Installation from Source](#installation-from-source)
  - [Installation using Docker](#installation-using-docker)
  - [Installation using Poetry](#installation-using-poetry)
- [Configuration](#configuration)
- [Verifying Installation](#verifying-installation)
- [Platform-Specific Instructions](#platform-specific-instructions)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
- [Database Setup](#database-setup)
  - [PostgreSQL Setup](#postgresql-setup)
  - [SQLite Setup](#sqlite-setup)
- [Next Steps](#next-steps)
- [Troubleshooting Installation Issues](#troubleshooting-installation-issues)

## Prerequisites

Before installing SynthLang Proxy, ensure you have the following:

- **Python**: Version 3.10 or higher
- **Database** (one of the following):
  - PostgreSQL 14.0 or higher (recommended for production)
  - SQLite 3.35.0 or higher (suitable for development/testing)
- **API Keys**:
  - OpenAI API key for LLM access

### System Requirements

- **CPU**: 2+ cores recommended
- **RAM**: Minimum 2GB, 4GB+ recommended
- **Disk Space**: 200MB for SynthLang Proxy + additional space for database and logs
- **Network**: Outbound HTTPS access to API providers

## Installation Methods

### Installation from PyPI

The simplest way to install SynthLang Proxy is via pip:

```bash
pip install synthlang-proxy
```

This installs the SynthLang Proxy package and its dependencies. For production use, you may want to create a virtual environment first:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install synthlang-proxy
```

### Installation from Source

To install the latest development version from source:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy
```

2. Install the package:

```bash
pip install -e .
```

Or install with dependencies:

```bash
pip install -r requirements.txt
```

### Installation using Docker

To install using Docker:

1. Pull the Docker image:

```bash
docker pull ghcr.io/yourusername/synthlang-proxy:latest
```

2. Or build from Dockerfile:

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy
docker build -t synthlang-proxy .
```

### Installation using Poetry

For dependency management with Poetry:

1. Install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install SynthLang Proxy:

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy
poetry install
```

## Configuration

After installation, you need to configure SynthLang Proxy:

1. Create a configuration file by copying the sample:

```bash
cp .env.sample .env
```

2. Edit the `.env` file to include your settings:

```
# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=false

# Security
# Generate a secure random key for encryption (32 bytes, base64 encoded)
# You can generate one with: python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
ENCRYPTION_KEY=your_generated_encryption_key

# Database Configuration
# PostgreSQL connection URL (for production)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/synthlang_proxy

# For development/testing, you can use SQLite instead
USE_SQLITE=0
SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db

# Debug SQL queries (set to 1 to enable)
DEBUG_SQL=0

# Rate Limiting
# Default rate limits (requests per minute)
DEFAULT_RATE_LIMIT_QPM=60
PREMIUM_RATE_LIMIT=120

# SynthLang Integration
# Enable/disable SynthLang compression (set to 0 to disable)
USE_SYNTHLANG=1

# PII Masking Configuration
# Mask PII before sending to LLM (set to 1 to enable)
MASK_PII_BEFORE_LLM=0
# Mask PII in logs and database (set to 0 to disable)
MASK_PII_IN_LOGS=1

# LLM Provider Configuration
# OpenAI API key (required)
OPENAI_API_KEY=your_openai_api_key
# Default model to use
DEFAULT_MODEL=gpt-4o
# Timeout for LLM API calls (in seconds)
LLM_TIMEOUT=30

# Semantic Cache
# Enable/disable semantic cache (set to 0 to disable)
ENABLE_CACHE=1
# Similarity threshold for cache hits (0.0-1.0)
CACHE_SIMILARITY_THRESHOLD=0.95
# Maximum number of items to keep in cache
CACHE_MAX_ITEMS=1000

# Logging
LOG_LEVEL=INFO
LOG_FILE=proxy.log
```

### Essential Configuration Options

At a minimum, you must configure:

- `ENCRYPTION_KEY`: A secure random key for encrypting sensitive data
- `OPENAI_API_KEY`: Your OpenAI API key
- Database settings: Either `DATABASE_URL` for PostgreSQL or `USE_SQLITE=1` for SQLite

## Verifying Installation

To verify that SynthLang Proxy is installed correctly:

1. Run the health check:

```bash
python -m app.main check
```

Or for CLI installations:

```bash
synthlang proxy health
```

2. Start the service:

```bash
python -m app.main
```

3. Test with a simple request:

```bash
curl -X GET http://localhost:8000/health
```

You should receive a JSON response indicating the service is running correctly.

## Platform-Specific Instructions

### Linux

For Debian/Ubuntu systems, you might need additional system packages:

```bash
sudo apt update
sudo apt install -y python3-dev build-essential libpq-dev
```

For production deployments, consider setting up a systemd service:

```bash
sudo nano /etc/systemd/system/synthlang.service
```

Add the following:

```
[Unit]
Description=SynthLang Proxy
After=network.target

[Service]
User=synthlang
WorkingDirectory=/path/to/synthlang-proxy
Environment="PATH=/path/to/synthlang-proxy/venv/bin"
EnvironmentFile=/path/to/synthlang-proxy/.env
ExecStart=/path/to/synthlang-proxy/venv/bin/python -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable synthlang
sudo systemctl start synthlang
```

### macOS

On macOS, you might need to install additional tools:

```bash
brew install postgresql python@3.10
```

For local development, consider using Docker for PostgreSQL:

```bash
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:14
```

### Windows

On Windows, consider using WSL (Windows Subsystem for Linux) for better compatibility:

1. Install WSL following [Microsoft's instructions](https://docs.microsoft.com/en-us/windows/wsl/install)
2. Install Python and other dependencies in your WSL environment
3. Follow the Linux installation instructions above

If you prefer native Windows:

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
3. Use PowerShell for running commands

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install SynthLang Proxy
pip install synthlang-proxy

# Create config file
Copy-Item .env.sample .env
```

## Database Setup

### PostgreSQL Setup

1. Install PostgreSQL:

   **Debian/Ubuntu**:
   ```bash
   sudo apt update
   sudo apt install -y postgresql postgresql-contrib
   ```

   **RHEL/CentOS**:
   ```bash
   sudo dnf install -y postgresql-server postgresql-contrib
   sudo postgresql-setup --initdb
   sudo systemctl enable postgresql
   sudo systemctl start postgresql
   ```

   **macOS**:
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. Create a database and user:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE synthlang_proxy;
CREATE USER synthlang WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE synthlang_proxy TO synthlang;
\q
```

3. Update your `.env` file with the connection string:

```
DATABASE_URL=postgresql+asyncpg://synthlang:your_password@localhost:5432/synthlang_proxy
```

### SQLite Setup

For development or small deployments, SQLite is simpler:

1. Enable SQLite in your `.env` file:

```
USE_SQLITE=1
SQLITE_PATH=sqlite+aiosqlite:///./synthlang_proxy.db
```

2. The database file will be created automatically when SynthLang Proxy starts.

## Next Steps

After installation:

1. **Run database migrations**:

```bash
alembic upgrade head
```

2. **Configure keyword patterns**:
   
   Edit `config/keywords.toml` to define keyword patterns for automatic tool invocation.

3. **Set up agent tools**:
   
   Configure any additional agent tools you want to use.

4. **Start the service**:

```bash
python -m app.main
```

5. **Test with the CLI**:

```bash
synthlang proxy chat "Hello, how are you?"
```

## Troubleshooting Installation Issues

### Common Issues

#### Database Connection Errors

If you get database connection errors:

1. Verify your PostgreSQL service is running:
   ```bash
   sudo systemctl status postgresql
   ```

2. Check your connection string in `.env`

3. Ensure the user has proper permissions:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE synthlang_proxy TO synthlang;
   ```

#### Package Dependency Errors

If you encounter package dependency issues:

1. Update pip:
   ```bash
   pip install --upgrade pip
   ```

2. Try installing with extra dependencies:
   ```bash
   pip install synthlang-proxy[all]
   ```

#### Port Already in Use

If port 8000 is already in use:

1. Change the port in your `.env` file:
   ```
   PORT=8001
   ```

2. Or find and stop the process using the port:
   ```bash
   sudo lsof -i :8000
   sudo kill <PID>
   ```

#### OpenAI API Key Issues

If you encounter OpenAI API errors:

1. Verify your API key is correct in `.env`

2. Check that your API key has the necessary permissions

3. Ensure you have billing set up in your OpenAI account

### Getting Help

If you continue to have installation issues:

1. Check the [GitHub Issues](https://github.com/yourusername/synthlang-proxy/issues) for similar problems and solutions

2. Join the community on [Discord or Slack]

3. File a new issue with detailed information about your environment and the error messages you're seeing