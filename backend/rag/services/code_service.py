from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rag.ingestion.code_ingestion import (
    CodeIngestion
)

from rag.metadata.code_metadata import (
    CodeMetadata
)

from rag.retrieval.code_retriever import (
    CodeRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class CodeService:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.ingestion = (

            CodeIngestion(

                embedding_model=embedding_model

            )

        )

        self.retriever = (

            CodeRetriever()

        )

    # ------------------------------------------
    # Ingest
    # ------------------------------------------

    def ingest(

        self,

        file_path: str,

        metadata: CodeMetadata

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