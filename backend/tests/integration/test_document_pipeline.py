from rag.pipelines.document_pipeline import (
    DocumentPipeline
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_document_pipeline():

    pipeline = (

        DocumentPipeline()

    )

    vector_manager = (

        VectorManager()

    )

    inserted = (

        pipeline.index(

            file_path=r"D:\UPSS\backend\tests\data\Vansh_macro-report.pdf",

            project="DeepShield",

            user_id=1

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    results = (

        pipeline.retrieve(

            query="Which model is used for audio deepfake detection?",

            limit=5

        )

    )

    print("\nRetrieved Results\n")

    for i, result in enumerate(results, 1):

        print(f"{i}. Score: {result.score}")

        print(result.payload)

        print()

    output = (

        pipeline.run(

            query="Which model is used for audio deepfake detection?",

            system_prompt=(

                "Answer only from retrieved context."

            )

        )

    )

    print("\nPipeline Output\n")

    print(output["prompt"])

    print(f"\nRetrieved: {output['count']}")

    print(

        "\nVector Count:",

        vector_manager.count_vectors(

            "document"

        )

    )

    print(

        "\n✅ Document Pipeline Passed"

    )


if __name__ == "__main__":

    test_document_pipeline()