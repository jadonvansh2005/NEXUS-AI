from rag.pipelines.project_pipeline import (
    ProjectPipeline
)

from rag.metadata.project_metadata import (
    ProjectMetadata
)

from rag.vector_store.vector_manager import (
    VectorManager
)


def test_project_pipeline():

    pipeline = (

        ProjectPipeline()

    )

    vector_manager = (

        VectorManager()

    )

    metadata = (

        ProjectMetadata(

            user_id=1,

            project_name="AI Operating System",

            module="rag",

            architecture_layer="backend",

            source="project"

        )

    )

    inserted = (

        pipeline.index(

            root_directory=r"D:\UPSS\backend\rag",

            metadata=metadata

        )

    )

    print(

        f"\nInserted Chunks: {inserted}"

    )

    assert inserted > 0

    results = (

        pipeline.retrieve(

            query="Where is VectorManager implemented?",

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

            query="Where is VectorManager implemented?",

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

            "project"

        )

    )

    print(

        "\n✅ Project Pipeline Passed"

    )


if __name__ == "__main__":

    test_project_pipeline()