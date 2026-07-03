"""
UPSS Code Explainer Tool

Explain source code.

Future integrations:

- LLM
- AST Parser
- Dependency Analyzer
- Documentation Tool
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
    CodeExplainerRequest,
    CodingResponse,
)


class CodeExplainerTool(BaseTool):
    """
    Explain source code.
    """

    metadata = ToolMetadata(

        name="coding.code_explainer",

        display_name="Code Explainer",

        description="Explain source code in a human-readable format.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "code",
            "explain",
            "learning",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CodeExplainerRequest

    async def execute(
        self,
        context: ToolContext,
        request: CodeExplainerRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert software engineer and technical teacher.
Explain the following code in a clear, human-readable, and step-by-step format.
Detail what the code does, its algorithmic complexity (if relevant), and how it works.
Language: {request.language}
Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Code explanation completed successfully."
        try:
            explanation = router.generate(prompt, request.code, "coding")
        except Exception as e:
            success = False
            explanation = f"Failed to explain code: {e}"
            message = f"Error explaining code: {e}"

        result = {
            "language": request.language,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "explanation": explanation,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "code_explanation": result,
                **response.model_dump(),
            },
        )