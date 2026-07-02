from rag.chunking.chunk_manager import (
    ChunkManager
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.loaders.loader_factory import (
    LoaderFactory
)

from rag.metadata.project_metadata import (
    ProjectMetadata
)

from rag.preprocessing.cleaner import (
    Cleaner
)

from rag.preprocessing.document_parser import (
    DocumentParser
)

from rag.project.project_scanner import (
    ProjectScanner
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)

from pathlib import Path


class ProjectIngestion:

    def __init__(

        self,

        embedding_model: str = "bge_m3"

    ):

        self.scanner = (

            ProjectScanner()

        )

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

        self.vector_manager = (

            VectorManager()

        )

    # --------------------------------------------------
    # Ingest Complete Project
    # --------------------------------------------------

    def ingest(

        self,

        root_directory: str,

        metadata: ProjectMetadata

    ) -> int:

        project_files = (

            self.scanner.scan(

                root_directory

            )

        )

        total_inserted = 0

        for file_path in project_files:

            try:

                inserted = (

                    self._ingest_file(

                        file_path=str(

                            file_path

                        ),

                        metadata=metadata

                    )

                )

                total_inserted += (

                    inserted

                )

            except Exception as error:

                print(

                    "[ProjectIngestion]",

                    file_path,

                    error

                )

                continue

        return (

            total_inserted

        )

    # --------------------------------------------------
    # Ingest Single File
    # --------------------------------------------------

    def _ingest_file(

        self,

        file_path: str,

        metadata: ProjectMetadata

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

            inserted += (

                self._ingest_page(

                    page=page,

                    document=parsed_document,

                    metadata=metadata,

                    file_path=file_path

                )

            )

        return (

            inserted

        )
    

    # --------------------------------------------------
    # Ingest Single Page
    # --------------------------------------------------

    def _ingest_page(

        self,

        page,

        document,

        metadata: ProjectMetadata,

        file_path: str

    ) -> int:

        chunks = (

            self.chunk_manager.split(

                text=page.text,

                source="project"

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

            metadata.file_path = (

                file_path

            )

            metadata.folder_path = (

                str(

                    Path(

                        file_path

                    ).parent

                )

            )

            metadata.chunk_index = (

                chunk_index

            )

            metadata.total_chunks = (

                total_chunks

            )

            metadata.page_number = (

                page.page_number

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

                collection_key="project",

                point=point

            )

            inserted += 1

        return (

            inserted

        )