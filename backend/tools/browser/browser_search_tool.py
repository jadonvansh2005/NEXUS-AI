"""
UPSS Browser Search Tool

Searches the web and automatically reads
the most relevant webpage.
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

from tools.search.schemas import (
    SearchRequest,
)

from tools.browser.schemas import (
    BrowserRequest,
)

from tools.search.web_search_tool import (
    WebSearchTool,
)

from tools.browser.webpage_reader_tool import (
    WebPageReaderTool,
)


class BrowserSearchTool(BaseTool):

    metadata = ToolMetadata(
        name="browser.search",
        display_name="Browser Search",
        description="Searches the web and reads the best result.",
        category=ToolCategory.BROWSER,
        tags=[
            "browser",
            "search",
            "research",
        ],
    )

    permission = ToolPermission.read_only()

    input_model = SearchRequest

    def __init__(self):

        super().__init__()

        self.search_tool = WebSearchTool()

        self.reader_tool = WebPageReaderTool()

    async def initialize(self):

        await self.search_tool.initialize()

        await self.reader_tool.initialize()

    async def shutdown(self):

        await self.search_tool.shutdown()

        await self.reader_tool.shutdown()

    async def execute(

        self,

        context: ToolContext,

        request: SearchRequest,

    ) -> ToolResult:

        search_result = await self.search_tool.execute(

            context,

            request,

        )

        if not search_result.success:

            return search_result

        results = search_result.data.get(
            "results",
            [],
        )

        if not results:

            return ToolResult.failure(
                message="No search results found.",
            )

        best_result = results[0]

        page = await self.reader_tool.execute(

            context,

            BrowserRequest(
                url=best_result["url"],
            ),

        )

        return ToolResult.ok(

            message="Search completed successfully.",

            data={

                "search": search_result.data,

                "page": page.data,

            },

        )