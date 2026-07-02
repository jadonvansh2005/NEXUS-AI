from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.knowledge_service import (
    KnowledgeService
)


class KnowledgePipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            KnowledgeService()

        )