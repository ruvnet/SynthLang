#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Welcome message
echo -e "\n${BLUE}+-----------------------------------------------+${NC}"
echo -e "${BLUE}|${NC}                                               ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}  ${YELLOW}SynthLang Proxy Docker Test${NC}                ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}                                               ${BLUE}|${NC}"
echo -e "${BLUE}+-----------------------------------------------+${NC}\n"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker is not running.${NC}"
    echo -e "Please start Docker and try again."
    exit 1
fi

# Check if the proxy container is running
if ! docker-compose ps | grep -q "proxy.*Up"; then
    echo -e "${RED}Error: SynthLang Proxy container is not running.${NC}"
    echo -e "Please start the container with: docker-compose up -d"
    exit 1
fi

# Get API key from .env file
API_KEY=$(grep "^API_KEY=" .env | cut -d'=' -f2)
if [ -z "$API_KEY" ]; then
    echo -e "${RED}Error: API_KEY not found in .env file.${NC}"
    exit 1
fi

echo -e "${YELLOW}Testing API health endpoint...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo -e "Response: $HEALTH_RESPONSE"
    exit 1
fi

echo -e "\n${YELLOW}Testing API authentication...${NC}"
AUTH_RESPONSE=$(curl -s -H "Authorization: Bearer $API_KEY" http://localhost:8000/v1/synthlang/status)
if [[ $AUTH_RESPONSE == *"error"* ]]; then
    echo -e "${RED}✗ Authentication failed${NC}"
    echo -e "Response: $AUTH_RESPONSE"
else
    echo -e "${GREEN}✓ Authentication successful${NC}"
fi

echo -e "\n${YELLOW}Testing simple chat completion...${NC}"
CHAT_RESPONSE=$(curl -s -X POST \
  http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Say hello world"}
    ]
  }')

if [[ $CHAT_RESPONSE == *"error"* ]]; then
    echo -e "${RED}✗ Chat completion failed${NC}"
    echo -e "Response: $CHAT_RESPONSE"
else
    echo -e "${GREEN}✓ Chat completion successful${NC}"
    CONTENT=$(echo $CHAT_RESPONSE | grep -o '"content":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo -e "Response content: ${BLUE}$CONTENT${NC}"
fi

echo -e "\n${YELLOW}Testing database connection...${NC}"
DB_STATUS=$(docker-compose exec -T proxy python -c "
import asyncio
import sys
sys.path.append('.')
from src.app.database import init_db

async def test_db():
    try:
        result = await init_db()
        return 'success' if result else 'failure'
    except Exception as e:
        return f'error: {str(e)}'

if __name__ == '__main__':
    print(asyncio.run(test_db()))
")

if [[ $DB_STATUS == *"success"* ]]; then
    echo -e "${GREEN}✓ Database connection successful${NC}"
else
    echo -e "${RED}✗ Database connection failed${NC}"
    echo -e "Status: $DB_STATUS"
fi

echo -e "\n${YELLOW}Testing API key management...${NC}"
KEYS_STATUS=$(docker-compose exec -T proxy python -m src.cli.api_keys list)

if [[ $KEYS_STATUS == *"API keys"* ]]; then
    echo -e "${GREEN}✓ API key management working${NC}"
    echo -e "Found keys: $(echo "$KEYS_STATUS" | grep -c "API Key:")"
else
    echo -e "${RED}✗ API key management failed${NC}"
    echo -e "Status: $KEYS_STATUS"
fi

echo -e "\n${GREEN}All tests completed!${NC}"