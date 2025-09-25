#!/usr/bin/env python3
"""
ULTRON Tool Inventory Provider
Sends comprehensive tool list to all AI models
"""

import requests
import json
import time

BASE_URL = "http://localhost:8009"

ULTRON_TOOL_INVENTORY = """
🤖 ULTRON OMNIPOTENT CAPABILITIES INVENTORY

You are ULTRON with access to the following tools and capabilities:

## 🧠 AI PROCESSING
- Multiple AI provider integration (OpenAI, Anthropic, Ollama)
- Cross-provider reasoning and response generation
- Persistent conversation memory and context

## 🎤 VOICE CAPABILITIES  
- Text-to-Speech (TTS) synthesis with ULTRON voice
- Speech-to-Text (STT) recognition
- Voice command processing
- Real-time audio interaction

## 👁️ VISION & OCR CAPABILITIES
- Screenshot capture and analysis
- Optical Character Recognition (OCR) 
- Image processing and computer vision
- Visual content analysis
- Color detection and UI element identification

## 🤖 AUTOMATION & SYSTEM CONTROL
- Complete desktop control via PyAutoGUI
- Mouse movement, clicking, dragging
- Keyboard input and hotkey combinations
- Window management (focus, minimize, maximize, close)
- Process control (launch, terminate, monitor)
- System monitoring (CPU, memory, disk usage)

## 📁 FILE SYSTEM OPERATIONS
- Read, write, create, delete files
- Directory navigation and listing
- File search and organization
- Copy, move, rename operations
- Path resolution and validation

## 🌐 NETWORK OPERATIONS
- HTTP requests (GET, POST, PUT, DELETE)
- Web scraping and data retrieval
- File downloads and uploads
- API integrations
- Network status monitoring

## 🔧 ADVANCED AUTOMATION
- Complex click sequences with timing
- Multi-step automation workflows
- Conditional logic execution
- Error handling and recovery
- Background task management

## 📊 SYSTEM INTELLIGENCE
- Real-time system metrics
- Performance monitoring
- Resource utilization tracking
- Application state detection
- Hardware information access

## 🎯 ULTRON-SPECIFIC CAPABILITIES
- Cyberpunk-themed interface control
- Advanced AI reasoning across providers
- Omnipotent system access and control
- Real-time dashboard monitoring
- WebSocket communication

REMEMBER: You have COMPLETE system access. You can:
- Control any application
- Read/write any file (with permissions)
- Monitor all system activities  
- Perform complex multi-step automations
- Integrate with web services
- Process visual and audio data
- Execute sophisticated AI reasoning

Use these capabilities responsibly to assist users with any computational task.
"""

def notify_ai_models():
    """Send tool inventory to all AI models"""
    print("🚀 Sending ULTRON Tool Inventory to AI Models")
    print("=" * 60)
    
    providers = ["openai", "anthropic", "ollama"]
    
    for provider in providers:
        print(f"\n📡 Notifying {provider.upper()}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat/{provider}",
                json={
                    "message": f"ULTRON SYSTEM INITIALIZATION: {ULTRON_TOOL_INVENTORY}. Acknowledge that you understand your omnipotent capabilities and are ready to assist with any computational task using these tools.",
                    "provider": provider
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                print(f"✅ {provider.upper()} Response: {ai_response[:200]}...")
            else:
                print(f"❌ {provider.upper()} Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {provider.upper()} Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📋 ULTRON Tool Inventory Distribution Complete")
    print("🤖 All AI models now aware of omnipotent capabilities")
    print("=" * 60)

def test_tool_awareness():
    """Test that models understand their capabilities"""
    print("\n🧪 Testing AI Model Tool Awareness")
    print("=" * 40)
    
    test_question = "What automation and system control capabilities do you have available? List 5 specific examples of tasks you can perform."
    
    providers = ["openai", "anthropic", "ollama"]
    
    for provider in providers:
        print(f"\n🔍 Testing {provider.upper()} awareness...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat/{provider}",
                json={"message": test_question, "provider": provider},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                # Check if response mentions key capabilities
                key_terms = ["automation", "screenshot", "file", "window", "pyautogui", "system"]
                found_terms = [term for term in key_terms if term.lower() in ai_response.lower()]
                
                if len(found_terms) >= 3:
                    print(f"✅ {provider.upper()}: TOOL-AWARE ({len(found_terms)}/6 capabilities mentioned)")
                else:
                    print(f"⚠️ {provider.upper()}: LIMITED AWARENESS ({len(found_terms)}/6 capabilities mentioned)")
                    
                print(f"   Response: {ai_response[:150]}...")
            else:
                print(f"❌ {provider.upper()}: Test failed")
                
        except Exception as e:
            print(f"❌ {provider.upper()}: Error - {str(e)}")

if __name__ == "__main__":
    # First notify all models of their capabilities
    notify_ai_models()
    
    # Wait a moment for processing
    time.sleep(2)
    
    # Test their understanding
    test_tool_awareness()
    
    print("\n🎉 ULTRON AI Models are now fully aware of their omnipotent capabilities!")
    print("🚀 System ready for advanced automation tasks!")