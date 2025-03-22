#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting SynthLang CLI deployment to PyPI...${NC}"

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    echo -e "${RED}Error: pyproject.toml not found. Please run this script from the cli directory.${NC}"
    exit 1
fi

# Clean up existing distributions
echo -e "${YELLOW}Cleaning up old distribution files...${NC}"
rm -rf dist/* 2>/dev/null || true

# Build the package
echo -e "${YELLOW}Building package...${NC}"
poetry build

# Check if build was successful
if [[ ! -d "dist" ]]; then
    echo -e "${RED}Error: Build failed - dist directory not created${NC}"
    exit 1
fi

# Upload to PyPI
echo -e "${YELLOW}Uploading to PyPI...${NC}"
poetry publish

echo -e "${GREEN}Deployment completed successfully!${NC}"

# Get the version from pyproject.toml
VERSION=$(grep "version = " pyproject.toml | cut -d'"' -f2)
echo -e "${GREEN}Package version ${VERSION} is now available on PyPI${NC}"
echo -e "${GREEN}View at: https://pypi.org/project/synthlang/${VERSION}/${NC}"
