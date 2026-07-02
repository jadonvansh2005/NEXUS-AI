from llm.router.base_llm import BaseLLM

import google.generativeai as genai

from app.settings import settings


class GeminiClient(BaseLLM):

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate(
        self,
        prompt: str,
        timeout: float = 10.0
    ):
        try:
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": timeout}
            )
            return response.text
        except Exception as e:
            # Fallback if request_options fails in an older SDK version
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as inner_e:
                raise inner_e