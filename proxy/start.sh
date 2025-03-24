#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Clear the screen
clear

# Welcome message with simple border
echo -e "\n${BLUE}+-----------------------------------------------+${NC}"
echo -e "${BLUE}|${NC}                                               ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}  ${YELLOW}SynthLang Proxy v0.1${NC}                       ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}  ${GREEN}High-performance LLM router with caching${NC}    ${BLUE}|${NC}"
echo -e "${BLUE}|${NC}                                               ${BLUE}|${NC}"
echo -e "${BLUE}+-----------------------------------------------+${NC}\n"

# Load environment variables from .env file
echo -e "🔍 ${YELLOW}Checking environment...${NC}"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✓ Found .env file${NC}"
    echo -e "   ${GREEN}✓ Loading environment variables${NC}"
    
    # Export all variables from .env file, ensuring proper format
    # Convert any "KEY: VALUE" format to "KEY=VALUE" format
    set -a
    source <(sed 's/: /=/g' .env)
    set +a
else
    echo -e "   ${RED}✗ .env file not found${NC}"
    echo -e "   ${YELLOW}⚠️  Make sure to set OPENAI_API_KEY manually${NC}"
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "\n${RED}❌ Error: OPENAI_API_KEY environment variable is not set.${NC}"
    echo -e "${YELLOW}Please create a .env file with OPENAI_API_KEY=your_api_key or set it manually.${NC}\n"
    exit 1
else
    echo -e "   ${GREEN}✓ OPENAI_API_KEY is set${NC}"
fi

# Check if DATABASE_URL is set, if not set a default
if [ -z "$DATABASE_URL" ]; then
    echo -e "   ${YELLOW}⚠️  DATABASE_URL not set, using SQLite${NC}"
    export USE_SQLITE=1
    export SQLITE_PATH="sqlite+aiosqlite:///./synthlang_proxy.db"
else
    echo -e "   ${GREEN}✓ DATABASE_URL is set${NC}"
fi

# Check if ENCRYPTION_KEY is set, if not generate one
if [ -z "$ENCRYPTION_KEY" ]; then
    echo -e "   ${YELLOW}⚠️  ENCRYPTION_KEY not set, will generate one${NC}"
    # Generate a random encryption key
    export ENCRYPTION_KEY=$(openssl rand -hex 16)
    echo -e "   ${GREEN}✓ Generated ENCRYPTION_KEY: ${ENCRYPTION_KEY}${NC}"
    echo -e "   ${YELLOW}⚠️  Consider adding this to your .env file for persistence${NC}"
else
    echo -e "   ${GREEN}✓ ENCRYPTION_KEY is set${NC}"
fi

# Initialization message
echo -e "\n🔧 ${YELLOW}Initializing server...${NC}"
echo -e "   ${GREEN}✓ Configuration loaded${NC}"

# Run the server with environment variables
echo -e "\n🚀 ${GREEN}Starting SynthLang proxy server...${NC}\n"
uvicorn src.app.main:app --reload