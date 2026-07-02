from rag.embeddings.embedding_models import (
    SUPPORTED_MODELS,
    DEFAULT_MODEL
)

import torch

from sentence_transformers import (
    SentenceTransformer
)


class ModelLoader:

    _model = None

    _config = None

    @classmethod
    def load(

        cls,

        model_key: str = DEFAULT_MODEL

    ):

        if cls._model is not None:

            return cls._model

        if model_key not in SUPPORTED_MODELS:

            raise ValueError(

                f"Embedding model "

                f"'{model_key}' "

                f"is not supported."

            )

        cls._config = (

            SUPPORTED_MODELS[

                model_key

            ]

        )

        device = (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

        print(

            f"\n[ModelLoader] Loading Embedding Model: {cls._config.model_name}"

        )

        print(

            f"[ModelLoader] Running Device: {device.upper()}"

        )

        try:
            cls._model = (

                SentenceTransformer(

                    cls._config.model_name,

                    device=device,

                    cache_folder=cls._config.cache_folder,

                    local_files_only=True

                )

            )
        except Exception:
            cls._model = (

                SentenceTransformer(

                    cls._config.model_name,

                    device=device,

                    cache_folder=cls._config.cache_folder,

                    local_files_only=False

                )

            )

        print(

            "Embedding model loaded successfully.\n"

        )

        return cls._model

    @classmethod
    def get_config(

        cls,
        model_key: str = DEFAULT_MODEL

    ):

        if cls._config is None:

            if model_key not in SUPPORTED_MODELS:
                raise ValueError(f"Embedding model '{model_key}' is not supported.")
            cls._config = SUPPORTED_MODELS[model_key]

        return cls._config