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
class CodeMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Repository Information
    # --------------------------------------------------

    repository: Optional[str] = None

    branch: Optional[str] = None

    commit_hash: Optional[str] = None

    # --------------------------------------------------
    # File Information
    # --------------------------------------------------

    file_name: Optional[str] = None

    file_path: Optional[str] = None

    language: Optional[str] = None

    document_type: Optional[str] = None

    # --------------------------------------------------
    # Code Structure
    # --------------------------------------------------

    module: Optional[str] = None

    class_name: Optional[str] = None

    function_name: Optional[str] = None

    method_name: Optional[str] = None

    # --------------------------------------------------
    # chunk information
    # --------------------------------------------------

    page_number: Optional[int] = None

    chunk_index: Optional[int] = None

    total_chunks: Optional[int] = None

    file_path: Optional[str] = None

    folder_path: Optional[str] = None

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    line_start: Optional[int] = None

    line_end: Optional[int] = None

    # --------------------------------------------------
    # Code Properties
    # --------------------------------------------------

    framework: Optional[str] = None

    package: Optional[str] = None

    imports: Optional[list[str]] = None

    dependencies: Optional[list[str]] = None

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

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

                SourceType.CODE.value

            )

    # --------------------------------------------------
    # File Helpers
    # --------------------------------------------------

    def is_python(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.PYTHON.value

        )

    def is_javascript(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.JAVASCRIPT.value

        )

    def is_typescript(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.TYPESCRIPT.value

        )

    def is_java(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.JAVA.value

        )

    def is_cpp(

        self

    ) -> bool:

        return (

            self.document_type ==

            DocumentType.CPP.value

        )

    # --------------------------------------------------
    # Code Helpers
    # --------------------------------------------------

    def has_class(

        self

    ) -> bool:

        return (

            self.class_name

            is not None

        )

    def has_function(

        self

    ) -> bool:

        return (

            self.function_name

            is not None

        )

    def has_method(

        self

    ) -> bool:

        return (

            self.method_name

            is not None

        )

    def has_imports(

        self

    ) -> bool:

        return (

            self.imports is not None

            and

            len(

                self.imports

            ) > 0

        )

    def has_dependencies(

        self

    ) -> bool:

        return (

            self.dependencies is not None

            and

            len(

                self.dependencies

            ) > 0

        )

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

    def has_line_numbers(

        self

    ) -> bool:

        return (

            self.line_start is not None

            and

            self.line_end is not None

        )