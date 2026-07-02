from typing import List

from rag.loaders.loader_schema import (
    LoadedDocument
)

from rag.preprocessing.preprocessing_schema import (
    ParsedDocument,
    ParsedPage
)


class DocumentParser:

    @staticmethod
    def parse(

        document: LoadedDocument

    ) -> ParsedDocument:

        pages = (

            document.pages

            if document.pages is not None

            else [

                document.text

            ]

        )

        parsed_pages: List[

            ParsedPage

        ] = []

        for index, page in enumerate(

            pages

        ):

            parsed_pages.append(

                ParsedPage(

                    page_number=index + 1,

                    text=page,

                    character_count=len(

                        page

                    ),

                    word_count=len(

                        page.split()

                    )

                )

            )

        return ParsedDocument(

            document_type=(

                document.document_type

            ),

            filename=(

                document.filename

            ),

            source_path=(

                document.source_path

            ),

            page_count=len(

                parsed_pages

            ),

            pages=parsed_pages,

            metadata=(

                document.metadata

            ),

            extra=(

                document.extra

            )

        )

    @staticmethod
    def extract_text(

        document: LoadedDocument

    ) -> str:

        return (

            document.text

        )

    @staticmethod
    def extract_pages(

        document: LoadedDocument

    ) -> List[str]:

        if (

            document.pages

            is None

        ):

            return [

                document.text

            ]

        return (

            document.pages

        )

    @staticmethod
    def total_words(

        document: LoadedDocument

    ) -> int:

        return len(

            document.text.split()

        )

    @staticmethod
    def total_characters(

        document: LoadedDocument

    ) -> int:

        return len(

            document.text

        )

    @staticmethod
    def page_count(

        document: LoadedDocument

    ) -> int:

        if (

            document.pages

            is None

        ):

            return 1

        return len(

            document.pages

        )