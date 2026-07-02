from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)


def test_vector_search():

    embedding_manager = (

        EmbeddingManager()

    )

    vector_manager = (

        VectorManager()

    )

    query = (

        "Hello UPSS"

    )

    query_embedding = (

        embedding_manager.embed_text(

            text=query

        )

    )

    results = (

        vector_manager.search(

            collection_key="conversation",

            query_vector=query_embedding.embedding,

            limit=5

        )

    )

    print("\nSearch Results\n")

    print(results)


if __name__ == "__main__":

    test_vector_search()