#!/bin/bash

# Navigate to the proxy directory (Not needed as script is already in proxy/)

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install latest faiss-cpu separately
pip install faiss-cpu

# Remove version constraint for faiss-cpu in requirements.txt
sed -i 's/faiss-cpu>=1.7.4,<1.8.0/faiss-cpu/g' requirements.txt

# Install requirements
pip install -r requirements.txt

echo "Installation completed successfully!"