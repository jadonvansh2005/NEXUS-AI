from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.semantic_service import (
    SemanticService
)


class SemanticPipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            SemanticService()

        )