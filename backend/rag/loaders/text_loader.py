from rag.loaders.base_loader import (
    BaseLoader
)

from rag.loaders.loader_constants import (
    TEXT_EXTENSIONS,
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


class TextLoader(

    BaseLoader

):

    SUPPORTED_EXTENSIONS = (

        TEXT_EXTENSIONS

    )

    def load(

        self

    ) -> LoadedDocument:

        encoding = "utf-8"

        try:

            with open(

                self.absolute_path,

                "r",

                encoding="utf-8"

            ) as file:

                text = (

                    file.read()

                )

        except UnicodeDecodeError:

            encoding = "latin-1"

            with open(

                self.absolute_path,

                "r",

                encoding="latin-1"

            ) as file:

                text = (

                    file.read()

                )

        text = (

            LoaderUtils.normalize_text(

                text

            )

        )

        return LoadedDocument(

            text=text,

            document_type=(

                DocumentType.TXT.value

            ),

            source_path=(

                self.absolute_path

            ),

            filename=(

                self.filename

            ),

            metadata=self.metadata(),

            page_count=1,

            pages=[

                text

            ],

            encoding=encoding,

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

    TextLoader

)