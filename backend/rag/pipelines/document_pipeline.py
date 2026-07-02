from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.document_service import (
    DocumentService
)


class DocumentPipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            DocumentService()

        )