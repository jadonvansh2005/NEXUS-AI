from qdrant_client import QdrantClient

from app.settings import settings


class QdrantManager:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = QdrantClient(

                url=settings.QDRANT_URL,

                api_key=settings.QDRANT_API_KEY,

                timeout=60

            )

        return cls._client

    @classmethod
    def health_check(cls):

        client = cls.get_client()

        return client.get_collections()