#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo -e "\n${BLUE}+-----------------------------------------------+${NC}"
echo -e "${BLUE}|                                               |${NC}"
echo -e "${BLUE}|  ${GREEN}SynthLang Proxy Docker Test${BLUE}                |${NC}"
echo -e "${BLUE}|                                               |${NC}"
echo -e "${BLUE}+-----------------------------------------------+${NC}\n"

# Function to check if docker-compose is running
check_running() {
  if ! docker-compose ps | grep -q "Up"; then
    echo -e "${RED}Error: Docker containers are not running. Please start them with 'docker-compose up -d'${NC}"
    exit 1
  fi
}

# Test the API health endpoint
test_health() {
  echo "Testing API health endpoint..."
  HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
  
  if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo -e "${GREEN}✓ Health check passed${NC}\n"
  else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Response: $HEALTH_RESPONSE"
    exit 1
  fi
}

# Test API authentication
test_auth() {
  echo "Testing API authentication..."
  # Get the API key from .env file
  API_KEY=$(grep -E "^API_KEY=" .env | cut -d '=' -f2)
  
  if [ -z "$API_KEY" ]; then
    API_KEY="sk_acbed96a85a9ef05d014e145ba84a707" # Default test key
  fi
  
  AUTH_RESPONSE=$(curl -s -X GET http://localhost:8000/v1/models \
    -H "Authorization: Bearer $API_KEY")
  
  if [[ $AUTH_RESPONSE != *"error"* ]]; then
    echo -e "${GREEN}✓ Authentication successful${NC}\n"
  else
    echo -e "${RED}✗ Authentication failed${NC}"
    echo "Response: $AUTH_RESPONSE"
    exit 1
  fi
}

# Test simple chat completion
test_chat() {
  echo "Testing simple chat completion..."
  # Get the API key from .env file
  API_KEY=$(grep -E "^API_KEY=" .env | cut -d '=' -f2)
  
  if [ -z "$API_KEY" ]; then
    API_KEY="sk_acbed96a85a9ef05d014e145ba84a707" # Default test key
  fi
  
  CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{
      "model": "gpt-4o-mini",
      "messages": [
        {"role": "user", "content": "Say hello world"}
      ]
    }')
  
  if [[ $CHAT_RESPONSE == *"assistant"* ]]; then
    echo -e "${GREEN}✓ Chat completion successful${NC}"
    echo -e "Response content: $(echo $CHAT_RESPONSE | grep -o '"content":"[^"]*' | head -1 | sed 's/"content":"//')\n"
  else
    echo -e "${RED}✗ Chat completion failed${NC}"
    echo "Response: $CHAT_RESPONSE"
    exit 1
  fi
}

# Test database connection
test_db() {
  echo "Testing database connection..."
  DB_RESPONSE=$(docker-compose exec -T proxy python -c "
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set SQLite database path
os.environ['USE_SQLITE'] = '1'
os.environ['SQLITE_PATH'] = 'sqlite+aiosqlite:///./synthlang_proxy.db'

from src.app.database import init_db

async def test_db():
    try:
        await init_db()
        print('Database connection successful')
        return True
    except Exception as e:
        print(f'Database connection failed: {e}')
        return False

if asyncio.run(test_db()):
    sys.exit(0)
else:
    sys.exit(1)
")
  
  if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓ Database connection successful${NC}\n"
  else
    echo -e "${RED}✗ Database connection failed${NC}"
    echo "Response: $DB_RESPONSE"
    exit 1
  fi
}

# Test API key management
test_api_keys() {
  echo "Testing API key management..."
  # Get the admin API key from .env file
  ADMIN_API_KEY=$(grep -E "^ADMIN_API_KEY=" .env | cut -d '=' -f2)
  
  if [ -z "$ADMIN_API_KEY" ]; then
    ADMIN_API_KEY="sk_a006079d291f135266b0a5c15d87cce5" # Default admin key
  fi
  
  API_KEYS_RESPONSE=$(docker-compose exec -T proxy python -c "
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set SQLite database path
os.environ['USE_SQLITE'] = '1'
os.environ['SQLITE_PATH'] = 'sqlite+aiosqlite:///./synthlang_proxy.db'

from src.app.auth.api_keys import API_KEYS

async def test_api_keys():
    try:
        print(f'Found keys: {len(API_KEYS)}')
        return True
    except Exception as e:
        print(f'API key management failed: {e}')
        return False

if asyncio.run(test_api_keys()):
    sys.exit(0)
else:
    sys.exit(1)
")
  
  if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓ API key management working${NC}"
    echo "Found keys: $(echo "$API_KEYS_RESPONSE" | grep -o 'Found keys: [0-9]*' | cut -d ' ' -f 3)"
  else
    echo -e "${RED}✗ API key management failed${NC}"
    echo "Response: $API_KEYS_RESPONSE"
    exit 1
  fi
}

# Run all tests
check_running
test_health
test_auth
test_chat
test_db
test_api_keys

echo -e "\nAll tests completed!"