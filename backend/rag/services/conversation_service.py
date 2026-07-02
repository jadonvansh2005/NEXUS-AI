from typing import List
from typing import Optional

from rag.ingestion.conversation_ingestion import (
    ConversationIngestion
)

from rag.retrieval.conversation_retriever import (
    ConversationRetriever
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class ConversationService:

    def __init__(

        self

    ):

        self.ingestion = (

            ConversationIngestion()

        )

        self.retriever = (

            ConversationRetriever()

        )

    # -----------------------------------------
    # Store Conversation
    # -----------------------------------------

    def ingest(

        self,

        **kwargs

    ) -> int:

        return (

            self.ingestion.ingest(

                **kwargs

            )

        )

    # -----------------------------------------
    # Retrieve Conversation
    # -----------------------------------------

    def search(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[float] = None,

        filters: Optional[dict] = None

    ) -> List[SearchResult]:

        return (

            self.retriever.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters=filters

            )

        )

    # -----------------------------------------
    # User Conversation
    # -----------------------------------------

    def search_user(

        self,

        user_id: int,

        query: str,

        limit: int = 5

    ) -> List[SearchResult]:

        return (

            self.retriever.search(

                query=query,

                limit=limit,

                filters={

                    "user_id": user_id

                }

            )

        )

    # -----------------------------------------
    # Conversation History
    # -----------------------------------------

    def search_conversation(

        self,

        conversation_id: int,

        query: str,

        limit: int = 5

    ) -> List[SearchResult]:

        return (

            self.retriever.search(

                query=query,

                limit=limit,

                filters={

                    "conversation_id": conversation_id

                }

            )

        )

    # -----------------------------------------
    # User + Conversation
    # -----------------------------------------

    def search_user_conversation(

        self,

        user_id: int,

        conversation_id: int,

        query: str,

        limit: int = 5

    ) -> List[SearchResult]:

        return (

            self.retriever.search(

                query=query,


                filters={

                    "user_id": user_id,

                    "conversation_id": conversation_id

                },

                limit=limit

            )

        )