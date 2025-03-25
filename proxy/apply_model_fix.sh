#!/bin/bash

# Script to apply the model selection fix

# Check if the new files exist
if [ ! -f "src/app/main.py.new" ] || [ ! -f "src/app/models_endpoint.py.new" ]; then
    echo "Error: New files not found. Make sure you're running this script from the proxy directory."
    exit 1
fi

# Create backups of the original files
echo "Creating backups of original files..."
cp src/app/main.py src/app/main.py.bak
cp src/app/models_endpoint.py src/app/models_endpoint.py.bak

# Apply the changes
echo "Applying changes to main.py..."
mv src/app/main.py.new src/app/main.py

echo "Applying changes to models_endpoint.py..."
mv src/app/models_endpoint.py.new src/app/models_endpoint.py

echo "Changes applied successfully!"
echo "Restart the server for changes to take effect."
echo "If you encounter any issues, you can restore the backups with:"
echo "  mv src/app/main.py.bak src/app/main.py"
echo "  mv src/app/models_endpoint.py.bak src/app/models_endpoint.py"