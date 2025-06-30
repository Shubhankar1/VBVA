#!/bin/bash

# VBVA Startup Script
# Simple wrapper for the robust Python startup script

echo "🚀 VBVA - Video-Based Virtual Assistant"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "start_robust.py" ]; then
    echo "❌ Please run this script from the VBVA project root directory"
    exit 1
fi

# Make the Python script executable
chmod +x start_robust.py

# Run the robust startup script
echo "Starting VBVA with robust configuration..."
python3 start_robust.py

# Exit with the same code as the Python script
exit $? 