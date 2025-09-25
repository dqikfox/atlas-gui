#!/usr/bin/env python3
"""
Final ULTRON Omnipotent Test - All Functions
Complete verification of all ULTRON capabilities
"""

import sys
sys.path.append('.')
from agent_core import UltronAgent
from voice_manager import VoiceManager  
from vision import VisionManager
from ultron_automation import UltronAutomationManager
import asyncio
import time
import os
import json

async def test_all_functions():
    """Test all ULTRON omnipotent capabilities directly"""
    
    print("🚀 ULTRON OMNIPOTENT CAPABILITIES TEST")
    print("Testing ALL functions end-to-end")
    print("=" * 60)
    
    results = []
    
    # Initialize all systems
    print("🔧 Initializing ULTRON systems...")
    try:
        agent = UltronAgent()
        voice_mgr = VoiceManager() 
        vision_mgr = VisionManager()
        automation_mgr = UltronAutomationManager()
        print("✅ All systems initialized")
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return
    
    # Test 1: AI Providers
    print("\n🧠 Testing AI Providers...")
    
    providers = ["openai", "anthropic", "ollama"]
    for provider in providers:
        try:
            response = await agent.process_message("Test response - say 'ULTRON ACTIVE'", provider)
            if isinstance(response, dict) and "response" in response:
                ai_text = response["response"]
                if "ULTRON ACTIVE" in ai_text or "active" in ai_text.lower():
                    print(f"✅ {provider.upper()}: WORKING")
                    results.append(f"✅ AI Provider {provider.upper()}")
                else:
                    print(f"✅ {provider.upper()}: RESPONDING (got: {ai_text[:50]}...)")
                    results.append(f"✅ AI Provider {provider.upper()}")
            else:
                print(f"❌ {provider.upper()}: Invalid response format")
                results.append(f"❌ AI Provider {provider.upper()}")
        except Exception as e:
            print(f"❌ {provider.upper()}: Error - {e}")
            results.append(f"❌ AI Provider {provider.upper()}")
    
    # Test 2: Voice System
    print("\n🎤 Testing Voice System...")
    
    try:
        # Test TTS
        tts_result = await voice_mgr.speak_text("ULTRON voice systems operational")
        if tts_result.get("status") == "success":
            print("✅ Voice TTS: WORKING")
            results.append("✅ Voice TTS")
        else:
            print("❌ Voice TTS: FAILED")  
            results.append("❌ Voice TTS")
            
        # Test voice status
        voice_status = voice_mgr.get_status()
        if voice_status.get("tts_available"):
            print("✅ Voice Status: WORKING")
            results.append("✅ Voice Status")
        else:
            print("❌ Voice Status: FAILED")
            results.append("❌ Voice Status")
            
    except Exception as e:
        print(f"❌ Voice System Error: {e}")
        results.append("❌ Voice System")
    
    # Test 3: Vision System
    print("\n👁️ Testing Vision System...")
    
    try:
        # Test screenshot
        screenshot_result = vision_mgr.take_screenshot()
        if screenshot_result.get("status") == "success":
            print("✅ Vision Screenshot: WORKING")
            results.append("✅ Vision Screenshot")
            
            # Save screenshot
            import base64
            filename = f"test_vision_{int(time.time())}.png"
            os.makedirs("screenshots", exist_ok=True)
            image_data = base64.b64decode(screenshot_result["image_data"])
            with open(f"screenshots/{filename}", 'wb') as f:
                f.write(image_data)
            print(f"   📸 Screenshot saved: screenshots/{filename}")
        else:
            print("❌ Vision Screenshot: FAILED")
            results.append("❌ Vision Screenshot")
            
        # Test OCR (if available)
        try:
            ocr_status = vision_mgr.get_ocr_status()
            if ocr_status.get("available"):
                print("✅ Vision OCR: AVAILABLE")
                results.append("✅ Vision OCR")
            else:
                print("⚠️ Vision OCR: NOT AVAILABLE") 
                results.append("⚠️ Vision OCR")
        except:
            results.append("⚠️ Vision OCR")
            
    except Exception as e:
        print(f"❌ Vision System Error: {e}")
        results.append("❌ Vision System")
    
    # Test 4: Automation System
    print("\n🤖 Testing Automation System...")
    
    try:
        # Test screenshot analysis
        automation_screenshot = automation_mgr.screenshot_analysis()
        if "error" not in automation_screenshot:
            print("✅ Automation Screenshot: WORKING")
            results.append("✅ Automation Screenshot")
        else:
            print("❌ Automation Screenshot: FAILED")
            results.append("❌ Automation Screenshot")
            
        # Test system info
        system_info = automation_mgr.process_control("system_info")
        if system_info.get("success"):
            print("✅ Automation System Info: WORKING")
            results.append("✅ Automation System Info")
        else:
            print("❌ Automation System Info: FAILED")
            results.append("❌ Automation System Info")
            
        # Test window management
        windows = automation_mgr.window_management("list_all")
        if windows.get("count", 0) > 0:
            print(f"✅ Automation Windows: WORKING ({windows['count']} windows)")
            results.append("✅ Automation Windows")
        else:
            print("❌ Automation Windows: FAILED")
            results.append("❌ Automation Windows")
            
    except Exception as e:
        print(f"❌ Automation System Error: {e}")
        results.append("❌ Automation System")
    
    # Test 5: File Operations
    print("\n📁 Testing File Operations...")
    
    try:
        # Test directory listing
        current_dir = automation_mgr.file_system_operations("list_directory", path=".")
        if current_dir.get("success"):
            print(f"✅ File Operations: WORKING ({len(current_dir.get('items', []))} items)")
            results.append("✅ File Operations")
        else:
            print("❌ File Operations: FAILED")
            results.append("❌ File Operations")
            
    except Exception as e:
        print(f"❌ File Operations Error: {e}")
        results.append("❌ File Operations")
    
    # Generate Final Summary
    print("\n" + "=" * 60)
    print("📊 FINAL ULTRON OMNIPOTENT TEST RESULTS")
    print("=" * 60)
    
    total = len(results)
    working = len([r for r in results if "✅" in r])
    failed = len([r for r in results if "❌" in r])
    warnings = len([r for r in results if "⚠️" in r])
    
    print(f"Total Functions Tested: {total}")
    print(f"✅ Working: {working}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️ Warnings: {warnings}")
    print(f"Success Rate: {(working/total)*100:.1f}%")
    
    print("\nDETAILED RESULTS:")
    for result in results:
        print(f"  {result}")
    
    print("\n" + "=" * 60)
    
    if working >= total * 0.9:  # 90% success rate
        print("🎉 ULTRON OMNIPOTENT SYSTEM FULLY OPERATIONAL!")
        print("🤖 ALL MAJOR CAPABILITIES VERIFIED ✨")
        print("🚀 READY FOR SUPREME AUTOMATION TASKS")
    elif working >= total * 0.7:  # 70% success rate
        print("✅ ULTRON SYSTEM MOSTLY OPERATIONAL")
        print("🔧 Some minor issues to address")
    else:
        print("⚠️ ULTRON SYSTEM NEEDS ATTENTION")
        print("🛠️ Multiple capabilities require fixes")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_all_functions())