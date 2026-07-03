"""
UPSS Bug Fixer Tool

Analyze source code and runtime errors to prepare
bug fixing.

Future integrations:

- LLM
- Python Runner
- Terminal Tool
- Debugger Tool
- GitHub Tool
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.coding.schemas import (
    BugFixRequest,
    CodingResponse,
)


class BugFixTool(BaseTool):
    """
    Analyze bugs and prepare a fixing workflow.
    """

    metadata = ToolMetadata(

        name="coding.bug_fixer",

        display_name="Bug Fixer",

        description="Analyze source code and prepare bug fixes.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "bug",
            "debug",
            "fix",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = BugFixRequest

    async def execute(
        self,
        context: ToolContext,
        request: BugFixRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert developer.
Analyze the following source code and the accompanying error message.
Find the root cause of the error and provide:
1. An explanation of what went wrong.
2. The fixed source code.

Language: {request.language}
Error Message: {request.error_message}

Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Bug fix suggestion generated successfully."
        try:
            fix_response = router.generate(prompt, request.error_message, "coding")
        except Exception as e:
            success = False
            fix_response = f"Failed to generate bug fix: {e}"
            message = f"Error during bug fixing: {e}"

        result = {
            "language": request.language,
            "error_message": request.error_message,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "fix": fix_response,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "bug_fix": result,
                **response.model_dump(),
            },
        )