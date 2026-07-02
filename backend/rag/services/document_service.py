from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rag.ingestion.document_ingestion import (
    DocumentIngestion
)

from rag.retrieval.document_retriever import (
    DocumentRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class DocumentService:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.ingestion = (

            DocumentIngestion(

                embedding_model=embedding_model

            )

        )

        self.retriever = (

            DocumentRetriever()

        )

    # ------------------------------------------
    # Ingest Document
    # ------------------------------------------

    def ingest(

        self,

        file_path: str,

        project: Optional[str] = None,

        user_id: Optional[int] = None

    ) -> int:

        return (

            self.ingestion.ingest(

                file_path=file_path,

                project=project,

                user_id=user_id

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