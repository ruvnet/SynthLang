# SynthLang Proxy Deployment Guide

This guide provides detailed instructions for deploying SynthLang Proxy in various environments, from development to production.

## Deployment Options

SynthLang Proxy can be deployed in several ways:

1. **Docker Deployment**: Containerized deployment using Docker
2. **Serverless Deployment**: Deployment on serverless platforms (AWS Lambda, Google Cloud Functions, etc.)
3. **Traditional Server Deployment**: Deployment on VPS, dedicated servers, or cloud VMs
4. **Platform-as-a-Service (PaaS) Deployment**: Deployment on platforms like Heroku, Fly.io, or Render

## Prerequisites

Regardless of deployment method, the following prerequisites apply:

- **API Keys**: OpenAI API key and other service API keys
- **Database**: PostgreSQL database (or SQLite for development)
- **Environment Variables**: Configuration through environment variables
- **Security**: Encryption key for sensitive data

## Docker Deployment

### Building the Docker Image

SynthLang Proxy includes a `Dockerfile` for easy containerization:

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src ./src
COPY config ./config
COPY .env.sample ./.env.sample

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "src.app.main"]
```

To build the Docker image:

```bash
docker build -t synthlang-proxy .
```

### Running the Docker Container

To run the Docker container:

```bash
docker run -d \
  --name synthlang-proxy \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e ENCRYPTION_KEY=your_encryption_key \
  -e DATABASE_URL=postgresql+asyncpg://user:password@host:port/database \
  synthlang-proxy
```

### Using Docker Compose

For more complex deployments, Docker Compose provides a better solution:

```yaml
# docker-compose.yml
version: '3.8'

services:
  proxy:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/synthlang
      - USE_SYNTHLANG=1
      - ENABLE_CACHE=1
    depends_on:
      - db
    restart: unless-stopped
    volumes:
      - ./config:/app/config

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=synthlang
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

To run with Docker Compose:

```bash
docker-compose up -d
```

### Docker Health Checks

Include health checks to ensure your container is running properly:

```yaml
# In docker-compose.yml
services:
  proxy:
    # ... other configuration ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

## Serverless Deployment

### AWS Lambda Deployment

#### Prerequisites

- AWS Account
- AWS CLI installed and configured
- SAM CLI installed (for local testing)

#### Project Structure for Lambda

```
lambda/
├── app/                # Application code
├── Dockerfile          # Container image for Lambda
├── requirements.txt    # Python dependencies
├── template.yaml       # SAM template
└── events/             # Test events for local testing
```

#### Dockerfile for Lambda

```dockerfile
FROM public.ecr.aws/lambda/python:3.10

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY config/ ${LAMBDA_TASK_ROOT}/config/

# Set the handler
CMD ["app.lambda_handler.handler"]
```

#### SAM Template

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: SynthLang Proxy Lambda Function

Resources:
  SynthLangFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      MemorySize: 1024
      Timeout: 30
      Environment:
        Variables:
          OPENAI_API_KEY: !Ref OpenAIApiKey
          ENCRYPTION_KEY: !Ref EncryptionKey
          DATABASE_URL: !Ref DatabaseUrl
          USE_SYNTHLANG: '1'
          ENABLE_CACHE: '1'
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
    Metadata:
      DockerTag: latest
      DockerContext: .
      Dockerfile: Dockerfile

Parameters:
  OpenAIApiKey:
    Type: String
    Description: OpenAI API Key
    NoEcho: true
  EncryptionKey:
    Type: String
    Description: Encryption Key for sensitive data
    NoEcho: true
  DatabaseUrl:
    Type: String
    Description: PostgreSQL Database URL
    NoEcho: true

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
```

#### Lambda Handler

```python
# app/lambda_handler.py
import json
import asyncio
from mangum import Mangum
from app.main import app

# Create Mangum handler
handler = Mangum(app)
```

#### Deploy to AWS Lambda

```bash
# Build and deploy with SAM CLI
sam build
sam deploy --guided
```

### Google Cloud Functions Deployment

#### Prerequisites

- Google Cloud Platform account
- Google Cloud SDK installed and configured

#### Project Structure for Cloud Functions

```
cloud-functions/
├── app/                # Application code
├── main.py             # Entry point for Cloud Functions
├── requirements.txt    # Python dependencies
└── .gcloudignore       # Files to exclude from deployment
```

#### Entry Point for Cloud Functions

```python
# main.py
from app.main import app
from functions_framework import http

@http
def handle_request(request):
    """HTTP Cloud Function entry point."""
    return app(request)
```

#### Deploy to Google Cloud Functions

```bash
gcloud functions deploy synthlang-proxy \
  --runtime python310 \
  --trigger-http \
  --entry-point handle_request \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_openai_api_key,ENCRYPTION_KEY=your_encryption_key,DATABASE_URL=your_database_url
```

## Traditional Server Deployment

### Prerequisites

- Linux server (Ubuntu 20.04 LTS recommended)
- Python 3.10 or later
- PostgreSQL database
- Nginx web server (recommended)

### Installation Steps

1. Install system dependencies:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx postgresql
```

2. Create a user for the application:

```bash
sudo useradd -m -s /bin/bash synthlang
sudo su - synthlang
```

3. Clone the repository:

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy
```

4. Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure environment variables:

```bash
cp .env.sample .env
nano .env
# Edit the environment variables as needed
```

6. Create a systemd service:

```bash
sudo nano /etc/systemd/system/synthlang.service
```

Add the following content:

```
[Unit]
Description=SynthLang Proxy
After=network.target

[Service]
User=synthlang
WorkingDirectory=/home/synthlang/synthlang-proxy
Environment="PATH=/home/synthlang/synthlang-proxy/venv/bin"
EnvironmentFile=/home/synthlang/synthlang-proxy/.env
ExecStart=/home/synthlang/synthlang-proxy/venv/bin/python -m src.app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

7. Configure Nginx as a reverse proxy:

```bash
sudo nano /etc/nginx/sites-available/synthlang
```

Add the following content:

```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

8. Enable the Nginx site:

```bash
sudo ln -s /etc/nginx/sites-available/synthlang /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

9. Start the service:

```bash
sudo systemctl enable synthlang
sudo systemctl start synthlang
```

### SSL/TLS with Certbot

To secure your deployment with HTTPS:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Platform-as-a-Service (PaaS) Deployment

### Deploying to Fly.io

#### Prerequisites

- Fly.io account
- Fly CLI installed

#### Configuration

1. Create a `fly.toml` file:

```toml
app = "synthlang-proxy"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 1024

[[mounts]]
  source = "data"
  destination = "/app/data"
```

2. Set up secrets:

```bash
fly secrets set OPENAI_API_KEY=your_openai_api_key
fly secrets set ENCRYPTION_KEY=your_encryption_key
fly secrets set DATABASE_URL=your_database_url
```

3. Deploy the application:

```bash
fly deploy
```

### Deploying to Heroku

1. Create a `Procfile`:

```
web: python -m src.app.main
```

2. Create a `runtime.txt`:

```
python-3.10.12
```

3. Set up environment variables:

```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set ENCRYPTION_KEY=your_encryption_key
heroku config:set DATABASE_URL=your_database_url
```

4. Deploy to Heroku:

```bash
git push heroku main
```

### Deploying to Render

1. Create a new Web Service on Render
2. Link your repository
3. Configure environment variables
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `python -m src.app.main`

## High-Availability Deployment

For production environments requiring high availability, consider these additional steps:

### Load Balancing

1. Deploy multiple instances of SynthLang Proxy
2. Set up a load balancer (e.g., AWS ELB, Nginx, HAProxy)
3. Configure health checks to detect and replace unhealthy instances

Example Nginx load balancer configuration:

```
upstream synthlang {
    server synthlang1.example.com;
    server synthlang2.example.com;
    server synthlang3.example.com;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://synthlang;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Database High Availability

1. Set up database replication
2. Configure read replicas for read-heavy workloads
3. Consider managed database services (e.g., AWS RDS, Azure Database, Google Cloud SQL)

### Caching Layer

1. Set up Redis or Memcached for distributed caching
2. Configure SynthLang Proxy to use the distributed cache

Example Redis configuration in `.env`:

```
CACHE_TYPE=redis
REDIS_URL=redis://redis-host:6379/0
```

## Monitoring and Logging

### Prometheus Metrics

SynthLang Proxy exposes metrics at the `/metrics` endpoint.

Example Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'synthlang'
    scrape_interval: 15s
    static_configs:
      - targets: ['synthlang:8000']
```

### Grafana Dashboards

Set up Grafana dashboards to visualize metrics:

1. Import the provided dashboard template
2. Configure data source to point to your Prometheus instance
3. Customize alerts and notifications

### Log Aggregation

Configure log aggregation with tools like:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Graylog
- Loki

Example Filebeat configuration for log shipping:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/synthlang/*.log

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

## Security Considerations

### API Key Protection

- Store API keys in environment variables or a secrets manager
- Never commit API keys to source control
- Rotate API keys regularly

### Network Security

- Use HTTPS for all communications
- Configure firewalls to restrict access
- Implement rate limiting and request validation

### Database Security

- Use TLS for database connections
- Restrict database access to necessary IP addresses
- Use strong passwords and consider certificate authentication

### Container Security

- Use minimal base images
- Run containers as non-root users
- Scan container images for vulnerabilities

## Scaling Considerations

### Vertical Scaling

- Increase CPU and memory resources
- Upgrade database to higher performance tiers

### Horizontal Scaling

- Deploy multiple instances behind a load balancer
- Shard database for write-heavy workloads
- Use read replicas for read-heavy workloads

### Autoscaling

Configure autoscaling based on metrics:

- CPU utilization
- Memory usage
- Request rate
- Response time

Example AWS Auto Scaling configuration:

```yaml
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      MetricsCollection:
        - Granularity: 1Minute
      AutoScalingGroupName: SynthLangProxyASG
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
      TargetGroupARNs:
        - !Ref TargetGroup
      VPCZoneIdentifier: !Ref Subnets
      
  ScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      AutoScalingGroupName: !Ref AutoScalingGroup
      PolicyType: TargetTrackingScaling
      TargetTrackingConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ASGAverageCPUUtilization
        TargetValue: 70.0
```

## Backup and Disaster Recovery

### Database Backups

1. Configure automated database backups
2. Test restore procedures regularly
3. Store backups in multiple locations

Example PostgreSQL backup script:

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="/var/backups/postgresql"
DATABASE="synthlang"
USER="postgres"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -U $USER $DATABASE | gzip > $BACKUP_DIR/$DATABASE-$TIMESTAMP.sql.gz

# Delete backups older than 30 days
find $BACKUP_DIR -name "$DATABASE-*.sql.gz" -mtime +30 -delete
```

### Configuration Backups

1. Store configuration files in version control
2. Document environment variables
3. Automate environment setup

### Disaster Recovery Plan

1. Document recovery procedures
2. Set up monitoring and alerting
3. Test recovery procedures regularly
4. Define RPO (Recovery Point Objective) and RTO (Recovery Time Objective)

## Cost Optimization

### Resource Optimization

- Configure proper instance sizes
- Use spot/preemptible instances for non-critical workloads
- Implement autoscaling to match demand

### Cost Analysis

- Monitor usage patterns
- Use cloud provider cost analysis tools
- Set up budget alerts

### Request Optimization

- Optimize prompt compression
- Configure semantic caching
- Batch requests when possible

## Performance Tuning

### Worker Configuration

For Gunicorn/Uvicorn environments:

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Determine the optimal number of workers:
- CPU-bound: `2 * number_of_cores + 1`
- I/O-bound: `number_of_cores * 2` or higher

### Database Optimization

- Index frequently queried fields
- Optimize query patterns
- Configure connection pooling

### Caching Strategy

- Tune cache size and eviction policies
- Monitor cache hit rates
- Consider hierarchical caching (memory, Redis, database)

## Upgrading and Maintenance

### Rolling Updates

To perform zero-downtime updates:

1. Deploy new instances with updated code
2. Verify health of new instances
3. Gradually shift traffic from old to new instances
4. Remove old instances once traffic is fully migrated

### Database Migrations

Run database migrations safely:

```bash
# Using Alembic
alembic upgrade head
```

For critical systems, consider:
1. Testing migrations on a staging environment
2. Creating database snapshots before migration
3. Having a rollback plan

### Maintenance Windows

For activities requiring downtime:

1. Notify users in advance
2. Schedule during low-traffic periods
3. Update status page during maintenance
4. Test thoroughly before and after maintenance

## Troubleshooting Deployment Issues

### Common Issues

1. **Database Connection Failures**
   - Check network connectivity
   - Verify database credentials
   - Check security group/firewall settings

2. **Memory Issues**
   - Increase container/server memory
   - Check for memory leaks
   - Configure proper garbage collection

3. **API Rate Limits**
   - Implement backoff strategies
   - Distribute requests across multiple API keys
   - Cache responses when possible

4. **Load Balancer Issues**
   - Check health check configuration
   - Verify instance registration
   - Check for certificate errors

### Debugging Techniques

1. **Check Logs**
   ```bash
   journalctl -u synthlang.service -f
   ```

2. **Monitor Resource Usage**
   ```bash
   htop
   ```

3. **Test Connectivity**
   ```bash
   curl -v http://localhost:8000/health
   ```

4. **Check Container Status**
   ```bash
   docker logs synthlang-proxy
   ```

## Deployment Checklist

Use this checklist before deploying to production:

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security features enabled (HTTPS, authentication)
- [ ] Monitoring and logging configured
- [ ] Backup strategy implemented
- [ ] Load testing performed
- [ ] Resource scaling configured
- [ ] Documentation updated
- [ ] Rollback plan prepared

## Environment-Specific Configurations

### Development

```bash
DEBUG=true
LOG_LEVEL=DEBUG
USE_SQLITE=1
```

### Staging

```bash
DEBUG=false
LOG_LEVEL=INFO
ENABLE_CACHE=1
```

### Production

```bash
DEBUG=false
LOG_LEVEL=WARNING
ENABLE_CACHE=1
AUTO_MIGRATE=0  # Manual migrations only
```

## Appendix

### Complete Environment Variable Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Port to listen on | `8000` | No |
| `HOST` | Host to bind to | `0.0.0.0` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `ENCRYPTION_KEY` | Key for encrypting sensitive data | - | Yes |
| `DATABASE_URL` | PostgreSQL connection URL | - | Yes (if not using SQLite) |
| `USE_SQLITE` | Use SQLite instead of PostgreSQL | `0` | No |
| `SQLITE_PATH` | SQLite database path | `sqlite+aiosqlite:///./synthlang_proxy.db` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `DEFAULT_MODEL` | Default LLM model | `gpt-4o` | No |
| `USE_SYNTHLANG` | Enable SynthLang compression | `1` | No |
| `ENABLE_CACHE` | Enable semantic caching | `1` | No |
| `CACHE_SIMILARITY_THRESHOLD` | Threshold for cache hits | `0.95` | No |
| `CACHE_MAX_ITEMS` | Maximum cache items | `1000` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `LOG_FILE` | Log file path | `proxy.log` | No |
| `ADMIN_USERS` | Admin user IDs (comma-separated) | - | No |
| `PREMIUM_USERS` | Premium user IDs (comma-separated) | - | No |
| `DEFAULT_ROLE` | Default user role | `basic` | No |

### Scripts

#### Database Initialization Script

```bash
#!/bin/bash
# init-db.sh
set -e

# Create database and user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE synthlang;
    CREATE USER synthlang WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE synthlang TO synthlang;
EOSQL
```

#### Deployment Script

```bash
#!/bin/bash
# deploy.sh
set -e

# Pull latest changes
git pull

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Restart the service
sudo systemctl restart synthlang
```

#### Backup Script

```bash
#!/bin/bash
# backup.sh
set -e

# Variables
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="/var/backups/synthlang"
DATABASE_URL="postgresql://user:password@host:port/synthlang"
S3_BUCKET="synthlang-backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Dump database
pg_dump $DATABASE_URL | gzip > $BACKUP_DIR/synthlang-$TIMESTAMP.sql.gz

# Copy to S3
aws s3 cp $BACKUP_DIR/synthlang-$TIMESTAMP.sql.gz s3://$S3_BUCKET/

# Delete old backups (keep last 30 days)
find $BACKUP_DIR -name "synthlang-*.sql.gz" -mtime +30 -delete