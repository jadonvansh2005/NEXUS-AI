"""
UPSS Documentation Tool

Generate project documentation.

Future integrations:

- LLM
- AST Parser
- README Generator
- Sphinx
- MkDocs
- File Tool
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
    DocumentationRequest,
    CodingResponse,
)


class DocumentationTool(BaseTool):
    """
    Generate project documentation.
    """

    metadata = ToolMetadata(

        name="coding.documentation",

        display_name="Documentation Generator",

        description="Generate documentation for source code.",

        category=ToolCategory.OTHER,

        tags=[
            "documentation",
            "readme",
            "api",
            "coding",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DocumentationRequest

    async def execute(
        self,
        context: ToolContext,
        request: DocumentationRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert developer and technical writer.
Generate complete and clear documentation for the following source code.
Create inline docstrings/comments directly inside the code if helpful, or return a Markdown document explaining the modules, classes, and functions.
Language: {request.language}

Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Documentation generated successfully."
        try:
            documentation = router.generate(prompt, request.code, "coding")
        except Exception as e:
            success = False
            documentation = f"Failed to generate documentation: {e}"
            message = f"Error during documentation generation: {e}"

        result = {
            "language": request.language,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "documentation": documentation,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "documentation": result,
                **response.model_dump(),
            },
        )