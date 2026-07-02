from abc import ABC
from abc import abstractmethod

from pathlib import Path

from typing import Dict
from typing import Any


class BaseLoader(

    ABC

):

    SUPPORTED_EXTENSIONS = []


    def __init__(

        self,

        file_path: str

    ):

        self.file_path = (

            Path(

                file_path

            )

        )

        self.validate()


    # ------------------------------------------
    # Validation
    # ------------------------------------------

    def validate(

        self

    ) -> None:

        if (

            not self.file_path.exists()

        ):

            raise FileNotFoundError(

                f"File not found: "

                f"{self.file_path}"

            )

        if (

            self.SUPPORTED_EXTENSIONS

            and

            self.file_path.suffix.lower()

            not in

            self.SUPPORTED_EXTENSIONS

        ):

            raise ValueError(

                f"Unsupported file type: "

                f"{self.file_path.suffix}"

            )


    # ------------------------------------------
    # File Information
    # ------------------------------------------

    @property

    def filename(

        self

    ) -> str:

        return (

            self.file_path.name

        )


    @property

    def extension(

        self

    ) -> str:

        return (

            self.file_path.suffix.lower()

        )


    @property

    def filesize(

        self

    ) -> int:

        return (

            self.file_path.stat().st_size

        )


    @property

    def absolute_path(

        self

    ) -> str:

        return str(

            self.file_path.resolve()

        )


    # ------------------------------------------
    # Metadata
    # ------------------------------------------

    def metadata(

        self

    ) -> Dict[str, Any]:

        return {

            "filename":

                self.filename,

            "extension":

                self.extension,

            "filesize":

                self.filesize,

            "path":

                self.absolute_path

        }


    # ------------------------------------------
    # Loader Interface
    # ------------------------------------------

    @abstractmethod

    def load(

        self

    ) -> str:

        """
        Return extracted text.
        """

        pass