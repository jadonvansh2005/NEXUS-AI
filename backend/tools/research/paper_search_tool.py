"""
UPSS Paper Search Tool

Search research papers.

Future integrations:

- arXiv
- Semantic Scholar
- Google Scholar
- PubMed
- Crossref
- Browser Tool
- Search Tool
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.research.schemas import (
    PaperSearchRequest,
    ResearchResponse,
)


class PaperSearchTool(BaseTool):
    """
    Search academic papers.
    """

    metadata = ToolMetadata(

        name="research.paper_search",

        display_name="Paper Search",

        description="Search academic research papers.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "papers",
            "scholar",
            "academic",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PaperSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: PaperSearchRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # provider = ProviderFactory.get(
        #     request.provider
        # )
        #
        # papers = await provider.search(
        #     query=request.query,
        #     limit=request.max_results,
        # )
        #
        # BrowserTool.fetch(...)
        #
        # SearchTool.search(...)
        #

        result = {

            "query": request.query,

            "provider": request.provider.value,

            "max_results": request.max_results,

            "status": "paper_search_pending",

            "message": (

                "Paper search will "

                "be performed after "

                "provider integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Paper search request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "paper_search": result,

                **response.model_dump(),

            },

        )