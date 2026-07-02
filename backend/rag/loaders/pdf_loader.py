from typing import List

import fitz

from rag.loaders.base_loader import (
    BaseLoader
)

from rag.loaders.loader_constants import (
    PDF_EXTENSIONS,
    DocumentType
)

from rag.loaders.loader_factory import (
    LoaderFactory
)

from rag.loaders.loader_schema import (
    LoadedDocument
)

from rag.loaders.loader_utils import (
    LoaderUtils
)


class PDFLoader(

    BaseLoader

):

    SUPPORTED_EXTENSIONS = (

        PDF_EXTENSIONS

    )

    def load(

        self

    ) -> LoadedDocument:

        document = (

            fitz.open(

                self.absolute_path

            )

        )

        pages: List[str] = []

        for page in document:

            text = (

                page.get_text()

            )

            pages.append(

                LoaderUtils.normalize_text(

                    text

                )

            )

        document.close()

        full_text = (

            "\n\n".join(

                pages

            )

        )

        return LoadedDocument(

            text=full_text,

            document_type=(

                DocumentType.PDF.value

            ),

            source_path=(

                self.absolute_path

            ),

            filename=(

                self.filename

            ),

            metadata=self.metadata(),

            page_count=len(

                pages

            ),

            pages=pages,

            checksum=(

                LoaderUtils.calculate_checksum(

                    self.absolute_path

                )

            ),

            file_size=(

                self.filesize

            )

        )


LoaderFactory.register(

    PDFLoader

)