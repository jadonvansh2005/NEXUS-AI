import csv

from typing import List

from rag.loaders.base_loader import (
    BaseLoader
)

from rag.loaders.loader_constants import (
    CSV_EXTENSIONS,
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


class CSVLoader(

    BaseLoader

):

    SUPPORTED_EXTENSIONS = (

        CSV_EXTENSIONS

    )

    def load(

        self

    ) -> LoadedDocument:

        rows: List[str] = []

        row_count = 0

        column_count = 0

        encoding = "utf-8"

        try:

            with open(

                self.absolute_path,

                mode="r",

                encoding="utf-8",

                newline=""

            ) as file:

                reader = csv.reader(

                    file

                )

                for row in reader:

                    column_count = max(

                        column_count,

                        len(

                            row

                        )

                    )

                    rows.append(

                        " | ".join(

                            str(

                                cell

                            )

                            for cell in row

                        )

                    )

                    row_count += 1

        except UnicodeDecodeError:

            encoding = "latin-1"

            rows.clear()

            row_count = 0
            column_count = 0

            with open(

                self.absolute_path,

                mode="r",

                encoding="latin-1",

                newline=""

            ) as file:

                reader = csv.reader(

                    file

                )

                for row in reader:

                    column_count = max(

                        column_count,

                        len(

                            row

                        )

                    )

                    rows.append(

                        " | ".join(

                            str(

                                cell

                            )

                            for cell in row

                        )

                    )

                    row_count += 1

        full_text = (

            "\n".join(

                rows

            )

        )

        full_text = (

            LoaderUtils.normalize_text(

                full_text

            )

        )

        return LoadedDocument(

            text=full_text,

            document_type=(

                DocumentType.CSV.value

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

                full_text

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

            extra={

                "row_count": row_count,

                "column_count": column_count

            }

        )


LoaderFactory.register(

    CSVLoader

)