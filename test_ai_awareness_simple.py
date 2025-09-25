#!/usr/bin/env python3
"""
Focused AI Model Tool Awareness Test
Tests only AI chat functionality without problematic OCR
"""
import requests
import json
import time

BASE_URL = "http://localhost:8009"

def test_ai_model_simple(provider):
    """Simple test to check if AI model understands available tools"""
    print(f"\n🤖 Testing {provider.upper()} tool awareness...")
    
    # Simple capability question
    capability_question = """
    What automation tools and capabilities do you have access to through ULTRON? 
    Please list the main categories like voice, vision, automation, file operations, etc.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": capability_question,
                "provider": provider
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("response", "")
            
            # Check if response mentions key capabilities
            key_terms = ["automation", "voice", "vision", "screenshot", "file", "system"]
            mentioned_terms = [term for term in key_terms if term.lower() in ai_response.lower()]
            
            print(f"✅ {provider.upper()} responded successfully")
            print(f"📝 Response length: {len(ai_response)} characters")
            print(f"🎯 Mentioned capabilities: {', '.join(mentioned_terms)}")
            print(f"🧠 Tool awareness score: {len(mentioned_terms)}/{len(key_terms)}")
            
            return len(mentioned_terms) >= 3  # Consider aware if mentions 3+ capabilities
            
        else:
            print(f"❌ {provider.upper()} request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {provider.upper()} error: {str(e)}")
        return False

def test_system_endpoints():
    """Test basic system endpoints"""
    print(f"\n🔧 Testing system endpoints...")
    
    endpoints_to_test = [
        ("/health", "Health check"),
        ("/status", "Status check"), 
        ("/automation/status", "Automation status"),
        ("/voice/status", "Voice status")
    ]
    
    working_endpoints = 0
    
    for endpoint, description in endpoints_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {description}: Working")
                working_endpoints += 1
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
    
    return working_endpoints, len(endpoints_to_test)

def main():
    """Run focused AI model tool awareness test"""
    print("🚀 ULTRON AI MODEL TOOL AWARENESS TEST (Simplified)")
    print("Testing AI models' understanding of available capabilities")
    print("=" * 65)
    
    # Check server health first
    try:
        health_check = requests.get(f"{BASE_URL}/health", timeout=10)
        if health_check.status_code != 200:
            print("❌ ULTRON server not healthy - exiting")
            return
    except:
        print("❌ Cannot connect to ULTRON server - exiting")
        return
    
    print("✅ ULTRON server is online and healthy")
    
    # Test system endpoints
    working_endpoints, total_endpoints = test_system_endpoints()
    
    # Test AI models
    providers = ["openai", "anthropic", "ollama"]
    model_results = []
    
    for provider in providers:
        result = test_ai_model_simple(provider)
        model_results.append((provider, result))
        time.sleep(2)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 65)
    print("📊 FINAL RESULTS")
    print("=" * 65)
    
    working_models = sum(1 for _, result in model_results if result)
    total_models = len(model_results)
    
    print(f"🌐 System Endpoints: {working_endpoints}/{total_endpoints} working")
    print(f"🤖 AI Models Tested: {total_models}")
    print(f"✅ Tool-Aware Models: {working_models}")
    
    print("\nDetailed Model Results:")
    for provider, result in model_results:
        status = "✅ Tool-Aware" if result else "❌ Needs Training"
        print(f"  {provider.upper()}: {status}")
    
    print("\n" + "=" * 65)
    
    if working_models == total_models and working_endpoints >= 3:
        print("🎉 EXCELLENT! All AI models understand their tools!")
        print("🤖 ULTRON omnipotent capabilities fully recognized")
        print("🚀 Ready for complex automation tasks")
    elif working_models > 0:
        print("✅ Good! Some models are tool-aware")
        print("🔧 Continue developing others")
    else:
        print("⚠️ Models need more tool awareness training")
        print("📚 Consider sending detailed capability documentation")
    
    print("=" * 65)

if __name__ == "__main__":
    main()