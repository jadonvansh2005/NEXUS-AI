from rag.embeddings.embedding_models import (
    SUPPORTED_MODELS
)

from rag.embeddings.model_loader import (
    ModelLoader
)


class EmbeddingFactory:

    @staticmethod
    def get_model(

        model_key: str

    ):

        if model_key not in SUPPORTED_MODELS:

            raise ValueError(

                f"Unsupported embedding model: "

                f"{model_key}"

            )

        return ModelLoader.load(

            model_key=model_key

        )

    @staticmethod
    def get_default_model():

        return ModelLoader.load()