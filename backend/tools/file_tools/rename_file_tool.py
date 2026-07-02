"""
UPSS Move File Tool
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


class MoveFileTool(BaseTool):

    metadata = ToolMetadata(
        name="file.move",
        display_name="Move File",
        description="Move files or directories.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "move"],
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

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(source),
                str(destination),
            )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Move completed.",
            data={
                "source": str(source),
                "destination": str(destination),
            },
        )