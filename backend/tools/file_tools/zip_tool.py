"""
UPSS Zip Tool
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


class ZipTool(BaseTool):

    metadata = ToolMetadata(
        name="file.zip",
        display_name="Zip Files",
        description="Compress files or directories into ZIP.",
        category=ToolCategory.FILE_SYSTEM,
        tags=[
            "zip",
            "archive",
        ],
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

        try:

            with zipfile.ZipFile(
                destination,
                "w",
                zipfile.ZIP_DEFLATED,
            ) as archive:

                if source.is_file():

                    archive.write(
                        source,
                        source.name,
                    )

                else:

                    for file in source.rglob("*"):

                        if file.is_file():

                            archive.write(
                                file,
                                file.relative_to(source),
                            )

        except Exception as exc:

            return ToolResult.failure(
                message=str(exc),
            )

        return ToolResult.ok(
            message="ZIP archive created successfully.",
            data={
                "archive": str(destination.resolve()),
            },
        )