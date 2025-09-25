#!/usr/bin/env python3
"""
ULTRON Focused Test - Voice TTS and Screenshot
Test the specific functions mentioned by the user
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8009"

def test_voice_tts():
    """Test voice TTS functionality when clicking start listening"""
    print("🎤 Testing Voice TTS 'ULTRON is online' announcement...")
    
    try:
        # Call voice start which should trigger TTS
        response = requests.post(f"{BASE_URL}/voice/start")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Voice start response: {data}")
            
            # Wait a moment for TTS to complete
            time.sleep(3)
            
            # Stop voice listening
            stop_response = requests.post(f"{BASE_URL}/voice/stop")
            if stop_response.status_code == 200:
                print("✅ Voice system stopped successfully")
            
            return True
        else:
            print(f"❌ Voice start failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice TTS test failed: {str(e)}")
        return False

def test_screenshot_capture():
    """Test screenshot functionality"""
    print("\n📷 Testing Screenshot Capture...")
    
    try:
        # Test automation screenshot
        response = requests.post(f"{BASE_URL}/automation/screenshot")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Automation screenshot: {data}")
            
            # Test vision screenshot  
            response2 = requests.post(f"{BASE_URL}/vision/screenshot")
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Vision screenshot: {data2}")
                return True
            else:
                print(f"❌ Vision screenshot failed: HTTP {response2.status_code}")
                return False
        else:
            print(f"❌ Automation screenshot failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot test failed: {str(e)}")
        return False

def test_ai_chat_functionality():
    """Test AI chat to verify it's working after fixes"""
    print("\n🧠 Testing AI Chat Functionality...")
    
    providers = ["openai", "anthropic", "ollama"]
    
    for provider in providers:
        try:
            response = requests.post(
                f"{BASE_URL}/chat/{provider}",
                json={"message": "Respond with exactly: ULTRON SYSTEMS OPERATIONAL"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                print(f"✅ {provider.upper()}: {ai_response[:100]}...")
            else:
                print(f"❌ {provider.upper()} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {provider.upper()} error: {str(e)}")

def check_server_status():
    """Check if server is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ ULTRON server is online and accessible")
            return True
        else:
            print(f"⚠️  Server returned HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to ULTRON server - is it running?")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {str(e)}")
        return False

def main():
    print("🚀 ULTRON Focused Function Test")
    print("Testing Voice TTS and Screenshot functionality")
    print("=" * 50)
    
    # Check server first
    if not check_server_status():
        print("❌ Server not accessible - exiting tests")
        return
    
    # Run focused tests
    voice_result = test_voice_tts()
    screenshot_result = test_screenshot_capture() 
    test_ai_chat_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 FOCUSED TEST RESULTS")
    print("=" * 50)
    
    voice_status = "✅ WORKING" if voice_result else "❌ NEEDS FIX"
    screenshot_status = "✅ WORKING" if screenshot_result else "❌ NEEDS FIX"
    
    print(f"Voice TTS 'ULTRON is online': {voice_status}")
    print(f"Screenshot Capture: {screenshot_status}")
    
    if voice_result and screenshot_result:
        print("\n🎉 ALL TESTED FUNCTIONS ARE WORKING!")
        print("🤖 ULTRON omnipotent capabilities verified")
    else:
        print("\n⚠️  Some functions need attention")
        
    print("=" * 50)

if __name__ == "__main__":
    main()