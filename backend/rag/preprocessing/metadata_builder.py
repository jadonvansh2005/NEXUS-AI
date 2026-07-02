from typing import Optional

from rag.metadata.document_metadata import (
    DocumentMetadata
)

from rag.metadata.metadata_factory import (
    MetadataFactory
)

from rag.metadata.metadata_constants import (
    SourceType
)

from rag.preprocessing.preprocessing_schema import (
    ParsedDocument,
    ParsedPage
)


class MetadataBuilder:

    @staticmethod
    def build(

        document: ParsedDocument,

        page: ParsedPage,

        chunk_index: int,

        total_chunks: int,

        user_id: Optional[int] = None,

        project: Optional[str] = None

    ) -> DocumentMetadata:

        metadata = MetadataFactory.document(

            user_id=user_id,

            source=SourceType.DOCUMENT.value,

            project=project,

            
            document_name=document.filename,

            document_type=document.document_type,

            page_number=page.page_number,

            chunk_index=chunk_index,

            total_chunks=total_chunks,

            # source_path=document.source_path,

            file_size=document.metadata.get(

                "filesize"

            ),

            checksum=document.metadata.get(

                "checksum"

            )

        )

        return metadata