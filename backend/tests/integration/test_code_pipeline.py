from rag.pipelines.code_pipeline import (
    CodePipeline
)

from rag.metadata.code_metadata import (
    CodeMetadata
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_code_pipeline():

    pipeline = (

        CodePipeline()

    )

    vector_manager = (

        VectorManager()

    )

    metadata = (

        CodeMetadata(

            user_id=1,

            project="UPSS",

            language="python",

            source="code",

            module="rag",

            document_type="python"

        )

    )

    inserted = (

        pipeline.index(

            file_path=r"D:\UPSS\backend\rag\ingestion\document_ingestion.py",

            metadata=metadata

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    results = (

        pipeline.retrieve(

            query="How are document embeddings generated?",

            limit=5

        )

    )

    print(

        "\nRetrieved Results\n"

    )

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

            query="How are document embeddings generated?",

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

            "code"

        )

    )

    print(

        "\n✅ Code Pipeline Passed"

    )


if __name__ == "__main__":

    test_code_pipeline()