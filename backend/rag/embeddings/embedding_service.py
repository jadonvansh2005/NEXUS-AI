from datetime import (
    datetime
)

from typing import (
    List,
    Dict,
    Any,
    Optional
)

from rag.embeddings.embedding_factory import (
    EmbeddingFactory
)

from rag.embeddings.embedding_models import (
    DEFAULT_MODEL,
    SUPPORTED_MODELS
)

from rag.embeddings.embedding_schema import (
    EmbeddingResult
)


class EmbeddingService:

    def __init__(

        self,

        model_key: str = DEFAULT_MODEL

    ):

        self.model_key = model_key

        self._model = None

        self.config = (

            SUPPORTED_MODELS[

                model_key

            ]

        )

    @property
    def model(self):
        if self._model is None:
            self._model = (
                EmbeddingFactory.get_model(
                    self.model_key
                )
            )
        return self._model

    def embed_text(

        self,

        text: str,

        source_type: str = "general",

        source_id: Optional[str] = None,

        user_id: Optional[int] = None,

        metadata: Optional[

            Dict[str, Any]

        ] = None

    ) -> EmbeddingResult:

        if metadata is None:

            metadata = {}

        vector = (

            self.model.encode(

                text,

                normalize_embeddings=True

            )

            .tolist()

        )

        return EmbeddingResult(

            text=text,

            embedding=vector,

            model_name=self.config.model_name,

            dimension=self.config.dimension,

            source_type=source_type,

            source_id=source_id,

            user_id=user_id,

            metadata=metadata,

            created_at=datetime.utcnow()

        )

    def embed_batch(

        self,

        texts: List[str]

    ) -> List[List[float]]:

        vectors = (

            self.model.encode(

                texts,

                normalize_embeddings=True

            )

        )

        return vectors.tolist()

    def embed_query(

        self,

        query: str

    ) -> List[float]:

        return (

            self.model.encode(

                query,

                normalize_embeddings=True

            )

            .tolist()

        )

    def embed_document(

        self,

        chunks: List[str]

    ) -> List[List[float]]:

        vectors = (

            self.model.encode(

                chunks,

                normalize_embeddings=True

            )

        )

        return vectors.tolist()