from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.conversation_service import (
    ConversationService
)


class ConversationPipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            ConversationService()

        )