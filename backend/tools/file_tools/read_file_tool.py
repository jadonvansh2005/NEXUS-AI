"""
UPSS Read File Tool

Reads text files from the local filesystem.
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


class ReadFileTool(BaseTool):
    """
    Reads a text file.

    Supports UTF-8 encoded files.
    """

    metadata = ToolMetadata(
        name="file.read",
        display_name="Read File",
        description="Read a text file from the local filesystem.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "file",
            "filesystem",
            "read",
        ],
    )

    permission = ToolPermission.read_only()

    input_model = FileRequest

    async def execute(
        self,
        context: ToolContext,
        request: FileRequest,
    ) -> ToolResult:

        path = Path(request.path)

        if not path.exists():

            return ToolResult.failure(
                message=f"File not found: {path}"
            )

        if not path.is_file():

            return ToolResult.failure(
                message=f"Path is not a file: {path}"
            )

        try:

            content = path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            return ToolResult.failure(
                message="File is not UTF-8 encoded."
            )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc)
            )

        return ToolResult.ok(

            message="File read successfully.",

            data={
                "path": str(path.resolve()),
                "name": path.name,
                "extension": path.suffix,
                "size": path.stat().st_size,
                "content": content,
            },
        )