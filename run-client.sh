#!/bin/bash

echo "🚀 Starting NoteApp Client..."
echo "📍 Client will be available at: http://localhost:3000"
echo ""

# Change to client directory
cd client

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing client dependencies..."
    npm install
fi

# Start the development server
echo "🌟 Starting Next.js development server..."
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
