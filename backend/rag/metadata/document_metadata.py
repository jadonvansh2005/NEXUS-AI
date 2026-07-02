from dataclasses import dataclass

from typing import Optional

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_constants import (
    DocumentType,
    SourceType,
    ImportanceLevel
)


@dataclass
class DocumentMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Document Information
    # --------------------------------------------------

    document_id: Optional[str] = None

    document_name: Optional[str] = None

    document_type: Optional[str] = None

    document_version: Optional[str] = None

    # --------------------------------------------------
    # File Information
    # --------------------------------------------------

    file_size: Optional[int] = None

    file_extension: Optional[str] = None

    checksum: Optional[str] = None

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    page_number: Optional[int] = None

    chapter: Optional[str] = None

    section: Optional[str] = None

    heading: Optional[str] = None

    # --------------------------------------------------
    # Chunk Information
    # --------------------------------------------------

    chunk_index: Optional[int] = None

    total_chunks: Optional[int] = None

    start_char: Optional[int] = None

    end_char: Optional[int] = None

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    language: Optional[str] = None

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

                SourceType.DOCUMENT.value

            )

    # --------------------------------------------------
    # Utility
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

    def is_markdown(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.MARKDOWN.value

        )

    def has_chunks(

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

    def has_page_number(

        self

    ) -> bool:

        return (

            self.page_number

            is not None

        )

    def has_heading(

        self

    ) -> bool:

        return (

            self.heading

            is not None

        )

    def has_checksum(

        self

    ) -> bool:

        return (

            self.checksum

            is not None

        )