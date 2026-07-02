from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class LoadedDocument:

    # ------------------------------------------
    # Core Document
    # ------------------------------------------

    text: str

    document_type: str

    source_path: str

    filename: str

    # ------------------------------------------
    # Document Information
    # ------------------------------------------

    metadata: Dict[
        str,
        Any
    ] = field(

        default_factory=dict

    )

    # ------------------------------------------
    # Page Information
    # ------------------------------------------

    page_count: Optional[
        int
    ] = None

    pages: Optional[
        List[str]
    ] = None

    # ------------------------------------------
    # File Information
    # ------------------------------------------

    encoding: Optional[
        str
    ] = None

    language: Optional[
        str
    ] = None

    checksum: Optional[
        str
    ] = None

    file_size: Optional[
        int
    ] = None

    # ------------------------------------------
    # Extra Information
    # ------------------------------------------

    extra: Dict[
        str,
        Any
    ] = field(

        default_factory=dict

    )

    # ------------------------------------------
    # Utility
    # ------------------------------------------

    @property
    def has_pages(

        self

    ) -> bool:

        return (

            self.pages is not None

        )

    @property
    def is_empty(

        self

    ) -> bool:

        return (

            len(

                self.text.strip()

            ) == 0

        )

    @property
    def total_characters(

        self

    ) -> int:

        return len(

            self.text

        )

    @property
    def total_words(

        self

    ) -> int:

        return len(

            self.text.split()

        )

    def to_dict(

        self

    ) -> Dict[
        str,
        Any
    ]:

        return {

            "text":

                self.text,

            "document_type":

                self.document_type,

            "source_path":

                self.source_path,

            "filename":

                self.filename,

            "metadata":

                self.metadata,

            "page_count":

                self.page_count,

            "pages":

                self.pages,

            "encoding":

                self.encoding,

            "language":

                self.language,

            "checksum":

                self.checksum,

            "file_size":

                self.file_size,

            "extra":

                self.extra

        }