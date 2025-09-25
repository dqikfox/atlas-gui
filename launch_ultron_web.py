#!/usr/bin/env python3
"""
Quick launcher script for ULTRON Agent Web Dashboard
This script provides an easy way to start the web interface
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets', 
        'aiohttp',
        'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_files():
    """Check if required files exist"""
    required_files = [
        'ultron-web-dashboard.html',
        'ultron-dashboard.js',
        'ultron_web_server.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def start_server():
    """Start the ULTRON web server"""
    print("🚀 Starting ULTRON Agent Web Dashboard...")
    print("━" * 50)
    
    try:
        # Start the server
        process = subprocess.Popen([
            sys.executable, 'ultron_web_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
           universal_newlines=True, bufsize=1)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Server started successfully!")
            print("\n📊 Dashboard URL: http://localhost:8009")
            print("🔌 WebSocket URL: ws://localhost:8009/ws")
            print("\n🌐 Opening in browser...")
            
            # Open in browser
            webbrowser.open('http://localhost:8009')
            
            print("\n⚡ ULTRON Web Dashboard is now running!")
            print("   Press Ctrl+C to stop the server")
            print("━" * 50)
            
            # Keep the launcher running and show server output
            try:
                for line in process.stdout:
                    print(line.rstrip())
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped.")
        else:
            print("❌ Failed to start server. Check the output above for errors.")
            return False
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("")
    print("⚡" * 20)
    print("  ULTRON AGENT WEB DASHBOARD  ")
    print("⚡" * 20)
    print("")
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        return
    print("✅ All dependencies found.")
    
    # Check files
    print("\n📁 Checking required files...")
    if not check_files():
        print("\n❌ Please ensure all required files are in the current directory.")
        return
    print("✅ All required files found.")
    
    # Create directories
    print("\n📂 Creating directories...")
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    print("✅ Directories ready.")
    
    # Start server
    print("\n🚀 Starting web server...")
    start_server()

if __name__ == "__main__":
    main()