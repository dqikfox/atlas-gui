#!/bin/bash

# ULTRON Agent Web Dashboard Installation Script
# This script sets up the web dashboard for your existing ULTRON Agent

echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo "  ULTRON AGENT WEB DASHBOARD INSTALLER  "
echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo ""

# Check if we're in the ULTRON Agent directory
if [ ! -f "main.py" ] && [ ! -f "agent_core.py" ]; then
    echo "❌ This script should be run from your ULTRON Agent root directory"
    echo "   Please navigate to your ULTRON Agent folder and run this script again."
    exit 1
fi

echo "✅ Found ULTRON Agent directory"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn websockets aiohttp psutil

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    echo "   Please install manually: pip install fastapi uvicorn websockets aiohttp psutil"
    exit 1
fi

# Create necessary directories
echo ""
echo "📂 Creating directories..."
mkdir -p logs
mkdir -p screenshots
mkdir -p web_dashboard
echo "✅ Directories created"

# Copy web dashboard files to the project
echo ""
echo "📝 Copying web dashboard files..."

# Check if files exist in current directory
if [ -f "ultron-web-dashboard.html" ]; then
    cp ultron-web-dashboard.html .
    cp ultron-dashboard.js .
    cp ultron_web_server.py .
    cp launch_ultron_web.py .
    echo "✅ Web dashboard files copied"
else
    echo "❌ Web dashboard files not found in current directory"
    echo "   Please ensure the following files are present:"
    echo "   - ultron-web-dashboard.html"
    echo "   - ultron-dashboard.js"
    echo "   - ultron_web_server.py"
    echo "   - launch_ultron_web.py"
    exit 1
fi

# Make launch script executable
chmod +x launch_ultron_web.py

# Create a simple launcher batch file for Windows users
echo ""
echo "📝 Creating launcher scripts..."

cat > launch_web_dashboard.bat << 'EOF'
@echo off
echo Starting ULTRON Agent Web Dashboard...
python launch_ultron_web.py
pause
EOF

cat > launch_web_dashboard.sh << 'EOF'
#!/bin/bash
echo "Starting ULTRON Agent Web Dashboard..."
python3 launch_ultron_web.py
EOF

chmod +x launch_web_dashboard.sh

echo "✅ Launcher scripts created"

# Test the installation
echo ""
echo "🧪 Testing installation..."
python -c "import fastapi, uvicorn, websockets, aiohttp, psutil; print('✅ All dependencies available')"

if [ $? -eq 0 ]; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Final instructions
echo ""
echo "✨ INSTALLATION COMPLETE! ✨"
echo ""
echo "🚀 To start the web dashboard:"
echo ""
echo "   Option 1 (Recommended):"
echo "   python launch_ultron_web.py"
echo ""
echo "   Option 2 (Direct):"
echo "   python ultron_web_server.py"
echo ""
echo "   Option 3 (Windows):"
echo "   Double-click launch_web_dashboard.bat"
echo ""
echo "   Option 4 (Linux/Mac):"
echo "   ./launch_web_dashboard.sh"
echo ""
echo "📊 Once started, access the dashboard at:"
echo "   http://localhost:8000"
echo ""
echo "🔧 Features available:"
echo "   • Multi-Provider AI Chat (OpenAI, Anthropic, NVIDIA, Ollama)"
echo "   • Real-time System Monitoring"
echo "   • Voice Controls Integration"
echo "   • Automation Tools (Screenshot, OCR, etc.)"
echo "   • Activity Logging"
echo "   • WebSocket Real-time Updates"
echo ""
echo "⚡ ULTRON Agent Web Dashboard is ready to use! ⚡"
echo ""