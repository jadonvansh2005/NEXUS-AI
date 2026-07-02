"""
UPSS Write File Tool

Writes text files to the local filesystem.
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
    FileContentRequest,
)


class WriteFileTool(BaseTool):
    """
    Creates or overwrites a text file.
    """

    metadata = ToolMetadata(
        name="file.write",
        display_name="Write File",
        description="Create or overwrite a text file.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "file",
            "filesystem",
            "write",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = FileContentRequest

    async def execute(
        self,
        context: ToolContext,
        request: FileContentRequest,
    ) -> ToolResult:

        path = Path(request.path)

        try:

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            path.write_text(
                request.content,
                encoding="utf-8",
            )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="File written successfully.",
            data={
                "path": str(path.resolve()),
                "size": path.stat().st_size,
            },
        )