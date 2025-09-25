#!/usr/bin/env python3
"""
ULTRON Agent Web Dashboard Server
Integrates the web UI with the existing ULTRON Agent backend
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add the existing ULTRON agent paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "src"))

try:
    # Import ULTRON omnipotent components
    from agent_core import UltronAgent
    from ai_config import AIConfig
    from voice_manager import VoiceManager
    from vision import VisionManager as UltronVision
    from ultron_automation import UltronAutomationManager
    print("ULTRON omnipotent components loaded successfully - ultron_web_server.py:33")
except ImportError as e:
    print(f"Warning: Could not import ULTRON components: {e} - ultron_web_server.py:35")
    print("Running in standalone mode... - ultron_web_server.py:36")
    UltronAgent = None
    AIConfig = None
    VoiceManager = None
    UltronVision = None
    UltronAutomationManager = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    provider: str = "openai"
    include_voice: bool = False

class AutomationRequest(BaseModel):
    action: str
    parameters: Optional[Dict] = None

class VoiceRequest(BaseModel):
    action: str  # "start" or "stop"

# FastAPI app
app = FastAPI(
    title="ULTRON Agent Web Dashboard",
    description="Web interface for the ULTRON Agent AI Assistant",
    version="2.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

# Global ULTRON omnipotent components
ultron_agent = None
voice_manager = None
vision_manager = None
automation_manager = None

# Initialize ULTRON omnipotent systems
async def initialize_ultron():
    global ultron_agent, voice_manager, vision_manager, automation_manager
    
    try:
        if UltronAgent:
            ultron_agent = UltronAgent()
            ultron_agent.initialize()
            print("ULTRON Agent initialized with omnipotent AI capabilities - ultron_web_server.py:110")
        
        if VoiceManager:
            voice_manager = VoiceManager()
            print("ULTRON Voice Manager initialized with omnipotent speech capabilities - ultron_web_server.py:114")
        
        if UltronVision:
            vision_manager = UltronVision()
            print("ULTRON Vision System initialized with omnipotent visual processing - ultron_web_server.py:118")
            
        if UltronAutomationManager:
            automation_manager = UltronAutomationManager()
            print("ULTRON Automation Manager initialized with omnipotent system control - ultron_web_server.py:122")
            
    except Exception as e:
        print(f"⚠️  Warning: Failed to initialize ULTRON omnipotent components: {e} - ultron_web_server.py:125")
        print("Running in limited mode... - ultron_web_server.py:126")

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    try:
        with open("ultron-web-dashboard.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Dashboard not found</h1><p>Please ensure ultron-web-dashboard.html is in the same directory.</p>",
            status_code=404
        )

@app.get("/ultron-dashboard.js")
async def dashboard_js():
    """Serve the dashboard JavaScript"""
    return FileResponse("ultron-dashboard.js", media_type="application/javascript")

@app.get("/status")
async def get_status():
    """Get system status"""
    return {
        "status": "online",
        "version": "2.1.0",
        "ultron_available": ultron_agent is not None,
        "voice_available": voice_manager is not None,
        "vision_available": vision_manager is not None,
        "timestamp": time.time()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ultron_mode": ULTRON_MODE,
        "components": {
            "ai_agent": ultron_agent is not None,
            "voice_manager": voice_manager is not None,
            "vision_manager": vision_manager is not None,
            "automation_manager": UltronAutomationManager is not None
        },
        "timestamp": time.time()
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat messages"""
    try:
        if ultron_agent:
            # Use real ULTRON agent
            ai_result = await ultron_agent.process_message(
                message=request.message,
                provider=request.provider,
                include_voice=request.include_voice
            )
            
            # Extract the response text from the AI result
            if isinstance(ai_result, dict):
                if "error" in ai_result and ai_result["error"]:
                    # If there's an error, fall back to demo mode
                    response = f"[AI ERROR - DEMO MODE] ULTRON received: '{request.message}' via {request.provider}"
                    actual_provider = f"{request.provider} (demo)"
                else:
                    response = ai_result.get("response", str(ai_result))
                    actual_provider = ai_result.get("provider", request.provider)
            else:
                response = str(ai_result)
                actual_provider = request.provider
        else:
            # Demo mode response
            response = f"[DEMO MODE] ULTRON received: '{request.message}' via {request.provider}"
            actual_provider = request.provider
        
        # Ensure response is always a string
        if not isinstance(response, str):
            response = str(response)
        
        # Broadcast to WebSocket clients
        await manager.broadcast({
            "type": "ai_response",
            "response": response,
            "provider": actual_provider
        })
        
        return {"response": response, "provider": actual_provider}
        
    except Exception as e:
        error_msg = f"[ERROR] Failed to process message: {str(e)}"
        return {"response": error_msg, "provider": request.provider}

@app.post("/chat/openai")
async def chat_openai(request: dict):
    """OpenAI specific chat endpoint"""
    try:
        if ultron_agent:
            result = await ultron_agent.process_message(
                message=request["message"],
                provider="openai"
            )
            return result
        else:
            return {"response": "[DEMO MODE] OpenAI would respond here", "provider": "openai"}
    except Exception as e:
        return {"error": str(e), "provider": "openai"}

@app.post("/chat/anthropic") 
async def chat_anthropic(request: dict):
    """Anthropic specific chat endpoint"""
    try:
        if ultron_agent:
            result = await ultron_agent.process_message(
                message=request["message"],
                provider="anthropic"
            )
            return result
        else:
            return {"response": "[DEMO MODE] Anthropic Claude would respond here", "provider": "anthropic"}
    except Exception as e:
        return {"error": str(e), "provider": "anthropic"}

@app.post("/chat/ollama")
async def chat_ollama(request: dict):
    """Ollama specific chat endpoint"""
    try:
        if ultron_agent:
            result = await ultron_agent.process_message(
                message=request["message"],
                provider="ollama"
            )
            return result
        else:
            return {"response": "[DEMO MODE] Ollama would respond here", "provider": "ollama"}
    except Exception as e:
        return {"error": str(e), "provider": "ollama"}

@app.post("/voice/start")
async def start_voice_listening():
    """Start voice listening with ULTRON TTS announcement"""
    try:
        if voice_manager:
            # First announce ULTRON is online via TTS
            await voice_manager.speak_text("ULTRON is online")
            
            # Then start listening
            await voice_manager.start_listening()
            message = "ULTRON voice system activated"
        else:
            message = "[DEMO MODE] Voice listening started"
        
        await manager.broadcast({
            "type": "voice_status",
            "status": {"listening": True, "message": message}
        })
        
        return {"status": "success", "message": message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/stop")
async def stop_voice_listening():
    """Stop voice listening"""
    try:
        if voice_manager:
            await voice_manager.stop_listening()
            message = "Voice listening stopped"
        else:
            message = "[DEMO MODE] Voice listening stopped"
        
        await manager.broadcast({
            "type": "voice_status",
            "status": {"listening": False, "message": message}
        })
        
        return {"status": "success", "message": message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/synthesize")
async def synthesize_voice(request: dict):
    """Text-to-speech synthesis"""
    try:
        text = request.get("text", "")
        if voice_manager:
            result = await voice_manager.speak_text(text)
            return {"status": "success", "message": f"Synthesized: {text[:50]}..."}
        else:
            return {"status": "success", "message": f"[DEMO MODE] Would synthesize: {text[:50]}..."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/voice/status")
async def get_voice_status():
    """Get voice system status"""
    try:
        if voice_manager:
            status = voice_manager.get_status() if hasattr(voice_manager, 'get_status') else {"status": "Voice system ready"}
        else:
            status = {"status": "[DEMO MODE] Voice system would be ready"}
        return status
    except Exception as e:
        return {"error": str(e)}

@app.post("/vision/screenshot")
async def vision_screenshot(request: dict = None):
    """Take and analyze screenshot"""
    try:
        if vision_manager:
            result = vision_manager.take_screenshot()
            if result.get("status") == "success":
                filename = f"screenshots/ultron_vision_{int(time.time())}.png"
                # Decode base64 image and save
                import base64
                image_data = base64.b64decode(result["image_data"])
                with open(filename, 'wb') as f:
                    f.write(image_data)
                return {"status": "success", "screenshot_path": filename, "analysis": f"Screenshot captured: {result.get('size', 'unknown size')}"}
            else:
                return {"error": result.get("message", "Screenshot failed")}
        else:
            filename = f"demo_vision_{int(time.time())}.png"
            return {"status": "success", "screenshot_path": filename, "analysis": "[DEMO MODE] Screenshot would be captured"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/vision/status")
async def get_vision_status():
    """Get vision system status"""
    try:
        if vision_manager:
            status = vision_manager.get_status() if hasattr(vision_manager, 'get_status') else {"status": "Vision system ready"}
        else:
            status = {"status": "[DEMO MODE] Vision system would be ready"}
        return status
    except Exception as e:
        return {"error": str(e)}

# ULTRON OMNIPOTENT AUTOMATION ENDPOINTS

@app.post("/automation/screenshot")
async def take_screenshot():
    """Take screenshot with ULTRON precision"""
    try:
        if vision_manager:
            result = vision_manager.take_screenshot()
            if result.get("status") == "success":
                filename = f"screenshots/ultron_capture_{int(time.time())}.png"
                # Decode base64 image and save
                import base64
                from PIL import Image
                image_data = base64.b64decode(result["image_data"])
                with open(filename, 'wb') as f:
                    f.write(image_data)
                message = f"ULTRON screenshot captured: {filename}"
            else:
                message = f"Screenshot failed: {result.get('message', 'Unknown error')}"
        else:
            filename = f"demo_screenshot_{int(time.time())}.png"
            message = f"[DEMO MODE] Screenshot would be saved as: {filename}"
        
        await manager.broadcast({
            "type": "automation_result",
            "message": message
        })
        
        return {"status": "success", "filename": filename if vision_manager and "error" not in result else filename}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/ocr")
async def perform_ocr():
    """Perform omnipotent OCR analysis"""
    try:
        if vision_manager:
            capture_result = await vision_manager.capture_screen()
            if "error" not in capture_result:
                ocr_result = await vision_manager.enhanced_ocr(capture_result["image"])
                if "error" not in ocr_result:
                    tesseract_data = ocr_result["ocr_results"].get("tesseract", {})
                    text = tesseract_data.get("full_text", "")
                    message = f"ULTRON OCR completed: {len(text)} characters extracted"
                else:
                    text = ""
                    message = f"OCR failed: {ocr_result['error']}"
            else:
                text = ""
                message = f"Screen capture failed: {capture_result['error']}"
        else:
            text = "[DEMO MODE] This would be the extracted text from ULTRON OCR"
            message = f"[DEMO MODE] ULTRON OCR completed, extracted {len(text)} characters"
        
        await manager.broadcast({
            "type": "automation_result", 
            "message": message
        })
        
        return {"status": "success", "text": text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/pyautogui")
async def pyautogui_action(request: AutomationRequest):
    """Execute PyAutoGUI actions with ULTRON omnipotence"""
    try:
        if automation_manager:
            result = await automation_manager.execute_pyautogui_action(
                request.action, 
                request.parameters or {}
            )
        else:
            result = {
                "status": "success",
                "message": f"[DEMO MODE] Would execute PyAutoGUI action: {request.action}",
                "action": request.action,
                "parameters": request.parameters
            }
        
        await manager.broadcast({
            "type": "automation_result",
            "message": result.get("message", f"PyAutoGUI action completed: {request.action}")
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/system_control")
async def system_control(request: AutomationRequest):
    """Execute system control commands with ULTRON authority"""
    try:
        if automation_manager:
            result = await automation_manager.execute_system_command(
                request.action,
                request.parameters or {}
            )
        else:
            result = {
                "status": "success", 
                "message": f"[DEMO MODE] Would execute system control: {request.action}",
                "action": request.action
            }
        
        await manager.broadcast({
            "type": "automation_result",
            "message": result.get("message", f"System control executed: {request.action}")
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/speak")
async def speak_text(request: VoiceRequest):
    """Speak text with ULTRON authority"""
    try:
        if voice_manager:
            result = await voice_manager.speak_text(request.text)
        else:
            result = {
                "status": "success",
                "message": f"[DEMO MODE] ULTRON would speak: {request.text[:50]}..."
            }
        
        await manager.broadcast({
            "type": "voice_status",
            "status": {"speaking": True, "message": result.get("message", "")}
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/continuous_listening")
async def start_continuous_listening():
    """Start continuous voice recognition with AI processing"""
    try:
        if voice_manager and ultron_agent:
            # Define AI callback for voice commands
            def ai_voice_callback(recognized_text):
                try:
                    # Process with ULTRON AI
                    ai_response = ultron_agent.process_message(recognized_text, "anthropic")
                    return ai_response
                except Exception as e:
                    return f"I encountered an error processing your voice command: {str(e)}"
            
            result = await voice_manager.voice_command_processing(
                enable_ai_response=True,
                ai_callback=ai_voice_callback
            )
        else:
            result = {
                "status": "success",
                "message": "[DEMO MODE] ULTRON continuous voice AI processing would be active"
            }
        
        await manager.broadcast({
            "type": "voice_status",
            "status": {"listening": True, "ai_processing": True, "message": result.get("message", "")}
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/automation/status")
async def get_automation_status():
    """Get comprehensive automation system status"""
    try:
        status = {
            "automation_available": automation_manager is not None,
            "voice_available": voice_manager is not None,
            "vision_available": vision_manager is not None,
            "ai_available": ultron_agent is not None
        }
        
        if automation_manager:
            status["automation_status"] = automation_manager.get_status()
        if voice_manager:
            status["voice_status"] = voice_manager.get_status()
        if vision_manager:
            status["vision_status"] = vision_manager.get_status()
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/system_info")
async def get_system_info():
    """Get system information"""
    try:
        if UltronAutomationManager:
            automation_mgr = UltronAutomationManager()
            result = automation_mgr.process_control("system_info")
            return result
        else:
            return {
                "success": True,
                "cpu_count": 8,
                "memory_total": 16000000000,
                "memory_available": 8000000000,
                "message": "[DEMO MODE] System info would be here"
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/automation/window_management") 
async def window_management_endpoint(request: dict):
    """Window management operations"""
    try:
        action = request.get("action", "list_all")
        if UltronAutomationManager:
            automation_mgr = UltronAutomationManager()
            result = automation_mgr.window_management(action)
            return result
        else:
            return {
                "success": True,
                "windows": [{"title": "Demo Window", "visible": True}],
                "count": 1,
                "message": f"[DEMO MODE] Window {action} would be performed"
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/automation/process_control")
async def process_control_endpoint(request: dict):
    """Process control operations"""
    try:
        action = request.get("action", "list_processes")
        if UltronAutomationManager:
            automation_mgr = UltronAutomationManager()
            result = automation_mgr.process_control(action)
            return result
        else:
            return {
                "success": True,
                "processes": [{"pid": 1234, "name": "demo_process", "cpu_percent": 5.0}],
                "total_count": 50,
                "message": f"[DEMO MODE] Process {action} would be performed"
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/automation/file_operations")
async def file_operations_endpoint(request: dict):
    """File system operations"""
    try:
        action = request.get("action")
        path = request.get("path")
        content = request.get("content")
        
        if UltronAutomationManager:
            automation_mgr = UltronAutomationManager()
            result = automation_mgr.file_system_operations(action, path, content=content)
            return result
        else:
            if action == "list_directory":
                return {
                    "success": True,
                    "items": [{"name": "demo_file.txt", "is_file": True, "size": 1024}],
                    "message": f"[DEMO MODE] Would list directory: {path}"
                }
            elif action == "write":
                return {
                    "success": True,
                    "bytes_written": len(content) if content else 0,
                    "message": f"[DEMO MODE] Would write to: {path}"
                }
            else:
                return {
                    "success": True,
                    "message": f"[DEMO MODE] Would perform {action} on: {path}"
                }
    except Exception as e:
        return {"error": str(e)}

@app.post("/automation/network_operations")
async def network_operations_endpoint(request: dict):
    """Network operations"""
    try:
        action = request.get("action")
        url = request.get("url")
        
        if UltronAutomationManager:
            automation_mgr = UltronAutomationManager()
            result = automation_mgr.network_operations(action, url)
            return result
        else:
            return {
                "success": True,
                "status_code": 200,
                "content": f"[DEMO MODE] Response from {url}",
                "message": f"[DEMO MODE] Would perform {action} request to: {url}"
            }
    except Exception as e:
        return {"error": str(e)}

@app.get("/models/ollama")
async def get_ollama_models():
    """Get available Ollama models"""
    try:
        # Try to connect to Ollama
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model["name"] for model in data.get("models", [])]
                    return {"status": "online", "models": models}
                else:
                    return {"status": "offline", "models": []}
    except Exception:
        return {"status": "offline", "models": []}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        # Send initial status
        await websocket.send_text(json.dumps({
            "type": "system_status",
            "status": "connected"
        }))
        
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# System monitoring task
async def system_monitoring_task():
    """Background task for system monitoring"""
    import psutil
    
    while True:
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = {
                "cpu": round(cpu_percent, 1),
                "memory": round(memory.percent, 1),
                "disk": round(disk.percent, 1)
            }
            
            # Broadcast to all connected clients
            await manager.broadcast({
                "type": "system_metrics",
                "metrics": metrics
            })
            
        except Exception as e:
            print(f"System monitoring error: {e} - ultron_web_server.py:741")
        
        await asyncio.sleep(5)  # Update every 5 seconds

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("Starting ULTRON Agent Web Dashboard... - ultron_web_server.py:748")
    
    # Initialize ULTRON components
    await initialize_ultron()
    
    # Start system monitoring
    asyncio.create_task(system_monitoring_task())
    
    print("Dashboard ready! - ultron_web_server.py:756")
    print("Access dashboard at: http://localhost:8009 - ultron_web_server.py:757")
    print("WebSocket endpoint: ws://localhost:8009/ws - ultron_web_server.py:758")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "ultron_web_server:app",
        host="0.0.0.0",
        port=8009,
        reload=True,
        log_level="info"
    )
