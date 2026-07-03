from llm.router.task_classifier import (
    TaskClassifier
)

from llm.router.routing_rules import (
    ROUTING_RULES
)

from llm.providers.gemini.gemini_client import (
    GeminiClient
)

from llm.providers.openai.openai_client import (
    OpenAIClient
)

from llm.providers.claude.claude_client import (
    ClaudeClient
)

from llm.providers.mistral.mistral_client import (
    MistralClient
)

from llm.providers.llama.llama_client import (
    LlamaClient
)


class ModelRouter:

    def __init__(self):

        self.classifier = (
            TaskClassifier()
        )

        self.models = {
            "gemini": GeminiClient(),
            "openai": OpenAIClient(),
            "claude": ClaudeClient(),
            "mistral": MistralClient(),
            "llama": LlamaClient()
        }

    def generate(

        self,

        prompt: str,

        query: str,

        domain: str

    ):

        try:
            task_type = (

                self.classifier.classify(

                    query,

                    domain

                )
            )

            model_name = (

                ROUTING_RULES.get(

                    task_type,

                    "gemini"

                )
            )

            # Check if the requested model exists, default to gemini
            model = self.models.get(model_name, self.models["gemini"])

            # Verify if the model's key is configured, fallback if not
            if hasattr(model, "api_key") and not getattr(model, "api_key", None):
                print(f"[ModelRouter Warning] API key for '{model_name}' is not set. Falling back to Gemini.")
                model = self.models["gemini"]
                model_name = "gemini"

            print(f"[ModelRouter] Routing '{task_type}' task in domain '{domain}' using model '{model_name}'")
            response = model.generate(prompt)

            # Check if the response indicates a configuration or runtime error, fallback if so
            if isinstance(response, str) and (
                "[OpenAI Client] Error:" in response or 
                "[Claude Client] Error:" in response or 
                "[Mistral Client] Error:" in response or
                "[OpenAI Error]" in response or
                "[Claude Error]" in response or
                "[Mistral Error]" in response
            ):
                print(f"[ModelRouter Fallback] Provider '{model_name}' returned error. Falling back to Gemini.")
                response = self.models["gemini"].generate(prompt)

            return response
        except Exception as e:
            import traceback
            print(f"\n[ModelRouter Error] Failed to generate response for domain '{domain}': {e}")
            traceback.print_exc()
            raise e