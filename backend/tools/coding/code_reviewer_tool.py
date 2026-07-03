"""
UPSS Code Reviewer Tool

Review source code and provide feedback.

Future integrations:

- LLM
- Ruff
- Pylint
- Flake8
- SonarQube
- CodeQL
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
    CodeReviewRequest,
    CodingResponse,
)


class CodeReviewerTool(BaseTool):
    """
    Review source code.
    """

    metadata = ToolMetadata(

        name="coding.code_reviewer",

        display_name="Code Reviewer",

        description="Analyze source code and provide review feedback.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "review",
            "quality",
            "analysis",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CodeReviewRequest

    async def execute(
        self,
        context: ToolContext,
        request: CodeReviewRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert senior software developer and code reviewer.
Review the following code for bugs, logic errors, performance issues, readability, and security vulnerabilities.
Provide constructive feedback and recommended improvements.
Language: {request.language}
Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Code review completed successfully."
        try:
            review_feedback = router.generate(prompt, request.code, "coding")
        except Exception as e:
            success = False
            review_feedback = f"Failed to perform code review: {e}"
            message = f"Error during code review: {e}"

        result = {
            "language": request.language,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "review": review_feedback,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "review": result,
                **response.model_dump(),
            },
        )