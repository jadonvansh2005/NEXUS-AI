from llm.router.task_classifier import (
    TaskClassifier
)

from llm.router.routing_rules import (
    ROUTING_RULES
)

from llm.providers.gemini.gemini_client import (
    GeminiClient
)


class ModelRouter:

    def __init__(self):

        self.classifier = (
            TaskClassifier()
        )

        self.models = {

            "gemini":
                GeminiClient()

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

            model = self.models[
                model_name
            ]

            return model.generate(
                prompt
            )
        except Exception as e:
            import traceback
            print(f"\n[ModelRouter Error] Failed to generate response for domain '{domain}': {e}")
            traceback.print_exc()
            raise e