#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}SynthLang Proxy Examples${NC}"
echo -e "${BLUE}This script demonstrates the proxy capabilities of SynthLang CLI${NC}\n"

# Check if synthlang is installed
if ! command -v synthlang &> /dev/null; then
    echo -e "${RED}Error: synthlang command not found.${NC}"
    echo -e "Please install SynthLang CLI with: pip install synthlang"
    exit 1
fi

# Example 1: Compression
echo -e "\n${GREEN}Example 1: Prompt Compression${NC}"
echo -e "${BLUE}Compressing a prompt using SynthLang compression:${NC}"
PROMPT="Design a system architecture for a microservices-based e-commerce platform with user authentication, product catalog, shopping cart, payment processing, and order management. Include considerations for scalability, reliability, and security."
echo -e "Original prompt: ${PROMPT}"
echo -e "\nCompressing..."
synthlang proxy compress "${PROMPT}"

echo -e "\n${BLUE}Compressing with gzip for maximum compression:${NC}"
synthlang proxy compress --use-gzip "${PROMPT}"

# Example 2: Chat Completion
echo -e "\n${GREEN}Example 2: Chat Completion${NC}"
echo -e "${BLUE}Sending a chat request to the proxy:${NC}"
echo -e "Query: What is the capital of France?"
echo -e "\nResponse:"
synthlang proxy chat "What is the capital of France?"

# Example 3: Translation with Proxy
echo -e "\n${GREEN}Example 3: Translation with Proxy${NC}"
echo -e "${BLUE}Translating a prompt using the proxy service:${NC}"
TRANSLATE_PROMPT="Create a data pipeline for processing customer feedback and generating insights"
echo -e "Prompt: ${TRANSLATE_PROMPT}"
echo -e "\nTranslating..."
synthlang translate --source "${TRANSLATE_PROMPT}" --framework synthlang --use-proxy

# Example 4: Cache Management
echo -e "\n${GREEN}Example 4: Cache Management${NC}"
echo -e "${BLUE}Checking cache statistics:${NC}"
synthlang proxy cache-stats

echo -e "\n${BLUE}Clearing the cache:${NC}"
synthlang proxy clear-cache

# Example 5: Agent Tools
echo -e "\n${GREEN}Example 5: Agent Tools${NC}"
echo -e "${BLUE}Listing available tools:${NC}"
synthlang proxy tools

echo -e "\n${BLUE}Calling a calculation tool:${NC}"
synthlang proxy call-tool --tool "calculate" --args '{"expression": "2 * 3.14159 * 5"}'

# Example 6: Starting a Local Server (commented out to avoid blocking the script)
echo -e "\n${GREEN}Example 6: Local Proxy Server${NC}"
echo -e "${BLUE}To start a local proxy server, run:${NC}"
echo -e "synthlang proxy serve --port 8000"
echo -e "${YELLOW}(This command is not executed automatically as it would block the script)${NC}"

echo -e "\n${GREEN}All examples completed successfully!${NC}"
echo -e "${BLUE}For more information, see the documentation:${NC}"
echo -e "- README.md"
echo -e "- docs/tutorials/proxy_integration_tutorial.md"