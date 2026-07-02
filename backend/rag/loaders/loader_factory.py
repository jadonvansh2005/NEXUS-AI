from pathlib import Path
import rag.loaders
from typing import Dict
from typing import Type

from rag.loaders.base_loader import (
    BaseLoader
)


class LoaderFactory:

    _registry: Dict[
        str,
        Type[BaseLoader]
    ] = {}

    # ------------------------------------------
    # Register Loader
    # ------------------------------------------

    @classmethod
    def register(

        cls,

        loader: Type[BaseLoader]

    ) -> None:

        for extension in (

            loader.SUPPORTED_EXTENSIONS

        ):

            cls._registry[

                extension.lower()

            ] = loader

    # ------------------------------------------
    # Get Loader Class
    # ------------------------------------------

    @classmethod
    def get_loader(

        cls,

        file_path: str

    ) -> Type[BaseLoader]:

        extension = (

            Path(

                file_path

            )

            .suffix

            .lower()

        )

        if extension not in cls._registry:

            raise ValueError(

                f"No loader registered "

                f"for '{extension}'."

            )

        return cls._registry[

            extension

        ]

    # ------------------------------------------
    # Create Loader Instance
    # ------------------------------------------

    @classmethod
    def create(

        cls,

        file_path: str

    ) -> BaseLoader:

        loader = (

            cls.get_loader(

                file_path

            )

        )

        return loader(

            file_path

        )

    # ------------------------------------------
    # Utility
    # ------------------------------------------

    @classmethod
    def supported_extensions(

        cls

    ) -> list[str]:

        return sorted(

            cls._registry.keys()

        )