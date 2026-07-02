from rag.pipelines.conversation_pipeline import (
    ConversationPipeline
)


class RAGPipeline:

    def __init__(

        self

    ):

        self.conversation = (

            ConversationPipeline()

        )

    def run(

        self,

        query: str,

        **kwargs

    ):

        return (

            self.conversation.run(

                query=query,

                **kwargs

            )

        )