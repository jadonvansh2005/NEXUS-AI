import os
import requests
from app.settings import settings

class ClaudeClient:
    def __init__(self):
        raw_key = settings.CLAUDE_API_KEY or os.getenv("CLAUDE_API_KEY", "")
        self.api_key = raw_key.strip() if raw_key else ""
        raw_model = os.getenv("CLAUDE_MODEL") or "claude-3-5-sonnet-20240620"
        self.model = raw_model.strip()

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[Claude Client] Error: CLAUDE_API_KEY not configured in .env"
        
        headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = None
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            if response is not None:
                return f"[Claude Error] {e}: {response.text}"
            return f"[Claude Error] {e}"
