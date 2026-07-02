"""
UPSS Copy File Tool
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

from tools.file_tools.schemas import CopyMoveRequest


class CopyFileTool(BaseTool):

    metadata = ToolMetadata(
        name="file.copy",
        display_name="Copy File",
        description="Copy files or directories.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "copy"],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = CopyMoveRequest

    async def execute(
        self,
        context: ToolContext,
        request: CopyMoveRequest,
    ) -> ToolResult:

        source = Path(request.path)
        destination = Path(request.destination)

        if not source.exists():

            return ToolResult.failure(
                message="Source does not exist."
            )

        try:

            if source.is_dir():

                shutil.copytree(
                    source,
                    destination,
                    dirs_exist_ok=True,
                )

            else:

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.copy2(
                    source,
                    destination,
                )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Copy completed.",
            data={
                "source": str(source),
                "destination": str(destination),
            },
        )