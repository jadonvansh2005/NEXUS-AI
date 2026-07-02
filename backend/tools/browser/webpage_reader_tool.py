"""
UPSS Webpage Reader Tool

Reads a webpage and extracts structured content.
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

from tools.browser.schemas import (
    BrowserRequest,
)

from tools.browser.adapters.base_browser_adapter import (
    BaseBrowserAdapter,
)

from tools.browser.adapters.playwright_adapter import (
    PlaywrightAdapter,
)


class WebPageReaderTool(BaseTool):
    """
    Reads webpage content using the configured browser adapter.
    """

    metadata = ToolMetadata(
        name="browser.reader",
        display_name="Webpage Reader",
        description="Reads webpage content and extracts text.",
        category=ToolCategory.BROWSER,
        tags=[
            "browser",
            "reader",
            "html",
            "webpage",
        ],
    )

    permission = ToolPermission.read_only()

    input_model = BrowserRequest

    def __init__(
        self,
        adapter: BaseBrowserAdapter | None = None,
    ):

        super().__init__()

        self.adapter = adapter or PlaywrightAdapter()

    async def initialize(self):

        await self.adapter.initialize()

    async def shutdown(self):

        await self.adapter.close()

    async def execute(
        self,
        context: ToolContext,
        request: BrowserRequest,
    ) -> ToolResult:

        response = await self.adapter.read(
            request
        )

        if not response.success:

            return ToolResult.failure(
                message=response.message,
            )

        return ToolResult.ok(
            message="Webpage read successfully.",
            data=response.model_dump(),
        )