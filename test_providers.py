#!/usr/bin/env python3
"""
Test ULTRON AI Provider Connections
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from agent_core import UltronAgent

async def test_providers():
    """Test all AI providers"""
    agent = UltronAgent()
    test_message = "Hello! Please respond with a short greeting."
    
    providers = ["openai", "anthropic", "ollama"]
    
    print("🔍 Testing ULTRON AI Providers...")
    print("=" * 50)
    
    for provider in providers:
        print(f"\n🤖 Testing {provider.upper()}...")
        try:
            result = await agent.process_message(test_message, provider)
            
            if isinstance(result, dict):
                if result.get("error"):
                    print(f"❌ {provider}: {result['response']}")
                else:
                    print(f"✅ {provider}: {result['response'][:100]}...")
            else:
                print(f"✅ {provider}: {str(result)[:100]}...")
                
        except Exception as e:
            print(f"❌ {provider}: Exception - {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_providers())