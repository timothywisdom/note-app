#!/bin/bash

# Parse command line arguments
DEBUG_MODE=false
DEBUG_PORT=5678
while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            DEBUG_MODE=true
            shift
            ;;
        --debug-port)
            DEBUG_PORT="$2"
            DEBUG_MODE=true
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--debug] [--debug-port PORT]"
            echo "  --debug        Enable debug mode (default port: 5678)"
            echo "  --debug-port   Specify debug port and enable debug mode"
            exit 1
            ;;
    esac
done

echo "🚀 Starting NoteApp FastAPI Application..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
if [ "$DEBUG_MODE" = true ]; then
    echo "🐛 Debug mode: ENABLED - Waiting for debugger connection..."
fi
echo ""

# Change to server directory
cd server

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies only if not already installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Dependencies already installed"
fi

# Start the application
echo "🌟 Starting FastAPI server..."
echo "Press Ctrl+C to stop the server"
echo ""

# Set environment variables for debug mode
if [ "$DEBUG_MODE" = true ]; then
    export DEBUG_MODE=true
    export DEBUG_PORT=${DEBUG_PORT:-5678}
fi

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
