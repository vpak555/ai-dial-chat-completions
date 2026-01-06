#!/bin/bash

# Quick test script for the DIAL Chat Completion application
# Usage: ./test_run.sh

echo "🚀 Starting DIAL Chat Application Test..."
echo ""

# Check if API key is set
if [ -z "$DIAL_API_KEY" ]; then
    echo "⚠️  DIAL_API_KEY is not set!"
    echo "Setting it from inline value..."
    export DIAL_API_KEY='dial-3d5hy3f74s7n1cf5eb5xkbvkwbs'
fi

# Activate virtual environment
source .venv/bin/activate

echo "✅ Virtual environment activated"
echo "✅ API Key is set"
echo ""
echo "================================================"
echo "Starting the chat application..."
echo "================================================"
echo ""
echo "TIP: Try these test scenarios:"
echo "  1. Simple Q&A: 'What is the capital of France?'"
echo "  2. Math: 'What is 15 * 7?'"
echo "  3. Conversation history: Say 'My name is Bob', then ask 'What is my name?'"
echo "  4. Type 'exit' to quit"
echo ""

# Run the application
python3 -m task.app

