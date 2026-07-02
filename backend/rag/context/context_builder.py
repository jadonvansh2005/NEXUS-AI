from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from rag.vector_store.vector_schema import (
    SearchResult
)


class ContextBuilder:

    def __init__(

        self,

        separator: str = "\n\n"

    ):

        self.separator = (

            separator

        )

    # --------------------------------------------------
    # Build Context
    # --------------------------------------------------




    def build(

        self,

        contexts: Union[
            Dict[str, List[SearchResult]],
            List[SearchResult]
        ]

    ) -> str:

        # --------------------------------------------------
        # Single Source
        # --------------------------------------------------

        if isinstance(

            contexts,

            list

        ):

            return (

                self._build_section(

                    "context",

                    contexts

                )

            )

        # --------------------------------------------------
        # Multi Source
        # --------------------------------------------------

        sections: List[str] = []

        for source, results in (

            contexts.items()

        ):

            section = (

                self._build_section(

                    source,

                    results

                )

            )

            if section:

                sections.append(

                    section

                )

        return (

            self.separator.join(

                sections

            )

        )
    # --------------------------------------------------
    # Build One Section
    # --------------------------------------------------

    def _build_section(

        self,

        source: str,

        results: List[
            SearchResult
        ]

    ) -> str:

        if not results:

            return ""

        lines = [

            f"===== {source.upper()} ====="

        ]

        for result in results:

            payload = (

                result.payload

                or {}

            )

            text = (

                payload.get(

                    "text",

                    ""

                )

            )

            if text:

                lines.append(

                    text

                )

        return (

            self.separator.join(

                lines

            )

        )

    # --------------------------------------------------
    # Merge Context
    # --------------------------------------------------

    def merge(

        self,

        *contexts: Optional[str]

    ) -> str:

        valid = [

            context

            for context in contexts

            if context

        ]

        return (

            self.separator.join(

                valid

            )

        )

    # --------------------------------------------------
    # Empty Context
    # --------------------------------------------------

    @staticmethod
    def empty(

    ) -> str:

        return ""

    # --------------------------------------------------
    # Has Context
    # --------------------------------------------------

    @staticmethod
    def has_context(

        context: str

    ) -> bool:

        return bool(

            context.strip()

        )