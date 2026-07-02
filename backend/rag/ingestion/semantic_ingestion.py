from rag.chunking.chunk_manager import (
    ChunkManager
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.metadata.semantic_metadata import (
    SemanticMetadata
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


class SemanticIngestion:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.chunk_manager = (

            ChunkManager()

        )

        self.embedding_manager = (

            EmbeddingManager(

                model_key=embedding_model

            )

        )

        self.vector_manager = (

            VectorManager()

        )

    # --------------------------------------------------
    # Ingest Memory
    # --------------------------------------------------

    def ingest(

        self,

        text: str,

        metadata: SemanticMetadata

    ) -> int:

        chunks = (

            self.chunk_manager.split(

                text=text,

                source="knowledge"

            )

        )

        if not chunks:

            return 0

        vectors = (

            self.embedding_manager.embed_document(

                chunks

            )

        )

        total_chunks = len(

            chunks

        )

        inserted = 0

        for chunk_index, (

            chunk,

            vector

        ) in enumerate(

            zip(

                chunks,

                vectors

            )

        ):

            metadata.chunk_index = (

                chunk_index

            )

            metadata.total_chunks = (

                total_chunks

            )

            point = (

                VectorPoint(

                    id=None,

                    embedding=vector,

                    payload={

                        "text": chunk,

                        **metadata.to_dict()

                    }

                )

            )

            self.vector_manager.insert(

                collection_key="semantic",

                point=point

            )

            inserted += 1

        return inserted