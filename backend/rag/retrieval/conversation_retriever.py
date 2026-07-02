from rag.retrieval.base_retrieval import (
    BaseRetrieval
)


class ConversationRetriever(

    BaseRetrieval

):

    def __init__(

        self

    ):

        super().__init__(

            collection_key="conversation"

        )