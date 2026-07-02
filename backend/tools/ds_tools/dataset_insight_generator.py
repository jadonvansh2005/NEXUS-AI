from llm.providers.gemini.gemini_client import (
    GeminiClient
)


class DatasetInsightGenerator:

    def __init__(self):

        self.llm = GeminiClient()

    def generate(
        self,
        report: dict
    ):

        prompt = f"""
You are a Senior Data Scientist.

Analyze the dataset report below.

Dataset Report:

{report}

Provide:

1. Dataset Overview
2. Data Quality Assessment
3. Important Features
4. Potential Target Variable
5. Suitable ML Problem Type
6. Recommended Algorithms
7. Key Insights

Keep response professional.
"""

        return self.llm.generate(
            prompt
        )