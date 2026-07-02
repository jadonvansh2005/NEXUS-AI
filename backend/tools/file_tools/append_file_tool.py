"""
UPSS Append File Tool

Appends content to an existing text file.
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


class AppendFileTool(BaseTool):

    metadata = ToolMetadata(
        name="file.append",
        display_name="Append File",
        description="Append content to a text file.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "file",
            "append",
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

            with path.open(
                "a",
                encoding="utf-8",
            ) as f:

                f.write(request.content)

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Content appended successfully.",
            data={
                "path": str(path.resolve()),
                "size": path.stat().st_size,
            },
        )