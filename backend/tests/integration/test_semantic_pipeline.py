from rag.pipelines.semantic_pipeline import (
    SemanticPipeline
)

from rag.metadata.semantic_metadata import (
    SemanticMetadata
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_semantic_pipeline():

    pipeline = (

        SemanticPipeline()

    )

    vector_manager = (

        VectorManager()

    )

    metadata = (

        SemanticMetadata(

            user_id=1,

            project="UPSS",

            memory_type="fact",

            category="AI",

            subcategory="RAG"

        )

    )

    inserted = (

        pipeline.index(

            text=(
                "UPSS uses Qdrant as the vector database. "
                "BAAI BGE-M3 is used for embeddings. "
                "FastAPI is used as backend."
            ),

            metadata=metadata

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    results = (

        pipeline.retrieve(

            query="Which vector database is used?",

            limit=5

        )

    )

    print("\nRetrieved Results\n")

    for i, result in enumerate(

        results,

        start=1

    ):

        print(

            f"{i}. Score: {result.score}"

        )

        print(

            result.payload

        )

        print()

    output = (

        pipeline.run(

            query="Which vector database is used?",

            system_prompt=(
                "Answer only from retrieved context."
            )

        )

    )

    print(

        "\nPipeline Output\n"

    )

    print(

        output["prompt"]

    )

    print(

        f"\nRetrieved: {output['count']}"

    )

    print(

        "\nVector Count:",

        vector_manager.count_vectors(

            "semantic"

        )

    )

    print(

        "\n✅ Semantic Pipeline Passed"

    )


if __name__ == "__main__":

    test_semantic_pipeline()