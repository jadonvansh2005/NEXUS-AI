"""
UPSS Browser History Tool
"""

from __future__ import annotations

from datetime import datetime

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)


class BrowserHistoryTool(BaseTool):

    metadata = ToolMetadata(
        name="browser.history",
        display_name="Browser History",
        description="Maintain browser navigation history.",
        category=ToolCategory.BROWSER,
        tags=[
            "browser",
            "history",
        ],
    )

    permission = ToolPermission.read_only()

    def __init__(self):

        super().__init__()

        self.history = []

    async def execute(
        self,
        context: ToolContext,
        request,
    ) -> ToolResult:

        return ToolResult.ok(
            message="Browser history retrieved.",
            data=self.history,
        )

    def add_entry(
        self,
        url: str,
        title: str,
    ):

        self.history.append(
            {
                "url": url,
                "title": title,
                "visited_at": datetime.utcnow().isoformat(),
            }
        )