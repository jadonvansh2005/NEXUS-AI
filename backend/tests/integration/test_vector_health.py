from rag.vector_store.vector_manager import (
    VectorManager
)


def test_vector_health():

    vector_manager = (

        VectorManager()

    )

    result = (

        vector_manager.health_check()

    )

    print(

        "\nQdrant Health:",

        result

    )

    assert result is True

    print(

        "\n✅ Qdrant Health Check Passed"

    )


if __name__ == "__main__":

    test_vector_health()