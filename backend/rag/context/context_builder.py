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

        print("\n" + "=" * 80)
        print("[ContextBuilder] Building Context")
        print("=" * 80)

        # --------------------------------------------------
        # Single Source
        # --------------------------------------------------

        if isinstance(

            contexts,

            list

        ):

            print(f"[ContextBuilder] Single Source Mode")
            print(f"[ContextBuilder] Total Results : {len(contexts)}")

            context = (

                self._build_section(

                    "context",

                    contexts

                )

            )

            print("\n[ContextBuilder] Final Context:\n")
            print(context if context else "<< EMPTY CONTEXT >>")
            print("=" * 80 + "\n")

            return context

        # --------------------------------------------------
        # Multi Source
        # --------------------------------------------------

        print("[ContextBuilder] Multi Source Mode\n")

        sections: List[str] = []

        for source, results in (

            contexts.items()

        ):

            print(f"Source : {source}")
            print(f"Results: {len(results)}")

            if results:

                for i, result in enumerate(results, start=1):

                    print(f"\n  Result {i}")
                    print(f"  Score : {result.score}")

                    payload = result.payload or {}

                    text = payload.get(

                        "text",

                        ""

                    )

                    if text:

                        print("  Chunk Preview:")
                        print(text[:200])

            print("-" * 80)

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

        context = (

            self.separator.join(

                sections

            )

        )

        print("\n========== FINAL CONTEXT ==========\n")

        if context:

            print(context)

        else:

            print("<< EMPTY CONTEXT >>")

        print("\n===================================\n")

        return context

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