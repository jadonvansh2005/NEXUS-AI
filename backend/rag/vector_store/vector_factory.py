from rag.vector_store.qdrant_manager import (
    QdrantManager
)


class VectorFactory:

    @staticmethod
    def get_client():

        return (

            QdrantManager.get_client()

        )