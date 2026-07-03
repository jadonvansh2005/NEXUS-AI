"""
UPSS Debugger Tool

Analyze runtime errors and prepare debugging.

Future integrations:

- Python Runner
- Terminal Tool
- Stack Trace Analyzer
- LLM
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
    DebugRequest,
    CodingResponse,
)


class DebuggerTool(BaseTool):
    """
    Analyze runtime errors and prepare debugging.
    """

    metadata = ToolMetadata(

        name="coding.debugger",

        display_name="Debugger",

        description="Analyze runtime errors and prepare debugging.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "debugger",
            "runtime",
            "stacktrace",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DebugRequest

    async def execute(
        self,
        context: ToolContext,
        request: DebugRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert developer and debugging assistant.
Analyze the following code and the provided stack trace / error details.
Identify the source of the crash/bug, explain what caused it, and provide step-by-step instructions to debug and fix it.
Language: {request.language}
Stack Trace: {request.stack_trace or "None provided"}

Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Debug analysis completed successfully."
        try:
            analysis = router.generate(prompt, request.stack_trace or "debug", "coding")
        except Exception as e:
            success = False
            analysis = f"Failed to perform debug analysis: {e}"
            message = f"Error during debug: {e}"

        result = {
            "language": request.language,
            "stack_trace_provided": request.stack_trace is not None,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "analysis": analysis,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "debug": result,
                **response.model_dump(),
            },
        )