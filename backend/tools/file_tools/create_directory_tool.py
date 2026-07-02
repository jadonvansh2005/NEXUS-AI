"""
UPSS Create Directory Tool
"""

from __future__ import annotations

from pathlib import Path

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.file_tools.schemas import (
    FileRequest,
)


class CreateDirectoryTool(BaseTool):

    metadata = ToolMetadata(
        name="file.mkdir",
        display_name="Create Directory",
        description="Create a directory.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "directory"],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = FileRequest

    async def execute(
        self,
        context: ToolContext,
        request: FileRequest,
    ) -> ToolResult:

        path = Path(request.path)

        try:

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Directory created successfully.",
            data={
                "path": str(path.resolve()),
            },
        )