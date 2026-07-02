from rag.ingestion.conversation_ingestion import (
    ConversationIngestion
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_conversation_ingestion():

    ingestion = (

        ConversationIngestion()

    )

    vector_manager = (

        VectorManager()

    )

    text = (

        "Hello, my name is Vansh. "
        "I am building the UPSS project. "
        "This project uses RAG, Qdrant, FastAPI and BGE-M3 embeddings."
    )

    inserted = (

        ingestion.ingest(

            text=text,

            conversation_id=1,

            user_id=1,

            message_id=1,

            role="user",

            session_name="Integration Test",

            topic="RAG Testing",

            domain="general"

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    print(

        "\nConversation Count:",

        vector_manager.count_vectors(

            "conversation"

        )

    )

    print(

        "\n✅ Conversation Ingestion Passed"

    )


if __name__ == "__main__":

    test_conversation_ingestion()