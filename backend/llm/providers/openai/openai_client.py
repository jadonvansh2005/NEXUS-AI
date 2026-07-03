import os
import requests
from app.settings import settings

class OpenAIClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[OpenAI Client] Error: OPENAI_API_KEY not configured in .env"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = None
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            if response is not None:
                return f"[OpenAI Error] {e}: {response.text}"
            return f"[OpenAI Error] {e}"
