from typing import List
from typing import Optional

from rag.chunking.chunk_manager import (
    ChunkManager
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.metadata.metadata_service import (
    MetadataService
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


class ConversationIngestion:

    def __init__(

        self

    ):

        self.chunk_manager = (

            ChunkManager()

        )

        self.embedding_manager = (

            EmbeddingManager()

        )

        self.vector_manager = (

            VectorManager()

        )

    def ingest(

        self,

        text: str,

        conversation_id: int,

        user_id: int,

        message_id: int,

        role: str = "user",

        session_name: Optional[str] = None,

        topic: Optional[str] = None,

        domain: Optional[str] = None

    ) -> int:

        chunks = (

            self.chunk_manager.split(

                text=text,

                source="conversation"

            )

        )

        inserted = 0

        total_chunks = (

            len(

                chunks

            )

        )

        for index, chunk in enumerate(

            chunks

        ):

            embedding = (

                self.embedding_manager.embed_text(

                    text=chunk,

                    source_type="conversation",

                    source_id=str(

                        conversation_id

                    ),

                    user_id=user_id

                )

            )

            metadata = (

                MetadataService.create(

                    source="conversation",

                    user_id=user_id,

                    conversation_id=conversation_id,

                    message_id=message_id,

                    role=role,

                    session_name=session_name,

                    topic=topic,

                    domain=domain,

                    chunk_index=index,

                    total_chunks=total_chunks,

                    embedding_model=(

                        embedding.model_name

                    )

                )

            )

            point = (

                VectorPoint(

                    embedding=embedding.embedding,

                    payload={

                        "text": chunk,

                        "metadata": (

                            metadata.to_dict()

                        )

                    }

                )

            )

            if (

                self.vector_manager.insert(

                    "conversation",

                    point

                )

            ):

                inserted += 1

        return inserted

    def ingest_batch(

        self,

        conversations: List[dict]

    ) -> int:

        inserted = 0

        for conversation in conversations:

            inserted += (

                self.ingest(

                    **conversation

                )

            )

        return inserted