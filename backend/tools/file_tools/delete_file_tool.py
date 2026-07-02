"""
UPSS Delete File Tool
"""

from __future__ import annotations

import shutil
from pathlib import Path

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.file_tools.schemas import FileRequest


class DeleteFileTool(BaseTool):

    metadata = ToolMetadata(
        name="file.delete",
        display_name="Delete File",
        description="Delete a file or directory.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "file",
            "delete",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = FileRequest

    async def execute(
        self,
        context: ToolContext,
        request: FileRequest,
    ) -> ToolResult:

        path = Path(request.path)

        if not path.exists():

            return ToolResult.failure(
                message="Path does not exist.",
            )

        try:

            if path.is_dir():

                shutil.rmtree(path)

            else:

                path.unlink()

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Deletion completed successfully.",
            data={
                "deleted_path": str(path),
            },
        )