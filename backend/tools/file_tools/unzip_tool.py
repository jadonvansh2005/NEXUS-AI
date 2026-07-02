"""
UPSS Unzip Tool
"""

from __future__ import annotations

import zipfile
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


class UnzipTool(BaseTool):

    metadata = ToolMetadata(
        name="file.unzip",
        display_name="Unzip Archive",
        description="Extract ZIP archives.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "zip",
            "extract",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = CopyMoveRequest

    async def execute(
        self,
        context: ToolContext,
        request: CopyMoveRequest,
    ) -> ToolResult:

        archive = Path(request.path)
        destination = Path(request.destination)

        try:

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            with zipfile.ZipFile(
                archive,
                "r",
            ) as zip_ref:

                zip_ref.extractall(destination)

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="Archive extracted successfully.",
            data={
                "destination": str(destination.resolve()),
            },
        )