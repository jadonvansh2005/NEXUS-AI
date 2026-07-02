"""
UPSS List Directory Tool
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


class ListDirectoryTool(BaseTool):

    metadata = ToolMetadata(
        name="file.list",
        display_name="List Directory",
        description="List directory contents.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "directory"],
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
                message=f"{path} does not exist."
            )

        if not path.is_dir():

            return ToolResult.failure(
                message=f"{path} is not a directory."
            )

        files = []

        for item in path.iterdir():

            files.append({

                "name": item.name,

                "path": str(item.resolve()),

                "type": "directory"
                if item.is_dir()
                else "file",

                "size": item.stat().st_size,

            })

        return ToolResult.ok(
            message="Directory listed successfully.",
            data=files,
        )