from abc import ABC

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rag.context.context_builder import (
    ContextBuilder
)

from rag.context.prompt_builder import (
    PromptBuilder
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class BasePipeline(

    ABC

):

    def __init__(

        self,

        service

    ):

        self.service = service

        self.context_builder = (

            ContextBuilder()

        )

        self.prompt_builder = (

            PromptBuilder()

        )

    def index(

        self,

        **kwargs: Any

    ) -> int:

        return self.service.ingest(

            **kwargs

        )

    def retrieve(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[

            float

        ] = None,

        filters: Optional[

            Dict[str, Any]

        ] = None

    ) -> List[SearchResult]:

        return self.service.search(

            query=query,

            limit=limit,

            score_threshold=score_threshold,

            filters=filters

        )

    def run(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[

            float

        ] = None,

        filters: Optional[

            Dict[str, Any]

        ] = None,

        system_prompt: str = ""

    ) -> Dict[str, Any]:

        results = self.retrieve(

            query=query,

            limit=limit,

            score_threshold=score_threshold,

            filters=filters

        )

        context = (

            self.context_builder.build(

                results

            )

        )

        prompt = (

            self.prompt_builder.build(

                user_query=query,

                context=context,

                system_prompt=system_prompt

            )

        )

        return {

            "query": query,

            "context": context,

            "prompt": prompt,

            "results": results,

            "count": len(

                results

            )

        }