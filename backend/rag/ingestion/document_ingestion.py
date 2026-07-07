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

    _latest_uploads = {}

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
        print(f"\n[Ingestion] Starting ingestion for file: {file_path}", flush=True)
        
        loader = (
            self.loader_factory.create(
                file_path
            )
        )
        print("[Ingestion] Created document loader instance. Loading file...", flush=True)

        document = (
            loader.load()
        )
        print(f"[Ingestion] File loaded. Size: {self.chunk_manager.split.__code__.co_consts} bytes. Cleaning text...", flush=True)

        document = (
            Cleaner.clean(
                document
            )
        )
        print("[Ingestion] Text clean completed. Parsing document pages...", flush=True)

        parsed_document = (
            DocumentParser.parse(
                document
            )
        )
        total_pages = len(parsed_document.pages)
        print(f"[Ingestion] Document parsed. Total pages: {total_pages}", flush=True)

        # Track the latest upload id for this user
        latest_doc_id = None
        inserted = 0

        for page_index, page in enumerate(parsed_document.pages):
            print(f"[Ingestion] Processing page {page_index + 1}/{total_pages}...", flush=True)
            
            chunks = (
                self.chunk_manager.split(
                    text=page.text,
                    source="document"
                )
            )

            if not chunks:
                print(f"[Ingestion] No chunks generated for page {page_index + 1}. Skipping.", flush=True)
                continue

            print(f"[Ingestion] Generated {len(chunks)} chunks on page {page_index + 1}. Generating model embeddings...", flush=True)
            vectors = (
                self.embedding_manager.embed_document(
                    chunks
                )
            )
            print(f"[Ingestion] Model embeddings generated. Inserting points into Qdrant collection 'document'...", flush=True)

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
                if latest_doc_id is None:
                    latest_doc_id = metadata.document_id

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
            print(f"[Ingestion] Page {page_index + 1}/{total_pages} processing complete. Inserted {inserted} total vectors so far.", flush=True)

        print(f"[Ingestion] Ingestion finished! Total chunks inserted: {inserted}\n", flush=True)
        if user_id is not None and latest_doc_id is not None:
            from rag.retrieval.base_retrieval import BaseRetrieval
            BaseRetrieval._latest_uploads[(user_id, "document")] = latest_doc_id
            print(f"[Ingestion] Cached latest upload document_id for user {user_id}: {latest_doc_id}", flush=True)
        return inserted