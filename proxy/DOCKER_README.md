# Docker Setup for SynthLang Proxy

This document provides instructions for running the SynthLang Proxy using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- OpenAI API key (or other compatible LLM provider)

## Quick Start

1. Clone the repository and navigate to the proxy directory:
   ```bash
   git clone https://github.com/yourusername/synthlang-proxy.git
   cd synthlang-proxy/proxy
   ```

2. Create a `.env` file with your configuration:
   ```bash
   cp .env.sample .env
   # Edit .env with your OpenAI API key and other settings
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. The proxy will be available at http://localhost:8000

## Configuration Options

You can configure the proxy by setting environment variables in your `.env` file or directly in the `docker-compose.yml` file.

### Essential Configuration

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `API_KEY`: API key for accessing the proxy (will be generated if not provided)
- `ADMIN_API_KEY`: API key for admin access (will be generated if not provided)

### Database Configuration

By default, the proxy uses SQLite, but you can configure it to use PostgreSQL:

- `USE_SQLITE`: Set to 1 to use SQLite, 0 to use PostgreSQL
- `DATABASE_URL`: PostgreSQL connection URL (used when USE_SQLITE=0)

### Advanced Configuration

- `DEFAULT_MODEL`: Default LLM model to use (default: gpt-4o-mini)
- `ENABLE_CACHE`: Enable semantic caching (1=enabled, 0=disabled)
- `USE_SYNTHLANG`: Enable SynthLang compression (1=enabled, 0=disabled)
- `ENCRYPTION_KEY`: Key for encrypting sensitive data (will be generated if not provided)

## Using PostgreSQL

The Docker Compose setup includes a PostgreSQL database. To use it:

1. Set `USE_SQLITE=0` in your `.env` file
2. Set `DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/synthlang_proxy`

## Volumes

The Docker Compose setup creates the following volumes:

- `postgres_data`: Persistent storage for the PostgreSQL database
- `./synthlang_proxy.db:/app/synthlang_proxy.db`: Maps the SQLite database file to your local filesystem
- `./.api_keys.json:/app/.api_keys.json`: Maps the API keys file to your local filesystem

## Health Checks

The Docker Compose setup includes health checks for both the proxy and the database. You can monitor the health of the services using:

```bash
docker-compose ps
```

## Logs

To view the logs:

```bash
docker-compose logs -f proxy
```

## Stopping the Services

To stop the services:

```bash
docker-compose down
```

To stop the services and remove the volumes:

```bash
docker-compose down -v
```

## Rebuilding the Image

If you make changes to the code, you'll need to rebuild the image:

```bash
docker-compose build
```

## Troubleshooting

### Database Initialization Issues

If you encounter issues with database initialization, you can run the initialization script manually:

```bash
docker-compose exec proxy python init_db_roles.py
```

### API Key Issues

If you need to create a new API key:

```bash
docker-compose exec proxy python -m src.cli.api_keys create --user-id "your_username" --rate-limit 100
```

### Connection Issues

If you can't connect to the proxy, check that the container is running:

```bash
docker-compose ps
```

And check the logs for any errors:

```bash
docker-compose logs proxy