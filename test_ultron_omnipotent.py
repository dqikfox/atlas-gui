"""
ULTRON Omnipotent System - End-to-End Testing Suite
Tests all capabilities to verify expected outcomes
"""

import requests
import json
import time
import os
from pathlib import Path
import base64

# Test configuration
BASE_URL = "http://localhost:8009"
TEST_RESULTS = []

def log_test(test_name, success, details="", error=""):
    """Log test results"""
    result = {
        "test": test_name,
        "success": success,
        "timestamp": time.time(),
        "details": details,
        "error": error
    }
    TEST_RESULTS.append(result)
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {test_name}")
    if details:
        print(f"     Details: {details}")
    if error:
        print(f"     Error: {error}")
    print()

def test_ai_providers():
    """Test all 3 AI providers"""
    print("🧠 TESTING AI PROVIDERS...")
    
    providers = ["openai", "anthropic", "ollama"]
    test_message = "Hello ULTRON, respond with exactly: 'AI_TEST_SUCCESS'"
    
    for provider in providers:
        try:
            response = requests.post(f"{BASE_URL}/chat", json={
                "message": test_message,
                "provider": provider
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                if "AI_TEST_SUCCESS" in ai_response:
                    log_test(f"AI Provider - {provider.upper()}", True, f"Response: {ai_response[:100]}...")
                else:
                    log_test(f"AI Provider - {provider.upper()}", False, f"Unexpected response: {ai_response[:100]}...")
            else:
                log_test(f"AI Provider - {provider.upper()}", False, error=f"HTTP {response.status_code}")
                
        except Exception as e:
            log_test(f"AI Provider - {provider.upper()}", False, error=str(e))
        
        time.sleep(1)  # Rate limiting

def test_vision_system():
    """Test OCR and vision capabilities"""
    print("👁️ TESTING VISION SYSTEM...")
    
    # Test screenshot capability
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "screenshot_analysis"
        }, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "screenshot_path" in data.get("result", {}):
                log_test("Vision - Screenshot Analysis", True, f"Screenshot saved to: {data['result']['screenshot_path']}")
            else:
                log_test("Vision - Screenshot Analysis", False, error="No screenshot path in response")
        else:
            log_test("Vision - Screenshot Analysis", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Vision - Screenshot Analysis", False, error=str(e))
    
    # Test OCR on an existing image if available
    test_images = ["imgs/cyberpunk_ai_robot_orange_eyes_neon_background_cinematic_concept_art.jpg"]
    for img_path in test_images:
        if os.path.exists(img_path):
            try:
                response = requests.post(f"{BASE_URL}/ocr", json={
                    "image_path": img_path
                }, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        extracted_text = data.get("text", "")
                        log_test("Vision - OCR Processing", True, f"Extracted {len(extracted_text)} characters")
                    else:
                        log_test("Vision - OCR Processing", False, error=data.get("error", "Unknown OCR error"))
                else:
                    log_test("Vision - OCR Processing", False, error=f"HTTP {response.status_code}")
                    
            except Exception as e:
                log_test("Vision - OCR Processing", False, error=str(e))
            break

def test_automation_safe():
    """Test safe automation functions (no actual system control)"""
    print("🤖 TESTING SAFE AUTOMATION...")
    
    # Test system info (read-only)
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "process_control",
            "data": {
                "action": "system_info"
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "cpu_count" in data.get("result", {}):
                cpu_count = data["result"]["cpu_count"]
                memory_total = data["result"]["memory_total"]
                log_test("Automation - System Info", True, f"CPU: {cpu_count} cores, Memory: {memory_total//1024//1024//1024}GB")
            else:
                log_test("Automation - System Info", False, error="Missing system info data")
        else:
            log_test("Automation - System Info", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Automation - System Info", False, error=str(e))
    
    # Test process listing (read-only)
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "process_control",
            "data": {
                "action": "list_processes"
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "total_count" in data.get("result", {}):
                process_count = data["result"]["total_count"]
                log_test("Automation - Process Listing", True, f"Found {process_count} running processes")
            else:
                log_test("Automation - Process Listing", False, error="Missing process data")
        else:
            log_test("Automation - Process Listing", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Automation - Process Listing", False, error=str(e))

def test_file_operations():
    """Test file system operations"""
    print("📁 TESTING FILE OPERATIONS...")
    
    test_dir = "test_ultron_files"
    test_file = f"{test_dir}/test_file.txt"
    test_content = "ULTRON FILE OPERATION TEST - SUCCESS"
    
    # Create directory
    try:
        os.makedirs(test_dir, exist_ok=True)
        log_test("File Ops - Directory Creation", True, f"Created directory: {test_dir}")
    except Exception as e:
        log_test("File Ops - Directory Creation", False, error=str(e))
        return
    
    # Test file write
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "file_system_operations",
            "data": {
                "action": "write",
                "path": test_file,
                "content": test_content
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                log_test("File Ops - Write File", True, f"Wrote {len(test_content)} characters")
            else:
                log_test("File Ops - Write File", False, error=data.get("error", "Write failed"))
        else:
            log_test("File Ops - Write File", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("File Ops - Write File", False, error=str(e))
    
    # Test file read
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "file_system_operations",
            "data": {
                "action": "read",
                "path": test_file
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("result", {}).get("content") == test_content:
                log_test("File Ops - Read File", True, f"Read content matches written content")
            else:
                log_test("File Ops - Read File", False, error="Content mismatch or read failed")
        else:
            log_test("File Ops - Read File", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("File Ops - Read File", False, error=str(e))
    
    # Test directory listing
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "file_system_operations",
            "data": {
                "action": "list_directory",
                "path": test_dir
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                items = data.get("result", {}).get("items", [])
                log_test("File Ops - Directory Listing", True, f"Found {len(items)} items in directory")
            else:
                log_test("File Ops - Directory Listing", False, error=data.get("error", "Listing failed"))
        else:
            log_test("File Ops - Directory Listing", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("File Ops - Directory Listing", False, error=str(e))
    
    # Cleanup
    try:
        import shutil
        shutil.rmtree(test_dir)
        log_test("File Ops - Cleanup", True, f"Cleaned up test directory")
    except Exception as e:
        log_test("File Ops - Cleanup", False, error=str(e))

def test_network_operations():
    """Test network capabilities"""
    print("🌐 TESTING NETWORK OPERATIONS...")
    
    # Test HTTP GET request
    try:
        response = requests.post(f"{BASE_URL}/automation", json={
            "action": "network_operations",
            "data": {
                "action": "get",
                "url": "https://httpbin.org/get"
            }
        }, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("result", {}).get("status_code") == 200:
                log_test("Network - HTTP GET", True, f"Successfully retrieved data from httpbin.org")
            else:
                log_test("Network - HTTP GET", False, error="Failed to get successful response")
        else:
            log_test("Network - HTTP GET", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Network - HTTP GET", False, error=str(e))

def test_voice_system():
    """Test voice capabilities (if available)"""
    print("🎤 TESTING VOICE SYSTEM...")
    
    # Test text-to-speech
    try:
        response = requests.post(f"{BASE_URL}/voice/speak", json={
            "text": "ULTRON voice system test successful"
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                log_test("Voice - Text-to-Speech", True, "TTS synthesis completed")
            else:
                log_test("Voice - Text-to-Speech", False, error=data.get("error", "TTS failed"))
        else:
            log_test("Voice - Text-to-Speech", False, error=f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Voice - Text-to-Speech", False, error=str(e))

def test_dashboard_endpoints():
    """Test web dashboard endpoints"""
    print("🌐 TESTING DASHBOARD ENDPOINTS...")
    
    endpoints = [
        ("/", "Dashboard Home"),
        ("/health", "Health Check"),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                log_test(f"Dashboard - {name}", True, f"Endpoint accessible")
            else:
                log_test(f"Dashboard - {name}", False, error=f"HTTP {response.status_code}")
        except Exception as e:
            log_test(f"Dashboard - {name}", False, error=str(e))

def generate_test_report():
    """Generate comprehensive test report"""
    print("\n" + "="*60)
    print("🎯 ULTRON OMNIPOTENT SYSTEM - TEST REPORT")
    print("="*60)
    
    total_tests = len(TEST_RESULTS)
    passed_tests = len([t for t in TEST_RESULTS if t["success"]])
    failed_tests = total_tests - passed_tests
    
    print(f"📊 SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests} ✅")
    print(f"   Failed: {failed_tests} ❌")
    print(f"   Success Rate: {(passed_tests/total_tests*100):.1f}%")
    print()
    
    if failed_tests > 0:
        print("❌ FAILED TESTS:")
        for test in TEST_RESULTS:
            if not test["success"]:
                print(f"   • {test['test']}: {test['error']}")
        print()
    
    print("✅ PASSED TESTS:")
    for test in TEST_RESULTS:
        if test["success"]:
            print(f"   • {test['test']}")
    
    # Save detailed report
    report_file = f"ultron_test_report_{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(TEST_RESULTS, f, indent=2)
    
    print(f"\n📋 Detailed report saved to: {report_file}")
    return passed_tests == total_tests

def main():
    """Run all tests"""
    print("🚀 STARTING ULTRON OMNIPOTENT SYSTEM TESTING...")
    print("="*60)
    
    start_time = time.time()
    
    # Run all test suites
    test_dashboard_endpoints()
    test_ai_providers()
    test_vision_system()
    test_automation_safe()
    test_file_operations()
    test_network_operations()
    test_voice_system()
    
    end_time = time.time()
    
    # Generate final report
    all_passed = generate_test_report()
    
    print(f"\n⏱️  Total test time: {end_time - start_time:.2f} seconds")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - ULTRON IS FULLY OMNIPOTENT! 🎉")
    else:
        print("\n⚠️  SOME TESTS FAILED - CHECK REPORT FOR DETAILS")
    
    return all_passed

if __name__ == "__main__":
    main()