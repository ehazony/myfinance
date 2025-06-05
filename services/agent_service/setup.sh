#!/bin/bash

# Setup script for agent_service
# This script handles the installation of dependencies including the local finance_common package

set -e  # Exit on any error

echo "🚀 Setting up agent_service..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FINANCE_COMMON_PATH="$PROJECT_ROOT/finance_common"

echo "📍 Script directory: $SCRIPT_DIR"
echo "📍 Project root: $PROJECT_ROOT" 
echo "📍 Finance common path: $FINANCE_COMMON_PATH"

# Check if finance_common directory exists
if [ ! -d "$FINANCE_COMMON_PATH" ]; then
    echo "❌ Error: finance_common directory not found at $FINANCE_COMMON_PATH"
    echo "   Make sure you're running this script from the correct location"
    exit 1
fi

# Check if setup.py exists in finance_common
if [ ! -f "$FINANCE_COMMON_PATH/setup.py" ]; then
    echo "❌ Error: setup.py not found in finance_common directory"
    echo "   finance_common package is not properly configured"
    exit 1
fi

echo "✅ finance_common directory found and validated"

# Install finance_common as editable package
echo "📦 Installing finance_common as editable package..."
pip install -e "$FINANCE_COMMON_PATH"

# Install other requirements
echo "📦 Installing other requirements..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "✅ Setup completed successfully!"
echo ""
echo "You can now run the agent service:"
echo "  cd $SCRIPT_DIR"
echo "  python main.py" 