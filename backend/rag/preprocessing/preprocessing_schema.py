from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


# --------------------------------------------------
# Parsed Page
# --------------------------------------------------

@dataclass
class ParsedPage:

    page_number: int

    text: str

    character_count: int

    word_count: int


# --------------------------------------------------
# Parsed Document
# --------------------------------------------------

@dataclass
class ParsedDocument:

    document_type: str

    filename: str

    source_path: str

    page_count: int

    pages: List[
        ParsedPage
    ]

    metadata: Dict[
        str,
        Any
    ] = field(

        default_factory=dict

    )

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
    def full_text(

        self

    ) -> str:

        return "\n\n".join(

            page.text

            for page in self.pages

        )

    @property
    def total_words(

        self

    ) -> int:

        return sum(

            page.word_count

            for page in self.pages

        )

    @property
    def total_characters(

        self

    ) -> int:

        return sum(

            page.character_count

            for page in self.pages

        )

    def to_dict(

        self

    ) -> Dict[
        str,
        Any
    ]:

        return {

            "document_type":

                self.document_type,

            "filename":

                self.filename,

            "source_path":

                self.source_path,

            "page_count":

                self.page_count,

            "pages": [

                {

                    "page_number":

                        page.page_number,

                    "text":

                        page.text,

                    "character_count":

                        page.character_count,

                    "word_count":

                        page.word_count

                }

                for page in self.pages

            ],

            "metadata":

                self.metadata,

            "extra":

                self.extra

        }