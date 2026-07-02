from rag.retrieval.base_retrieval import (
    BaseRetrieval
)


class DocumentRetriever(

    BaseRetrieval

):

    def __init__(

        self

    ):

        super().__init__(

            collection_key="document"

        )