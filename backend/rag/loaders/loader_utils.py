import hashlib
import mimetypes

from pathlib import Path

from typing import Optional


class LoaderUtils:

    @staticmethod
    def calculate_checksum(

        file_path: str

    ) -> str:

        sha256 = hashlib.sha256()

        with open(

            file_path,

            "rb"

        ) as file:

            while True:

                chunk = file.read(

                    8192

                )

                if not chunk:

                    break

                sha256.update(

                    chunk

                )

        return sha256.hexdigest()

    @staticmethod
    def detect_mime_type(

        file_path: str

    ) -> Optional[str]:

        mime, _ = (

            mimetypes.guess_type(

                file_path

            )

        )

        return mime

    @staticmethod
    def normalize_text(

        text: str

    ) -> str:

        text = (

            text.replace(

                "\x00",

                ""

            )

        )

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

        lines = [

            line.strip()

            for line in text.split(

                "\n"

            )

        ]

        return "\n".join(

            lines

        ).strip()

    @staticmethod
    def file_size(

        file_path: str

    ) -> int:

        return (

            Path(

                file_path

            )

            .stat()

            .st_size

        )

    @staticmethod
    def filename(

        file_path: str

    ) -> str:

        return (

            Path(

                file_path

            )

            .name

        )

    @staticmethod
    def extension(

        file_path: str

    ) -> str:

        return (

            Path(

                file_path

            )

            .suffix

            .lower()

        )

    @staticmethod
    def absolute_path(

        file_path: str

    ) -> str:

        return str(

            Path(

                file_path

            )

            .resolve()

        )