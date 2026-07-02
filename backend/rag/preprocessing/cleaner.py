import re

from rag.loaders.loader_schema import (
    LoadedDocument
)


class Cleaner:

    @staticmethod
    def clean(

        document: LoadedDocument

    ) -> LoadedDocument:

        text = document.text

        # ------------------------------------------
        # Normalize Line Endings
        # ------------------------------------------

        text = (

            text.replace(

                "\r\n",

                "\n"

            )

        )

        text = (

            text.replace(

                "\r",

                "\n"

            )

        )

        # ------------------------------------------
        # Remove Null Characters
        # ------------------------------------------

        text = (

            text.replace(

                "\x00",

                ""

            )

        )

        # ------------------------------------------
        # Remove Multiple Blank Lines
        # ------------------------------------------

        text = re.sub(

            r"\n{3,}",

            "\n\n",

            text

        )

        # ------------------------------------------
        # Remove Multiple Spaces
        # ------------------------------------------

        text = re.sub(

            r"[ \t]+",

            " ",

            text

        )

        text = text.strip()

        document.text = text

        if document.pages is not None:

            cleaned_pages = []

            for page in document.pages:

                page = page.replace(

                    "\r\n",

                    "\n"

                )

                page = page.replace(

                    "\r",

                    "\n"

                )

                page = page.replace(

                    "\x00",

                    ""

                )

                page = re.sub(

                    r"\n{3,}",

                    "\n\n",

                    page

                )

                page = re.sub(

                    r"[ \t]+",

                    " ",

                    page

                )

                cleaned_pages.append(

                    page.strip()

                )

            document.pages = (

                cleaned_pages

            )

        return document