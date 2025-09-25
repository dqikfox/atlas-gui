import sys
sys.path.append('.')
from voice_manager import VoiceManager
from vision import VisionManager
import asyncio
import os

async def test_voice_tts():
    """Test the TTS functionality directly"""
    print("🎤 Testing ULTRON Voice TTS...")
    
    try:
        voice_mgr = VoiceManager()
        result = await voice_mgr.speak_text("ULTRON is online")
        print(f"✅ TTS Result: {result}")
        return True
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return False

def test_screenshot():
    """Test screenshot functionality directly"""
    print("\n📷 Testing ULTRON Vision Screenshot...")
    
    try:
        vision_mgr = VisionManager()
        result = vision_mgr.take_screenshot()
        
        if result.get("status") == "success":
            print(f"✅ Screenshot Result: {result['message']}")
            
            # Save the screenshot
            filename = f"test_screenshot_{int(time.time())}.png"
            import base64
            image_data = base64.b64decode(result["image_data"])
            
            os.makedirs("screenshots", exist_ok=True)
            with open(f"screenshots/{filename}", 'wb') as f:
                f.write(image_data)
                
            print(f"✅ Screenshot saved: screenshots/{filename}")
            return True
        else:
            print(f"❌ Screenshot failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot Error: {e}")
        return False

async def main():
    print("🚀 ULTRON Direct Function Test")
    print("=" * 40)
    
    voice_result = await test_voice_tts()
    screenshot_result = test_screenshot()
    
    print("\n" + "=" * 40)
    print("📊 DIRECT TEST RESULTS")
    print("=" * 40)
    
    if voice_result:
        print("✅ Voice TTS: WORKING")
    else:
        print("❌ Voice TTS: NEEDS FIX")
    
    if screenshot_result:
        print("✅ Screenshot: WORKING")  
    else:
        print("❌ Screenshot: NEEDS FIX")
        
    if voice_result and screenshot_result:
        print("\n🎉 BOTH FUNCTIONS WORKING!")
    else:
        print("\n⚠️  Some functions need debugging")

if __name__ == "__main__":
    import time
    asyncio.run(main())