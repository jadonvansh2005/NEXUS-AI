from qdrant_client import (
    QdrantClient
)


class QdrantManager:

    _client = None

    @classmethod
    def get_client(

        cls

    ):

        if cls._client is None:

            cls._client = (

                QdrantClient(

                    host="127.0.0.1",

                    port=6333

                )

            )

        return cls._client

    @classmethod
    def health_check(

        cls

    ):

        client = (

            cls.get_client()

        )

        return client.get_collections()