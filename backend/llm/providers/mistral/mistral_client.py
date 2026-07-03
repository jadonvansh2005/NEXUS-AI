import os
import requests
from app.settings import settings

class MistralClient:
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY or os.getenv("MISTRAL_API_KEY", "")
        self.model = os.getenv("MISTRAL_MODEL", "mistral-tiny")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[Mistral Client] Error: MISTRAL_API_KEY not configured in .env"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Mistral Error] {e}"
