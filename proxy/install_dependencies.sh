#!/bin/bash
# Script to install dependencies for the SynthLang proxy

echo "Installing dependencies for SynthLang proxy..."

# Install setuptools and wheel first to ensure proper package building
pip install setuptools==68.0.0 wheel==0.41.0

# Install the rest of the dependencies one by one
pip install fastapi==0.104.1
pip install uvicorn==0.23.2
pip install pydantic==2.6.0
pip install pytest==8.0.0
pip install httpx==0.25.1
pip install python-multipart==0.0.9
pip install python-dotenv==1.0.1
pip install cryptography==41.0.7
pip install numpy==1.26.0
pip install sqlalchemy==2.0.25
pip install asyncpg==0.29.0
pip install aiosqlite==0.19.0
pip install openai==1.10.0
pip install tomli==2.0.0
pip install tomli_w==1.0.0
pip install scikit-learn==1.3.0

echo "Dependencies installed successfully!"