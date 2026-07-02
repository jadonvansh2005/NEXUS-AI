"""
UPSS Search File Tool
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

from tools.file_tools.schemas import SearchRequest


class SearchFileTool(BaseTool):

    metadata = ToolMetadata(
        name="file.search",
        display_name="Search Files",
        description="Search files using glob patterns.",
        category=ToolCategory.FILE_SYSTEM,
        tags=["file", "search"],
    )

    permission = ToolPermission.read_only()

    input_model = SearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: SearchRequest,
    ) -> ToolResult:

        root = Path(request.path)

        if not root.exists():

            return ToolResult.failure(
                message=f"{root} does not exist."
            )

        results = []

        for file in root.rglob(request.pattern):

            results.append(
                {
                    "name": file.name,
                    "path": str(file.resolve()),
                    "is_file": file.is_file(),
                    "is_directory": file.is_dir(),
                }
            )

        return ToolResult.ok(
            message="Search completed successfully.",
            data=results,
        )