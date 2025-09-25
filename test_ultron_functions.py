#!/usr/bin/env python3
"""
ULTRON Omnipotent Capabilities End-to-End Test Suite
Tests all functions to verify they perform actions with expected outcomes
"""

import requests
import json
import time
import os
from pathlib import Path

# ULTRON server endpoint
ULTRON_BASE_URL = "http://localhost:8009"

class UltronTester:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def log_test(self, test_name, result, details=None):
        """Log test result"""
        status = "✅ PASS" if result else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "result": result,
            "details": details
        })
        if result:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_ai_providers(self):
        """Test all AI providers (OpenAI, Anthropic, Ollama)"""
        print("\n🧠 Testing AI Providers...")
        
        providers = ["openai", "anthropic", "ollama"]
        for provider in providers:
            try:
                response = requests.post(
                    f"{ULTRON_BASE_URL}/chat/{provider}",
                    json={"message": "Test message - respond with 'ULTRON ACTIVE'"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "ULTRON" in str(data).upper():
                        self.log_test(f"AI Provider {provider.upper()}", True, f"Response: {str(data)[:100]}...")
                    else:
                        self.log_test(f"AI Provider {provider.upper()}", False, f"Unexpected response: {data}")
                else:
                    self.log_test(f"AI Provider {provider.upper()}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"AI Provider {provider.upper()}", False, str(e))
    
    def test_voice_capabilities(self):
        """Test voice recognition and synthesis"""
        print("\n🎤 Testing Voice Capabilities...")
        
        # Test TTS (Text-to-Speech)
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/voice/synthesize",
                json={"text": "ULTRON voice synthesis test successful"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Voice Text-to-Speech", True, data.get("message", "TTS completed"))
            else:
                self.log_test("Voice Text-to-Speech", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Voice Text-to-Speech", False, str(e))
        
        # Test voice recognition capabilities
        try:
            response = requests.get(f"{ULTRON_BASE_URL}/voice/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Voice Recognition Status", True, data.get("status", "Available"))
            else:
                self.log_test("Voice Recognition Status", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Voice Recognition Status", False, str(e))
    
    def test_vision_capabilities(self):
        """Test OCR and computer vision"""
        print("\n👁️ Testing Vision Capabilities...")
        
        # Test screenshot capability
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/vision/screenshot",
                json={"analyze": True},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if "screenshot_path" in str(data) or "analysis" in str(data):
                    self.log_test("Vision Screenshot", True, "Screenshot captured and analyzed")
                else:
                    self.log_test("Vision Screenshot", False, f"Unexpected response: {data}")
            else:
                self.log_test("Vision Screenshot", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Vision Screenshot", False, str(e))
        
        # Test OCR capabilities
        try:
            response = requests.get(f"{ULTRON_BASE_URL}/vision/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Vision OCR Status", True, data.get("status", "OCR Ready"))
            else:
                self.log_test("Vision OCR Status", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Vision OCR Status", False, str(e))
    
    def test_automation_capabilities(self):
        """Test PyAutoGUI and system automation"""
        print("\n🤖 Testing Automation Capabilities...")
        
        # Test system info
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/system_info",
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "cpu_count" in str(data) or "memory" in str(data):
                    self.log_test("System Information", True, f"System data retrieved: {str(data)[:100]}...")
                else:
                    self.log_test("System Information", False, f"No system data: {data}")
            else:
                self.log_test("System Information", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("System Information", False, str(e))
        
        # Test window management
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/window_management",
                json={"action": "list_all"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "windows" in str(data) or "count" in str(data):
                    self.log_test("Window Management", True, f"Windows detected: {data.get('count', 'N/A')}")
                else:
                    self.log_test("Window Management", False, f"No window data: {data}")
            else:
                self.log_test("Window Management", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Window Management", False, str(e))
        
        # Test process control
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/process_control",
                json={"action": "list_processes"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "processes" in str(data):
                    self.log_test("Process Control", True, f"Processes listed: {data.get('total_count', 'N/A')}")
                else:
                    self.log_test("Process Control", False, f"No process data: {data}")
            else:
                self.log_test("Process Control", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Process Control", False, str(e))
    
    def test_file_operations(self):
        """Test file system operations"""
        print("\n📁 Testing File Operations...")
        
        # Test directory listing
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/file_operations",
                json={
                    "action": "list_directory",
                    "path": "."
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "items" in str(data):
                    self.log_test("File Directory Listing", True, f"Items found: {len(data.get('items', []))}")
                else:
                    self.log_test("File Directory Listing", False, f"No items data: {data}")
            else:
                self.log_test("File Directory Listing", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("File Directory Listing", False, str(e))
        
        # Test file creation and deletion
        test_file = "ultron_test_file.txt"
        try:
            # Create test file
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/file_operations",
                json={
                    "action": "write",
                    "path": test_file,
                    "content": "ULTRON test file content"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("File Creation", True, f"File created: {test_file}")
                    
                    # Clean up - delete test file
                    requests.post(
                        f"{ULTRON_BASE_URL}/automation/file_operations",
                        json={"action": "delete", "path": test_file},
                        timeout=5
                    )
                else:
                    self.log_test("File Creation", False, f"Creation failed: {data}")
            else:
                self.log_test("File Creation", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("File Creation", False, str(e))
    
    def test_network_operations(self):
        """Test network capabilities"""
        print("\n🌐 Testing Network Operations...")
        
        try:
            response = requests.post(
                f"{ULTRON_BASE_URL}/automation/network_operations",
                json={
                    "action": "get",
                    "url": "https://httpbin.org/get"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "httpbin" in str(data):
                    self.log_test("Network Operations", True, "HTTP GET request successful")
                else:
                    self.log_test("Network Operations", False, f"Request failed: {data}")
            else:
                self.log_test("Network Operations", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Network Operations", False, str(e))
    
    def test_server_health(self):
        """Test server health and status"""
        print("\n⚕️ Testing Server Health...")
        
        try:
            response = requests.get(f"{ULTRON_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Server Health Check", True, data.get("status", "Healthy"))
            else:
                self.log_test("Server Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Server Health Check", False, str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🚀 ULTRON OMNIPOTENT CAPABILITIES TEST SUITE")
        print("=" * 60)
        
        # Test server connectivity first
        try:
            response = requests.get(f"{ULTRON_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ ULTRON server is accessible")
            else:
                print(f"❌ Server connection failed: HTTP {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Cannot connect to ULTRON server: {e}")
            return
        
        # Run all capability tests
        self.test_server_health()
        self.test_ai_providers()
        self.test_voice_capabilities()
        self.test_vision_capabilities()
        self.test_automation_capabilities()
        self.test_file_operations()
        self.test_network_operations()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(f"{result['status']}: {result['test']}")
        
        print(f"\n📊 FINAL SCORE: {self.passed} PASSED, {self.failed} FAILED")
        
        if self.failed == 0:
            print("🎉 ALL ULTRON CAPABILITIES FULLY OPERATIONAL! 🎉")
        else:
            print(f"⚠️  {self.failed} capabilities need attention")
        
        return self.failed == 0

if __name__ == "__main__":
    tester = UltronTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🤖 ULTRON is ready for omnipotent operations!")
    else:
        print("\n🔧 Some capabilities require debugging")