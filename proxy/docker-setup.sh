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
echo -e "${BLUE}|${NC}  ${YELLOW}SynthLang Proxy Docker Setup${NC}               ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}                                               ${BLUE}|${NC}"
echo -e "${BLUE}+-----------------------------------------------+${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo -e "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed.${NC}"
    echo -e "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}No .env file found. Creating from .env.sample...${NC}"
    
    if [ ! -f ".env.sample" ]; then
        echo -e "${RED}Error: .env.sample file not found.${NC}"
        exit 1
    fi
    
    cp .env.sample .env
    
    # Generate encryption key
    ENCRYPTION_KEY=$(openssl rand -hex 16)
    sed -i "s/ENCRYPTION_KEY=/ENCRYPTION_KEY=$ENCRYPTION_KEY/g" .env
    
    echo -e "${GREEN}Created .env file with a generated encryption key.${NC}"
    echo -e "${YELLOW}Please edit the .env file to set your OPENAI_API_KEY.${NC}"
    
    # Open the .env file in the default editor
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo -e "${YELLOW}Please edit the .env file manually to set your OPENAI_API_KEY.${NC}"
    fi
else
    echo -e "${GREEN}Found existing .env file.${NC}"
fi

# Check if .api_keys.json exists
if [ ! -f ".api_keys.json" ]; then
    echo -e "${YELLOW}No .api_keys.json file found. Creating default...${NC}"
    
    # Create default API keys file
    cat > .api_keys.json << EOL
{
  "api_keys": {
    "sk_$(openssl rand -hex 16)": "admin_user",
    "sk_$(openssl rand -hex 16)": "test_user"
  },
  "rate_limits": {
    "admin_user": 100,
    "test_user": 50
  }
}
EOL
    
    echo -e "${GREEN}Created default .api_keys.json file.${NC}"
    
    # Extract the admin API key
    ADMIN_API_KEY=$(grep -o '"sk_[a-f0-9]\+": "admin_user"' .api_keys.json | cut -d'"' -f2)
    TEST_API_KEY=$(grep -o '"sk_[a-f0-9]\+": "test_user"' .api_keys.json | cut -d'"' -f2)
    
    # Update .env with the API keys
    sed -i "s/API_KEY=/API_KEY=$TEST_API_KEY/g" .env
    sed -i "s/ADMIN_API_KEY=/ADMIN_API_KEY=$ADMIN_API_KEY/g" .env
    
    echo -e "${GREEN}Updated .env with generated API keys.${NC}"
else
    echo -e "${GREEN}Found existing .api_keys.json file.${NC}"
fi

# Ask if user wants to use SQLite or PostgreSQL
echo -e "\n${YELLOW}Database Configuration:${NC}"
echo -e "1) SQLite (default, simpler setup)"
echo -e "2) PostgreSQL (better for production)"
read -p "Select database type [1/2]: " db_choice

if [ "$db_choice" = "2" ]; then
    # Configure for PostgreSQL
    sed -i "s/USE_SQLITE=1/USE_SQLITE=0/g" .env
    echo -e "${GREEN}Configured to use PostgreSQL.${NC}"
else
    # Configure for SQLite
    sed -i "s/USE_SQLITE=0/USE_SQLITE=1/g" .env
    echo -e "${GREEN}Configured to use SQLite.${NC}"
fi

# Build and start the containers
echo -e "\n${YELLOW}Building and starting containers...${NC}"
docker-compose up -d --build

# Check if containers are running
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}SynthLang Proxy is now running!${NC}"
    echo -e "Access the API at: ${BLUE}http://localhost:8000${NC}"
    echo -e "API Documentation: ${BLUE}http://localhost:8000/docs${NC}"
    
    # Show API keys
    echo -e "\n${YELLOW}API Keys:${NC}"
    echo -e "Admin API Key: ${BLUE}$(grep ADMIN_API_KEY .env | cut -d'=' -f2)${NC}"
    echo -e "User API Key: ${BLUE}$(grep "^API_KEY=" .env | cut -d'=' -f2)${NC}"
    
    echo -e "\n${YELLOW}Useful Commands:${NC}"
    echo -e "View logs: ${BLUE}docker-compose logs -f proxy${NC}"
    echo -e "Stop service: ${BLUE}docker-compose down${NC}"
    echo -e "Restart service: ${BLUE}docker-compose restart proxy${NC}"
else
    echo -e "\n${RED}Failed to start containers. Check the error messages above.${NC}"
fi