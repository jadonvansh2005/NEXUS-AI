"""
UPSS Web Research Tool

Research information from the web.

Future integrations:

- Search Tool
- Browser Tool
- LLM
- Report Generator
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
    WebResearchRequest,
    ResearchResponse,
)


class WebResearchTool(BaseTool):
    """
    Perform web research.
    """

    metadata = ToolMetadata(

        name="research.web_research",

        display_name="Web Research",

        description="Research information from the web.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "web",
            "browser",
            "search",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = WebResearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: WebResearchRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # search_results = SearchTool.execute(
        #     query=request.query,
        #     max_results=request.max_results,
        # )
        #
        # pages = BrowserTool.execute(
        #     urls=search_results,
        # )
        #
        # summary = LLM.summarize(
        #     pages,
        # )
        #
        # ReportGenerator.execute(...)
        #

        result = {

            "query": request.query,

            "max_results": request.max_results,

            "status": "web_research_pending",

            "message": (

                "Web research will be "

                "performed after "

                "Search and Browser "

                "tool integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Web research request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "research": result,

                **response.model_dump(),

            },

        )