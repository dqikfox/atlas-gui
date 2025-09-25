#!/usr/bin/env python3
"""
ULTRON Agent Real PC Stats - Quick Launcher
This script starts the system monitor and opens the dashboard
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import psutil
        import fastapi
        import uvicorn
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Installing required packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "fastapi", "uvicorn", "websockets"])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies automatically")
            print("\n🔧 Please install manually:")
            print("   pip install psutil fastapi uvicorn websockets")
            return False

def start_system_monitor():
    """Start the system monitor backend"""
    script_path = Path(__file__).parent / "real-system-monitor.py"
    
    if not script_path.exists():
        print(f"❌ System monitor script not found: {script_path}")
        return None
    
    print("🚀 Starting ULTRON System Monitor...")
    
    try:
        # Start the backend server
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ System monitor started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ System monitor failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting system monitor: {e}")
        return None

def open_dashboard():
    """Open the dashboard in the default browser"""
    dashboard_url = "http://localhost:8001/"
    
    print(f"🌐 Opening dashboard: {dashboard_url}")
    
    try:
        webbrowser.open(dashboard_url)
        print("✅ Dashboard opened in browser!")
    except Exception as e:
        print(f"❌ Could not open browser automatically: {e}")
        print(f"📱 Please manually open: {dashboard_url}")

def main():
    print("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
    print("  ULTRON AGENT - REAL PC STATS LAUNCHER  ")
    print("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
    print("")
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    print("")
    
    # Start system monitor
    monitor_process = start_system_monitor()
    if not monitor_process:
        input("\nPress Enter to exit...")
        return
    
    # Wait a bit more for server to be fully ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Open dashboard
    open_dashboard()
    
    print("")
    print("🎯 SUCCESS! Your ULTRON Real PC Stats Dashboard is now running!")
    print("")
    print("📊 Dashboard URL: http://localhost:8001/")
    print("🔌 WebSocket URL: ws://localhost:8001/ws")
    print("📡 API Endpoints: http://localhost:8001/api/metrics")
    print("")
    print("🖥️  Now showing YOUR ACTUAL PC stats:")
    print("   • Real CPU usage and temperature")
    print("   • Actual memory consumption")
    print("   • Live disk usage")
    print("   • Network statistics")
    print("   • System uptime and processes")
    print("")
    print("⚡ Press Ctrl+C to stop the server")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        # Keep the launcher running and monitor the backend
        while True:
            if monitor_process.poll() is not None:
                print("\n❌ System monitor stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down ULTRON System Monitor...")
        monitor_process.terminate()
        
        # Wait for graceful shutdown
        try:
            monitor_process.wait(timeout=5)
            print("✅ System monitor stopped gracefully")
        except subprocess.TimeoutExpired:
            print("⚠️ Force stopping system monitor...")
            monitor_process.kill()
            
        print("👋 ULTRON Agent system monitor has been stopped.")

if __name__ == "__main__":
    main()