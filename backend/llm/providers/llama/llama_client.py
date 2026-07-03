import os
import requests

class LlamaClient:
    def __init__(self):
        self.endpoint = os.getenv("LLAMA_ENDPOINT", "http://localhost:11434/api/generate")
        self.model = os.getenv("LLAMA_MODEL", "llama3")

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            return f"[Llama/Ollama Local Error] {e}"
