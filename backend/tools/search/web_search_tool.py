"""
UPSS Web Search Tool
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
    SearchProvider,
    SearchRequest,
)

from tools.search.adapter_factory import (
    SearchAdapterFactory,
)


class WebSearchTool(BaseTool):
    """
    Generic Web Search Tool.

    Search provider selection is delegated to the
    SearchAdapterFactory.
    """

    metadata = ToolMetadata(
        name="search.web",
        display_name="Web Search",
        description="Search the web using configured provider.",
        category=ToolCategory.SEARCH,
        tags=["search", "web"],
    )

    permission = ToolPermission.read_only()

    input_model = SearchRequest

    def __init__(
        self,
        provider: SearchProvider = SearchProvider.AUTO,
    ):

        super().__init__()

        self.provider = provider

        self.adapter = SearchAdapterFactory.create(
            provider
        )

    async def initialize(self):

        await self.adapter.initialize()

    async def shutdown(self):

        await self.adapter.close()

    async def execute(
        self,
        context: ToolContext,
        request: SearchRequest,
    ) -> ToolResult:

        response = await self.adapter.search(
            request
        )

        return ToolResult.ok(
            message="Search completed successfully.",
            data=response.model_dump(),
        )