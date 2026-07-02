from rag.pipelines.conversation_pipeline import (
    ConversationPipeline
)


def test_conversation_pipeline():

    pipeline = (

        ConversationPipeline()

    )

    # --------------------------------------------------
    # Index Conversation
    # --------------------------------------------------

    inserted = (

        pipeline.index(

            text=(
                "My name is Vansh. "
                "I am building the UPSS project. "
                "The project uses FastAPI, "
                "Qdrant and BGE-M3."
            ),

            conversation_id=100,

            user_id=1,

            message_id=1,

            role="user",

            session_name="Integration Test",

            topic="UPSS",

            domain="general"

        )

    )

    print(

        "\nInserted:",

        inserted

    )

    assert inserted > 0

    # --------------------------------------------------
    # Retrieve
    # --------------------------------------------------

    retrieved = (

        pipeline.retrieve(

            query="Which vector database is used?",

            limit=3

        )

    )

    print(

        "\nRetrieved Results\n"

    )

    for index, result in enumerate(

        retrieved,

        start=1

    ):

        print(

            f"{index}.",

            result.score

        )

        print(

            result.payload

        )

        print()

    assert len(

        retrieved

    ) > 0

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    response = (

        pipeline.run(

            query="Which vector database is used?"

        )

    )

    print(

        "\nPipeline Output\n"

    )

    print(

        response["prompt"]

    )

    print()

    print(

        "Retrieved:",

        response["count"]

    )

    assert (

        response["count"] > 0

    )

    print(

        "\n✅ Conversation Pipeline Passed"

    )


if __name__ == "__main__":

    test_conversation_pipeline()