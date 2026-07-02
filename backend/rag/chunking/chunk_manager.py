from typing import List
from typing import Dict
from typing import Any

from rag.chunking.recursive_chunker import (
    RecursiveChunker
)

from rag.chunking.semantic_chunker import (
    SemanticChunker
)


DEFAULT_CONFIGURATION = {

    "conversation": {

        "strategy": "recursive",

        "chunk_size": 400,

        "chunk_overlap": 80

    },

    "document": {

        "strategy": "semantic",

        "chunk_size": 1000,

        "chunk_overlap": 200

    },

    "semantic": {

        "strategy": "semantic",

        "chunk_size": 600,

        "chunk_overlap": 100

    },

    "knowledge": {

        "strategy": "semantic",

        "chunk_size": 1200,

        "chunk_overlap": 250

    },

    "project": {

        "strategy": "recursive",

        "chunk_size": 800,

        "chunk_overlap": 150

    },

    "code": {

        "strategy": "recursive",

        "chunk_size": 600,

        "chunk_overlap": 100

    }

}


class ChunkManager:


    def __init__(

        self

    ):

        self._recursive = {}

        self._semantic = None


    def split(

        self,

        text: str,

        source: str

    ) -> List[str]:

        config = (

            DEFAULT_CONFIGURATION.get(

                source

            )

        )

        if config is None:

            raise ValueError(

                f"Unsupported source: {source}"

            )

        strategy = (

            config["strategy"]

        )

        if strategy == "semantic":

            if self._semantic is None:

                self._semantic = (

                    SemanticChunker()

                )

            return (

                self._semantic.split(

                    text

                )

            )

        chunker = (

            self._get_recursive(

                config

            )

        )

        return (

            chunker.split(

                text

            )

        )


    def chunk_count(

        self,

        text: str,

        source: str

    ) -> int:

        return len(

            self.split(

                text,

                source

            )

        )


    def configuration(

        self,

        source: str

    ) -> Dict[str, Any]:

        config = (

            DEFAULT_CONFIGURATION.get(

                source

            )

        )

        if config is None:

            raise ValueError(

                f"Unsupported source: {source}"

            )

        return config.copy()


    def supported_sources(

        self

    ) -> List[str]:

        return list(

            DEFAULT_CONFIGURATION.keys()

        )


    def _get_recursive(

        self,

        config: Dict[str, Any]

    ) -> RecursiveChunker:

        key = (

            f"{config['chunk_size']}_"

            f"{config['chunk_overlap']}"

        )

        if key not in self._recursive:

            self._recursive[key] = (

                RecursiveChunker(

                    chunk_size=config[

                        "chunk_size"

                    ],

                    chunk_overlap=config[

                        "chunk_overlap"

                    ]

                )

            )

        return (

            self._recursive[key]

        )