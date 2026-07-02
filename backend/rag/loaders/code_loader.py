from rag.loaders.base_loader import (
    BaseLoader
)

from rag.loaders.loader_constants import (
    CODE_EXTENSIONS,
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


class CodeLoader(

    BaseLoader

):

    SUPPORTED_EXTENSIONS = (

        CODE_EXTENSIONS

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

                code = (

                    file.read()

                )

        except UnicodeDecodeError:

            encoding = "latin-1"

            with open(

                self.absolute_path,

                "r",

                encoding="latin-1"

            ) as file:

                code = (

                    file.read()

                )

        return LoadedDocument(

            text=code,

            document_type=(

                DocumentType.CODE.value

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

                code

            ],

            encoding=encoding,

            checksum=(

                LoaderUtils.calculate_checksum(

                    self.absolute_path

                )

            ),

            file_size=(

                self.filesize

            ),

            language=(

                self.extension.replace(

                    ".",

                    ""

                )

            ),

            extra={

                "extension":

                    self.extension

            }

        )


LoaderFactory.register(

    CodeLoader

)