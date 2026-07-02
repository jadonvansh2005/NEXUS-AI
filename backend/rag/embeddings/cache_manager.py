import hashlib

from typing import Dict
from typing import List
from typing import Optional


class EmbeddingCache:

    def __init__(self):

        self.cache: Dict[

            str,

            List[float]

        ] = {}

    def _generate_key(

        self,

        model_name: str,

        text: str

    ) -> str:

        cache_key = (

            f"{model_name}::{text}"

        )

        return hashlib.sha256(

            cache_key.encode(

                "utf-8"

            )

        ).hexdigest()

    def get(

        self,

        model_name: str,

        text: str

    ) -> Optional[List[float]]:

        key = (

            self._generate_key(

                model_name,

                text

            )

        )

        return self.cache.get(

            key

        )

    def set(

        self,

        model_name: str,

        text: str,

        embedding: List[float]

    ):

        key = (

            self._generate_key(

                model_name,

                text

            )

        )

        self.cache[

            key

        ] = embedding

    def exists(

        self,

        model_name: str,

        text: str

    ) -> bool:

        key = (

            self._generate_key(

                model_name,

                text

            )

        )

        return (

            key in self.cache

        )

    def clear(

        self

    ):

        self.cache.clear()

    def size(

        self

    ) -> int:

        return len(

            self.cache

        )