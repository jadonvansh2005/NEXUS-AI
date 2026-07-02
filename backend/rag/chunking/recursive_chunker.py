from typing import List
from typing import Optional

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class RecursiveChunker:

    def __init__(

        self,

        chunk_size: int = 1000,

        chunk_overlap: int = 200,

        separators: Optional[List[str]] = None

    ):

        if separators is None:

            separators = [

                "\n\n",

                "\n",

                ". ",

                "? ",

                "! ",

                ", ",

                " ",

                ""

            ]

        self.chunk_size = (

            chunk_size

        )

        self.chunk_overlap = (

            chunk_overlap

        )

        self.separators = (

            separators

        )

        self.splitter = (

            RecursiveCharacterTextSplitter(

                chunk_size=self.chunk_size,

                chunk_overlap=self.chunk_overlap,

                separators=self.separators,

                length_function=len,

                keep_separator=True,

                is_separator_regex=False

            )

        )

    def split(

        self,

        text: str

    ) -> List[str]:

        if (

            not text

        ):

            return []

        return (

            self.splitter.split_text(

                text

            )

        )

    def chunk_count(

        self,

        text: str

    ) -> int:

        return len(

            self.split(

                text

            )

        )

    def average_chunk_length(

        self,

        text: str

    ) -> float:

        chunks = (

            self.split(

                text

            )

        )

        if (

            not chunks

        ):

            return 0.0

        total = sum(

            len(

                chunk

            )

            for chunk in chunks

        )

        return (

            total /

            len(

                chunks

            )

        )

    def get_configuration(

        self,

    ) -> dict:

        return {

            "chunk_size": self.chunk_size,

            "chunk_overlap": self.chunk_overlap,

            "separators": self.separators

        }

    def __repr__(

        self

    ) -> str:

        return (

            f"RecursiveChunker("

            f"chunk_size={self.chunk_size}, "

            f"chunk_overlap={self.chunk_overlap}"

            f")"

        )