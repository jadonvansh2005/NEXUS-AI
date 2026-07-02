from typing import List
from typing import Optional

from langchain_experimental.text_splitter import (
    SemanticChunker as LangchainSemanticChunker
)

from rag.embeddings.model_loader import (
    ModelLoader
)


class SemanticChunker:

    def __init__(

        self,

        embedding_model: Optional[str] = None,

        breakpoint_threshold_type: str = "percentile",

        breakpoint_threshold_amount: int = 90

    ):

        if embedding_model is None:

            embedding_model = (

                "BAAI/bge-m3"

            )

        self.model = (

            ModelLoader.load(

                model_key="bge_m3"

            )

        )
        self.chunker = (

            LangchainSemanticChunker(

                embeddings=self,

                breakpoint_threshold_type=(
                    breakpoint_threshold_type
                ),
                breakpoint_threshold_amount=(
                    breakpoint_threshold_amount
                )
            )

        )

    # --------------------------------------
    # LangChain Embedding Interface
    # --------------------------------------

    def embed_documents(

        self,

        texts: List[str]

    ) -> List[List[float]]:

        vectors = (

            self.model.encode(

                texts,

                normalize_embeddings=True

            )

        )

        return (

            vectors.tolist()

        )

    def embed_query(

        self,

        text: str

    ) -> List[float]:

        return (

            self.model.encode(

                text,

                normalize_embeddings=True

            ).tolist()

        )

    # --------------------------------------
    # Chunking
    # --------------------------------------

    def split(

        self,

        text: str

    ) -> List[str]:

        documents = (

            self.chunker.create_documents(

                [

                    text

                ]

            )

        )

        return [

            doc.page_content

            for doc in documents

        ]

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

        if not chunks:

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

    def __repr__(

        self

    ) -> str:

        return (

            "SemanticChunker()"

        )