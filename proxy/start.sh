#!/bin/bash

# Debug: Print current working directory
echo "Current working directory: $(pwd)"

# Debug: Check if venv activate script exists
if [ -f "proxy/venv/bin/activate" ]; then
  echo "venv activate script exists"
else
  echo "venv activate script DOES NOT exist"
  exit 1
fi

# Activate virtual environment
source proxy/venv/bin/activate

# Debug: List pip packages after activation
echo "List of pip packages in virtual environment:"
pip list

# Set PYTHONPATH to include the root directory
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "PYTHONPATH set to: $PYTHONPATH"

# Change working directory to root
cd /workspaces/SynthLang

# Add sys.path modification to help Python find modules
echo "
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
" > proxy/src/app/path_fix.py

# Run uvicorn command with module path
cd proxy && uvicorn src.app.main:app --reload