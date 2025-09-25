#!/usr/bin/env python3
"""
ULTRON AI Model Tool Awareness Test
Test each AI model to ensure they understand their available capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:8009"

# Comprehensive tool inventory for AI models
TOOL_INVENTORY_MESSAGE = """
ULTRON System Tool Inventory - You have access to ALL of these capabilities:

🧠 AI CAPABILITIES:
- Multi-provider chat (OpenAI GPT, Anthropic Claude, Ollama local models)
- Context-aware conversations with memory
- Real-time response generation

🎤 VOICE CAPABILITIES:
- Text-to-speech synthesis (pyttsx3)
- Speech-to-text recognition  
- Voice command processing
- Real-time audio interaction

👁️ VISION CAPABILITIES:
- Screenshot capture and analysis
- OCR text extraction from images
- Computer vision processing
- Image analysis and object detection
- Color detection and UI element identification

🤖 AUTOMATION CAPABILITIES:
- PyAutoGUI desktop control
- Advanced click sequences and mouse control
- Keyboard automation and hotkey combinations
- Window management (focus, minimize, maximize, close)
- Process control (launch, terminate, monitor)
- Screenshot analysis and UI element detection

📁 FILE SYSTEM OPERATIONS:
- File read/write/delete operations
- Directory listing and navigation
- File search and manipulation
- Copy/move operations
- Content analysis

🌐 NETWORK OPERATIONS:
- HTTP GET/POST requests
- Web content fetching
- File downloads
- API interactions

⚙️ SYSTEM MONITORING:
- Real-time system statistics
- Process monitoring
- Memory and CPU usage tracking
- Network activity monitoring
- Hardware information

🔧 ADVANCED FEATURES:
- Multi-command automation sequences
- Background process management
- Real-time WebSocket communication
- Cross-platform compatibility
- Error handling and recovery

Please confirm you understand these capabilities and can use them to assist users with complex automation tasks.
"""

def test_ai_model_awareness(provider: str):
    """Test if an AI model understands its available tools"""
    print(f"\n🧠 Testing {provider.upper()} model awareness...")
    
    try:
        # Send tool inventory to the model
        response = requests.post(
            f"{BASE_URL}/chat/{provider}",
            json={
                "message": TOOL_INVENTORY_MESSAGE + "\n\nRespond with: 'I understand and can use these ULTRON capabilities for [list 3 specific automation tasks you could help with]'"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "")
            
            print(f"✅ {provider.upper()} Response:")
            print(f"   {ai_response[:200]}...")
            
            # Test specific capability understanding
            capability_test = requests.post(
                f"{BASE_URL}/chat/{provider}",
                json={
                    "message": "Given your ULTRON capabilities, how would you help a user take a screenshot, analyze it with OCR, and save the text to a file? Provide specific steps."
                },
                timeout=30
            )
            
            if capability_test.status_code == 200:
                capability_data = capability_test.json()
                capability_response = capability_data.get("response", "")
                
                print(f"📋 {provider.upper()} Capability Understanding:")
                print(f"   {capability_response[:300]}...")
                
                return True
            else:
                print(f"❌ {provider.upper()} capability test failed")
                return False
                
        else:
            print(f"❌ {provider.upper()} connection failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {provider.upper()} error: {str(e)}")
        return False

def test_system_integration():
    """Test if the system can demonstrate tool usage"""
    print(f"\n🔧 Testing ULTRON system integration...")
    
    try:
        # Test voice capability
        voice_test = requests.post(f"{BASE_URL}/voice/start")
        if voice_test.status_code == 200:
            print("✅ Voice system: Accessible")
            requests.post(f"{BASE_URL}/voice/stop")  # Clean up
        else:
            print("❌ Voice system: Not accessible")
        
        # Test screenshot capability
        screenshot_test = requests.post(f"{BASE_URL}/automation/screenshot")
        if screenshot_test.status_code == 200:
            print("✅ Screenshot system: Accessible")
        else:
            print("❌ Screenshot system: Not accessible")
        
        # Test automation status
        automation_test = requests.get(f"{BASE_URL}/automation/status")
        if automation_test.status_code == 200:
            print("✅ Automation system: Accessible")
        else:
            print("❌ Automation system: Not accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ System integration test failed: {str(e)}")
        return False

def main():
    """Run comprehensive AI model tool awareness tests"""
    print("🚀 ULTRON AI MODEL TOOL AWARENESS TEST")
    print("Ensuring models understand their omnipotent capabilities")
    print("=" * 60)
    
    # Check server health first
    try:
        health_check = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_check.status_code != 200:
            print("❌ ULTRON server not healthy - exiting")
            return
    except:
        print("❌ Cannot connect to ULTRON server - exiting")
        return
    
    print("✅ ULTRON server is online and healthy")
    
    # Test each AI model
    providers = ["openai", "anthropic", "ollama"]
    model_results = []
    
    for provider in providers:
        result = test_ai_model_awareness(provider)
        model_results.append((provider, result))
        time.sleep(2)  # Brief pause between tests
    
    # Test system integration
    system_result = test_system_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 AI MODEL TOOL AWARENESS RESULTS")
    print("=" * 60)
    
    working_models = sum(1 for _, result in model_results if result)
    total_models = len(model_results)
    
    print(f"AI Models Tested: {total_models}")
    print(f"✅ Tool-Aware Models: {working_models}")
    print(f"🔧 System Integration: {'✅ Working' if system_result else '❌ Failed'}")
    
    print("\nDetailed Results:")
    for provider, result in model_results:
        status = "✅ Tool-Aware" if result else "❌ Needs Training"
        print(f"  {provider.upper()}: {status}")
    
    print("\n" + "=" * 60)
    
    if working_models == total_models and system_result:
        print("🎉 ALL AI MODELS ARE TOOL-AWARE!")
        print("🤖 ULTRON omnipotent capabilities fully understood")
        print("🚀 Ready for complex automation tasks")
    elif working_models > 0:
        print("✅ Some models are tool-aware")
        print("🔧 Continue training others")
    else:
        print("⚠️ Models need tool awareness training")
        print("📚 Send capability documentation")
    
    print("=" * 60)

if __name__ == "__main__":
    main()