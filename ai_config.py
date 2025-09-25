"""
Basic AI Configuration for ULTRON Dashboard
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIConfig:
    def __init__(self):
        self.providers = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-3.5-turbo",
                "enabled": bool(os.getenv("OPENAI_API_KEY"))
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"), 
                "model": "claude-3-5-sonnet-20241022",
                "enabled": bool(os.getenv("ANTHROPIC_API_KEY"))
            },
            "ollama": {
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                "model": os.getenv("OLLAMA_MODEL", "qwen3-coder:480b-cloud"),  # Updated to use your cloud model
                "enabled": True  # Assume ollama is available locally
            }
        }
    
    def get_provider_config(self, provider: str) -> Optional[Dict]:
        return self.providers.get(provider)
    
    def is_provider_enabled(self, provider: str) -> bool:
        config = self.get_provider_config(provider)
        return config and config.get("enabled", False)