from rag.pipelines.knowledge_pipeline import (
    KnowledgePipeline
)

from rag.metadata.knowledge_metadata import (
    KnowledgeMetadata
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_knowledge_pipeline():

    pipeline = (

        KnowledgePipeline()

    )

    vector_manager = (

        VectorManager()

    )

    metadata = (

        KnowledgeMetadata(

            user_id=1,

            project="DeepShield",

            source="knowledge"

        )

    )

    inserted = (

        pipeline.index(

            file_path=r"D:\UPSS\backend\tests\data\AI_based_Operating-system.pdf",

            metadata=metadata

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    results = (

        pipeline.retrieve(

            query="What is the problem statement?",

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

            query="What is the problem statement?",

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

            "knowledge"

        )

    )

    print(

        "\n✅ Knowledge Pipeline Passed"

    )


if __name__ == "__main__":

    test_knowledge_pipeline()