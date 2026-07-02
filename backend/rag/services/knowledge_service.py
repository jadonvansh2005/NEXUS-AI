from typing import Dict
from typing import List
from typing import Optional

from rag.ingestion.knowledge_ingestion import (
    KnowledgeIngestion
)

from rag.metadata.knowledge_metadata import (
    KnowledgeMetadata
)

from rag.retrieval.knowledge_retriever import (
    KnowledgeRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class KnowledgeService:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.ingestion = (

            KnowledgeIngestion(

                embedding_model=embedding_model

            )

        )

        self.retriever = (

            KnowledgeRetriever()

        )

    # ------------------------------------------
    # Ingest
    # ------------------------------------------

    def ingest(

        self,

        file_path: str,

        metadata: KnowledgeMetadata

    ) -> int:

        return (

            self.ingestion.ingest(

                file_path=file_path,

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
            Dict[str, str]
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