#!/usr/bin/env python3
"""
ULTRON Agent System Monitor - Real PC Stats
Reads actual system metrics using psutil and serves them via FastAPI
"""

import psutil
import platform
import time
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import asyncio
from typing import List
import threading
import queue

app = FastAPI(title="ULTRON Agent System Monitor", version="1.0.0")

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected WebSocket clients
connected_clients: List[WebSocket] = []

# Activity log storage
activity_log = queue.Queue(maxsize=100)
start_time = datetime.now()

def get_system_metrics():
    """Get real system metrics from the PC"""
    try:
        # CPU usage (average over 1 second)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        
        # Disk usage (main drive)
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        
        # Network stats
        network = psutil.net_io_counters()
        
        # Boot time and uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        # Process count
        process_count = len(psutil.pids())
        
        # CPU frequency
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_freq_current = cpu_freq.current if cpu_freq else 0
        except:
            cpu_freq_current = 0
            
        # Temperature (if available)
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try to get CPU temperature
                for name, entries in temps.items():
                    if 'cpu' in name.lower() or 'core' in name.lower():
                        temp = entries[0].current if entries else None
                        break
        except:
            pass
            
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": round(cpu_percent, 1),
                "frequency_mhz": round(cpu_freq_current, 0) if cpu_freq_current else None,
                "core_count": psutil.cpu_count(),
                "temperature_c": round(temp, 1) if temp else None
            },
            "memory": {
                "usage_percent": round(memory_percent, 1),
                "used_gb": round(memory_used_gb, 2),
                "total_gb": round(memory_total_gb, 2),
                "available_gb": round(memory.available / (1024**3), 2)
            },
            "disk": {
                "usage_percent": round(disk_percent, 1),
                "used_gb": round(disk_used_gb, 2),
                "total_gb": round(disk_total_gb, 2),
                "free_gb": round(disk.free / (1024**3), 2)
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            "system": {
                "uptime_seconds": int(uptime.total_seconds()),
                "uptime_formatted": format_uptime(uptime),
                "boot_time": boot_time.isoformat(),
                "process_count": process_count,
                "platform": platform.system(),
                "platform_version": platform.version(),
                "hostname": platform.node()
            }
        }
    except Exception as e:
        print(f"Error getting system metrics: {e}")
        return None

def format_uptime(uptime_delta):
    """Format uptime as human readable string"""
    days = uptime_delta.days
    hours, remainder = divmod(uptime_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def add_activity_log(message, log_type="info"):
    """Add entry to activity log"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "type": log_type
    }
    
    try:
        activity_log.put_nowait(log_entry)
    except queue.Full:
        # Remove oldest entry if queue is full
        try:
            activity_log.get_nowait()
            activity_log.put_nowait(log_entry)
        except queue.Empty:
            pass

def get_activity_logs():
    """Get all activity logs as list"""
    logs = []
    temp_logs = []
    
    # Get all logs from queue
    while not activity_log.empty():
        try:
            log = activity_log.get_nowait()
            logs.append(log)
            temp_logs.append(log)
        except queue.Empty:
            break
    
    # Put logs back in queue
    for log in temp_logs:
        try:
            activity_log.put_nowait(log)
        except queue.Full:
            break
            
    return logs

# API Endpoints
@app.get("/api/metrics")
async def get_metrics():
    """Get current system metrics"""
    metrics = get_system_metrics()
    if metrics:
        return metrics
    else:
        return {"error": "Unable to retrieve system metrics"}

@app.get("/api/logs")
async def get_logs():
    """Get activity logs"""
    return get_activity_logs()

@app.post("/api/logs")
async def add_log(log_data: dict):
    """Add new activity log entry"""
    message = log_data.get("message", "User action")
    log_type = log_data.get("type", "info")
    add_activity_log(message, log_type)
    return {"status": "success"}

@app.post("/api/chat")
async def chat_endpoint(chat_data: dict):
    """Handle chat messages"""
    message = chat_data.get("message", "")
    
    # Log the chat interaction
    add_activity_log(f"💬 User message: {message[:50]}{'...' if len(message) > 50 else ''}")
    
    # Simple AI responses
    responses = [
        f"System status: CPU at {get_system_metrics()['cpu']['usage_percent']}%, Memory at {get_system_metrics()['memory']['usage_percent']}%. All systems operational.",
        "I'm monitoring your system in real-time. Current performance metrics look good.",
        f"Your system has been running for {get_system_metrics()['system']['uptime_formatted']}. No critical issues detected.",
        "Real-time monitoring active. All subsystems are functioning within normal parameters.",
        f"Current system load: {psutil.cpu_count()} CPU cores, {round(psutil.virtual_memory().total / (1024**3), 1)}GB RAM total.",
        "System analysis complete. Performance metrics are within acceptable ranges."
    ]
    
    import random
    response = random.choice(responses)
    
    add_activity_log(f"🤖 AI response: {response[:50]}{'...' if len(response) > 50 else ''}")
    
    return {
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    add_activity_log("🔌 New WebSocket client connected")
    
    try:
        while True:
            # Send system metrics every 3 seconds
            metrics = get_system_metrics()
            if metrics:
                await websocket.send_json({
                    "type": "metrics",
                    "data": metrics
                })
            
            # Send activity logs
            logs = get_activity_logs()
            if logs:
                await websocket.send_json({
                    "type": "logs", 
                    "data": logs
                })
            
            await asyncio.sleep(3)
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        add_activity_log("🔌 WebSocket client disconnected")

# Serve the dashboard
@app.get("/")
async def serve_dashboard():
    """Serve the main dashboard"""
    return FileResponse("/workspace/real-dashboard.html")

# Background task to generate system activity logs
def background_monitor():
    """Background monitoring and logging"""
    while True:
        try:
            metrics = get_system_metrics()
            if metrics:
                cpu = metrics["cpu"]["usage_percent"]
                memory = metrics["memory"]["usage_percent"]
                
                # Log high usage warnings
                if cpu > 80:
                    add_activity_log(f"⚠️ High CPU usage detected: {cpu}%", "warning")
                if memory > 85:
                    add_activity_log(f"⚠️ High memory usage detected: {memory}%", "warning")
                    
                # Periodic system updates
                if int(time.time()) % 60 == 0:  # Every minute
                    add_activity_log(f"📊 System check: CPU {cpu}%, RAM {memory}%")
                    
        except Exception as e:
            print(f"Background monitor error: {e}")
            
        time.sleep(10)

# Initialize
@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    add_activity_log("🚀 ULTRON Agent System Monitor started")
    add_activity_log(f"💻 Monitoring system: {platform.node()}")
    add_activity_log(f"🖥️ Platform: {platform.system()} {platform.release()}")
    add_activity_log("📊 Real-time system monitoring activated")
    
    # Start background monitoring thread
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()

if __name__ == "__main__":
    print("🚀 Starting ULTRON Agent System Monitor...")
    print("📊 Real-time PC stats monitoring")
    print("🌐 Dashboard will be available at: http://localhost:8001")
    print("🔌 WebSocket endpoint: ws://localhost:8001/ws")
    print("📡 API endpoints: http://localhost:8001/api/metrics")
    print("⚡ Press Ctrl+C to stop")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info"
    )