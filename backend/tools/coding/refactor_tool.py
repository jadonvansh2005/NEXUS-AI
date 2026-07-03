"""
UPSS Refactor Tool

Refactor source code while preserving behavior.

Future integrations:

- LLM
- AST Parser
- Code Reviewer
- Test Generator
- Git Assistant
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
    RefactorRequest,
    CodingResponse,
)


class RefactorTool(BaseTool):
    """
    Refactor source code.
    """

    metadata = ToolMetadata(

        name="coding.refactor",

        display_name="Refactor Code",

        description="Improve code structure while preserving behavior.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "refactor",
            "clean-code",
            "maintainability",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = RefactorRequest

    async def execute(
        self,
        context: ToolContext,
        request: RefactorRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert software architect and developer.
Refactor the following code to improve its structure, performance, readability, or maintainability based on the objective:
Objective: {request.objective}
Language: {request.language}

Provide:
1. A summary of the changes made.
2. The complete refactored source code.

Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Code refactoring completed successfully."
        try:
            refactored_code = router.generate(prompt, request.objective, "coding")
        except Exception as e:
            success = False
            refactored_code = f"Failed to refactor code: {e}"
            message = f"Error during refactoring: {e}"

        result = {
            "language": request.language,
            "objective": request.objective,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "refactor": refactored_code,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "refactor": result,
                **response.model_dump(),
            },
        )