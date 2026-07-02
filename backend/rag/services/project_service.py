from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rag.ingestion.project_ingestion import (
    ProjectIngestion
)

from rag.metadata.project_metadata import (
    ProjectMetadata
)

from rag.retrieval.project_retriever import (
    ProjectRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class ProjectService:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.ingestion = (

            ProjectIngestion(

                embedding_model=embedding_model

            )

        )

        self.retriever = (

            ProjectRetriever()

        )

    # ------------------------------------------
    # Ingest
    # ------------------------------------------

    def ingest(

        self,

        root_directory: str,

        metadata: ProjectMetadata

    ) -> int:

        return (

            self.ingestion.ingest(

                root_directory=root_directory,

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