from rag.chunking.chunk_manager import (
    ChunkManager
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.loaders.loader_factory import (
    LoaderFactory
)

from rag.preprocessing.cleaner import (
    Cleaner
)

from rag.preprocessing.document_parser import (
    DocumentParser
)

from rag.preprocessing.metadata_builder import (
    MetadataBuilder
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


class DocumentIngestion:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.loader_factory = (

            LoaderFactory()

        )

        self.chunk_manager = (

            ChunkManager()

        )

        self.embedding_manager = (

            EmbeddingManager(

                model_key=embedding_model

            )

        )

        self.vector_store = (

            VectorManager()

        )

    # --------------------------------------------------
    # Ingest
    # --------------------------------------------------

    def ingest(

        self,

        file_path: str,

        project: str | None = None,

        user_id: int | None = None

    ) -> int:

        loader = (

            self.loader_factory.create(

                file_path

            )

        )

        document = (

            loader.load()

        )

        document = (

            Cleaner.clean(

                document

            )

        )

        parsed_document = (

            DocumentParser.parse(

                document

            )

        )

        inserted = 0

        for page in parsed_document.pages:

            chunks = (

                self.chunk_manager.split(

                    text=page.text,

                    source="document"

                )

            )

            if not chunks:

                continue

            vectors = (

                self.embedding_manager.embed_document(

                    chunks

                )

            )

            total_chunks = len(

                chunks

            )

            for chunk_index, (

                chunk,

                vector

            ) in enumerate(

                zip(

                    chunks,

                    vectors

                )

            ):

                metadata = (

                    MetadataBuilder.build(

                        document=parsed_document,

                        page=page,

                        chunk_index=chunk_index,

                        total_chunks=total_chunks,

                        user_id=user_id,

                        project=project

                    )

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

                self.vector_store.insert(

                    collection_key="document",

                    point=point

                )

                inserted += 1

        return inserted