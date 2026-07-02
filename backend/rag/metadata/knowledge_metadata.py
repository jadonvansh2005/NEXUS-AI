from dataclasses import dataclass

from typing import Optional

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_constants import (
    SourceType,
    DocumentType,
    ImportanceLevel
)


@dataclass
class KnowledgeMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Knowledge Information
    # --------------------------------------------------

    knowledge_id: Optional[str] = None

    knowledge_base: Optional[str] = None

    category: Optional[str] = None

    subcategory: Optional[str] = None

    topic: Optional[str] = None

    # --------------------------------------------------
    # Document Information
    # --------------------------------------------------

    document_name: Optional[str] = None

    document_type: Optional[str] = None

    version: Optional[str] = None

    author: Optional[str] = None

    organization: Optional[str] = None

    # --------------------------------------------------
    # Chunk Information
    # --------------------------------------------------

    page_number: Optional[int] = None

    section: Optional[str] = None

    heading: Optional[str] = None

    chunk_index: Optional[int] = None

    total_chunks: Optional[int] = None

    start_char: Optional[int] = None

    end_char: Optional[int] = None

    file_path: Optional[str] = None

    folder_path: Optional[str] = None

    # --------------------------------------------------
    # Search & Retrieval
    # --------------------------------------------------

    language: Optional[str] = None

    tags: Optional[list[str]] = None

    keywords: Optional[list[str]] = None

    importance_score: float = (

        ImportanceLevel.NORMAL.value

    )

    confidence_score: float = 1.0

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    def __post_init__(

        self

    ) -> None:

        if not self.source:

            self.source = (

                SourceType.KNOWLEDGE.value

            )

    # --------------------------------------------------
    # Document Helpers
    # --------------------------------------------------

    def is_pdf(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.PDF.value

        )

    def is_docx(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.DOCX.value

        )

    def is_ppt(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.PPTX.value

        )

    def is_excel(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.XLSX.value

        )

    def is_csv(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.CSV.value

        )

    def is_text(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.TXT.value

        )

    # --------------------------------------------------
    # Knowledge Helpers
    # --------------------------------------------------

    def has_tags(

        self

    ) -> bool:

        return (

            self.tags is not None

            and

            len(

                self.tags

            ) > 0

        )

    def has_keywords(

        self

    ) -> bool:

        return (

            self.keywords is not None

            and

            len(

                self.keywords

            ) > 0

        )

    def has_heading(

        self

    ) -> bool:

        return (

            self.heading

            is not None

        )

    def has_section(

        self

    ) -> bool:

        return (

            self.section

            is not None

        )

    def has_page(

        self

    ) -> bool:

        return (

            self.page_number

            is not None

        )

    def is_chunked(

        self

    ) -> bool:

        return (

            self.total_chunks is not None

            and

            self.total_chunks > 1

        )

    def is_first_chunk(

        self

    ) -> bool:

        return (

            self.chunk_index == 0

        )

    def is_last_chunk(

        self

    ) -> bool:

        if (

            self.chunk_index is None

            or

            self.total_chunks is None

        ):

            return False

        return (

            self.chunk_index ==

            self.total_chunks - 1

        )