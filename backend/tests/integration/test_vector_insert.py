from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


def test_insert_vector():

    embedding_manager = (

        EmbeddingManager()

    )

    vector_manager = (

        VectorManager()

    )

    text = "Hello UPSS"

    embedding = (

        embedding_manager.embed_text(

            text

        ).embedding

    )

    point = VectorPoint(

        embedding=embedding,

        payload={

            "type": "conversation",

            "user_id": 1,

            "text": text

        }

    )

    result = (

        vector_manager.insert(

            "conversation",

            point

        )

    )

    print(

        "Insert Result:",

        result

    )

    assert result is True

    print(

        "\n✅ Vector Inserted Successfully"

    )


if __name__ == "__main__":

    test_insert_vector()