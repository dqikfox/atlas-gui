#!/usr/bin/env python3
"""
Debug OCR functionality to identify the issue
"""
import requests
import time

BASE_URL = "http://localhost:8009"

def test_ocr_debug():
    """Test OCR with detailed error reporting"""
    print("🔍 Testing OCR functionality...")
    
    try:
        response = requests.post(f"{BASE_URL}/automation/ocr", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OCR Success!")
            print(f"Extracted text length: {len(result.get('text', ''))}")
            print(f"Text sample: {result.get('text', '')[:100]}...")
        else:
            print(f"❌ OCR Failed: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Raw response: {response.text}")
                
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def test_screenshot_first():
    """Test screenshot before OCR"""
    print("📷 Testing screenshot functionality...")
    
    try:
        response = requests.post(f"{BASE_URL}/automation/screenshot", timeout=15)
        
        if response.status_code == 200:
            print("✅ Screenshot Success!")
            return True
        else:
            print(f"❌ Screenshot Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot request failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 OCR DEBUG TEST")
    print("=" * 40)
    
    # Test screenshot first
    if test_screenshot_first():
        print()
        # Then test OCR
        test_ocr_debug()
    else:
        print("❌ Cannot test OCR without working screenshots")