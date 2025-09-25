"""
Basic ULTRON Agent Implementation
"""
import asyncio
import json
import os
from typing import Dict, Optional, Any
import httpx
import anthropic
from ai_config import AIConfig

class UltronAgent:
    def __init__(self):
        self.ai_config = AIConfig()
        self.session_history = []
        self.initialized = True
    
    def initialize(self):
        """Initialize the agent (for compatibility with server)"""
        self.initialized = True
        return self
    
    async def async_initialize(self):
        """Async initialization method"""
        self.initialized = True
        return self
    
    async def process_message(self, message: str, provider: str = "openai", include_voice: bool = False) -> Dict[str, Any]:
        """Process a message using the specified AI provider"""
        try:
            if provider == "openai":
                return await self._call_openai(message)
            elif provider == "anthropic":
                return await self._call_anthropic(message)
            elif provider == "ollama":
                return await self._call_ollama(message)
            else:
                return {
                    "response": "Unknown AI provider. Available: openai, anthropic, ollama",
                    "error": True
                }
        except Exception as e:
            return {
                "response": f"AI Error: {str(e)}",
                "error": True
            }
    
    async def _call_openai(self, message: str) -> Dict[str, Any]:
        config = self.ai_config.get_provider_config("openai")
        if not config or not config.get("api_key"):
            return {"response": "OpenAI API key not configured", "error": True}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config['api_key']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config["model"],
                    "messages": [{"role": "user", "content": message}],
                    "max_tokens": 500
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "provider": "openai",
                    "model": config["model"]
                }
            else:
                return {"response": f"OpenAI API error: {response.status_code}", "error": True}
    
    async def _call_anthropic(self, message: str) -> Dict[str, Any]:
        config = self.ai_config.get_provider_config("anthropic")
        if not config or not config.get("api_key"):
            return {"response": "Anthropic API key not configured", "error": True}
        
        try:
            client = anthropic.Anthropic(
                api_key=config["api_key"]
            )
            
            response = client.messages.create(
                model=config["model"],
                max_tokens=8192,
                temperature=1,
                system="You are ULTRON, an advanced AI assistant. Build the ultron_agent project - this is your command centre.",
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            
            return {
                "response": response.content[0].text,
                "provider": "anthropic",
                "model": config["model"]
            }
            
        except Exception as e:
            return {"response": f"Anthropic API error: {str(e)}", "error": True}
    
    async def _call_ollama(self, message: str) -> Dict[str, Any]:
        config = self.ai_config.get_provider_config("ollama")
        
        async with httpx.AsyncClient() as client:
            try:
                # Try chat format first (for cloud models like qwen3-coder:480b-cloud)
                response = await client.post(
                    f"{config['base_url']}/api/chat",
                    json={
                        "model": config["model"],
                        "messages": [{"role": "user", "content": message}],
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["message"]["content"],
                        "provider": "ollama",
                        "model": config["model"]
                    }
                else:
                    # Fallback to generate format (for local models)
                    response = await client.post(
                        f"{config['base_url']}/api/generate",
                        json={
                            "model": config["model"],
                            "prompt": message,
                            "stream": False
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "response": data["response"],
                            "provider": "ollama",
                            "model": config["model"]
                        }
                    else:
                        return {"response": f"Ollama API error: {response.status_code}", "error": True}
            except httpx.ConnectError:
                return {"response": "Ollama server not running or unreachable", "error": True}
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and available providers"""
        return {
            "status": "operational",
            "providers": {
                name: {
                    "enabled": self.ai_config.is_provider_enabled(name),
                    "model": config.get("model")
                }
                for name, config in self.ai_config.providers.items()
            }
        }