from rag.vector_store.vector_manager import (
    VectorManager
)


def test_vector_collection():

    vector_manager = (

        VectorManager()

    )

    collections = [

        "conversation",
        "document",
        "semantic",
        "project",
        "knowledge",
        "code"

    ]

    print("\nCreating Collections\n")

    for collection in collections:

        created = (

            vector_manager.create_collection(

                collection_key=collection

            )

        )

        print(

            f"{collection}: {created}"

        )

        assert created is True

    print("\nChecking Collections\n")

    for collection in collections:

        exists = (

            vector_manager.collection_exists(

                collection

            )

        )

        print(

            f"{collection}: {exists}"

        )

        assert exists is True

    print("\nCollection Information\n")

    for collection in collections:

        info = (

            vector_manager.collection_info(

                collection

            )

        )

        print(info)

    print("\nVector Counts\n")

    for collection in collections:

        count = (

            vector_manager.count_vectors(

                collection

            )

        )

        print(

            f"{collection}: {count}"

        )

    print("\nAvailable Collections\n")

    print(

        vector_manager.list_collections()

    )

    print(

        "\n✅ Collection Test Passed"

    )


if __name__ == "__main__":

    test_vector_collection()