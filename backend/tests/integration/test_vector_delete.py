from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


def test_vector_delete():

    embedding_manager = (

        EmbeddingManager()

    )

    vector_manager = (

        VectorManager()

    )

    text = (

        "Delete Test Vector"

    )

    embedding = (

        embedding_manager.embed_text(

            text=text,

            source_type="conversation"

        )

    )

    point = (

        VectorPoint(

            embedding=embedding.embedding,

            payload={

                "type": "conversation",

                "user_id": 999,

                "text": text

            }

        )

    )

    inserted = (

        vector_manager.insert(

            collection_key="conversation",

            point=point

        )

    )

    print(

        f"\nInsert Result: {inserted}"

    )

    assert inserted is True

    query_vector = (

        embedding_manager.embed_query(

            text

        )

    )

    results = (

        vector_manager.search(

            collection_key="conversation",

            query_vector=query_vector,

            limit=1

        )

    )

    assert len(

        results

    ) > 0

    point_id = (

        results[0].id

    )

    print(

        f"Point ID: {point_id}"

    )

    deleted = (

        vector_manager.delete(

            collection_key="conversation",

            point_id=point_id

        )

    )

    print(

        f"Delete Result: {deleted}"

    )

    assert deleted is True

    after_delete = (

        vector_manager.get(

            collection_key="conversation",

            point_id=point_id

        )

    )

    assert after_delete is None

    print(

        "\n✅ Vector Deleted Successfully"

    )


if __name__ == "__main__":

    test_vector_delete()