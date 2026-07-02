from typing import List
from typing import Dict
from typing import Any
from typing import Optional

from rag.embeddings.embedding_service import (
    EmbeddingService
)

from rag.embeddings.cache_manager import (
    EmbeddingCache
)

from rag.embeddings.embedding_schema import (
    EmbeddingResult
)


class EmbeddingManager:

    def __init__(

        self,

        model_key: str = "bge_m3"

    ):

        self.service = (

            EmbeddingService(

                model_key=model_key

            )

        )

        self.cache = (

            EmbeddingCache()

        )

        self.model_key = (

            model_key

        )

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

        cached_embedding = (

            self.cache.get(

                model_name=self.model_key,

                text=text

            )

        )

        if cached_embedding is not None:

            result = self.service.embed_text(

                text=text,

                source_type=source_type,

                source_id=source_id,

                user_id=user_id,

                metadata=metadata

            )

            result.embedding = (

                cached_embedding

            )

            return result

        result = (

            self.service.embed_text(

                text=text,

                source_type=source_type,

                source_id=source_id,

                user_id=user_id,

                metadata=metadata

            )

        )

        self.cache.set(

            model_name=self.model_key,

            text=text,

            embedding=result.embedding

        )

        return result

    def embed_query(

        self,

        query: str

    ) -> List[float]:

        return (

            self.service.embed_query(

                query

            )

        )

    def embed_document(

        self,

        chunks: List[str]

    ) -> List[List[float]]:

        return (

            self.service.embed_document(

                chunks

            )

        )

    def embed_batch(

        self,

        texts: List[str]

    ) -> List[List[float]]:

        return (

            self.service.embed_batch(

                texts

            )

        )