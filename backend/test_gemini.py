from llm.providers.gemini.gemini_client import (
    GeminiClient
)

client = GeminiClient()

response = client.generate(
    "What is Machine Learning?"
)

print(response)