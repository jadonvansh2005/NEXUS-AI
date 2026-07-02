"""
UPSS Download Tool

Downloads files using the browser.
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

from tools.browser.schemas import BrowserRequest
from tools.browser.adapters.base_browser_adapter import (
    BaseBrowserAdapter,
)
from tools.browser.adapters.playwright_adapter import (
    PlaywrightAdapter,
)


class DownloadTool(BaseTool):

    metadata = ToolMetadata(
        name="browser.download",
        display_name="Download Tool",
        description="Download files through browser.",
        category=ToolCategory.BROWSER,
        tags=[
            "browser",
            "download",
            "file",
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

        file_path = await self.adapter.download(
            request
        )

        return ToolResult.ok(
            message="File downloaded successfully.",
            data={
                "path": file_path,
            },
        )