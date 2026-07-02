"""
UPSS File Info Tool
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

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


class FileInfoTool(BaseTool):

    metadata = ToolMetadata(
        name="file.info",
        display_name="File Information",
        description="Retrieve file metadata.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "metadata"],
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
                message="Path does not exist.",
            )

        stat = path.stat()

        return ToolResult.ok(

            message="Metadata retrieved.",

            data={

                "name": path.name,

                "path": str(path.resolve()),

                "extension": path.suffix,

                "size": stat.st_size,

                "is_file": path.is_file(),

                "is_directory": path.is_dir(),

                "created": datetime.fromtimestamp(
                    stat.st_ctime
                ).isoformat(),

                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat(),

            },
        )