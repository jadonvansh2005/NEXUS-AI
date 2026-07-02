from abc import ABC

from typing import Dict
from typing import List
from typing import Optional
from typing import Any

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class BaseRetrieval(

    ABC

):

    def __init__(

        self,

        collection_key: str

    ):

        self.collection_key = (

            collection_key

        )

        self.embedding_manager = (

            EmbeddingManager()

        )

        self.vector_manager = (

            VectorManager()

        )

    # --------------------------------------------------
    # Generic Search
    # --------------------------------------------------

    def search(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[float] = None,

        filters: Optional[

            Dict[str, Any]

        ] = None

    ) -> List[SearchResult]:

        embedding = (

            self.embedding_manager.embed_query(

                query

            )

        )

        return (

            self.vector_manager.search(

                collection_key=self.collection_key,

                query_vector=embedding,

                limit=limit,

                score_threshold=score_threshold,

                filters=filters

            )

        )

    # --------------------------------------------------
    # Convenience Methods
    # --------------------------------------------------

    def search_by_user(

        self,

        query: str,

        user_id: int,

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters={

                    "user_id": user_id

                }

            )

        )

    def search_by_source(

        self,

        query: str,

        source_id: str,

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters={

                    "source_id": source_id

                }

            )

        )

    def search_with_filters(

        self,

        query: str,

        filters: Dict[str, Any],

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                filters=filters,

                limit=limit,

                score_threshold=score_threshold

            )

        )