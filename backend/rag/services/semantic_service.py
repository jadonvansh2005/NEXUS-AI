from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rag.ingestion.semantic_ingestion import (
    SemanticIngestion
)

from rag.metadata.semantic_metadata import (
    SemanticMetadata
)

from rag.retrieval.semantic_retriever import (
    SemanticRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class SemanticService:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.ingestion = (

            SemanticIngestion(

                embedding_model=embedding_model

            )

        )

        self.retriever = (

            SemanticRetriever()

        )

    # ------------------------------------------
    # Ingest
    # ------------------------------------------

    def ingest(

        self,

        text: str,

        metadata: SemanticMetadata

    ) -> int:

        return (

            self.ingestion.ingest(

                text=text,

                metadata=metadata

            )

        )

    # ------------------------------------------
    # Search
    # ------------------------------------------

    def search(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[
            float
        ] = None,

        filters: Optional[
            Dict[str, Any]
        ] = None

    ) -> List[SearchResult]:

        return (

            self.retriever.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters=filters

            )

        )