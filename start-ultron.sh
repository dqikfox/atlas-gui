#!/bin/bash

# Ultron Agent Startup Script
# Starts the React development server

echo "⚡ Starting Ultron Agent..."
echo "================================"

cd /workspace/ultron-agent

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🚀 Starting development server..."
echo "Access the application at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo "================================"

npm start
