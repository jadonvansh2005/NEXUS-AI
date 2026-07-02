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

        category=ToolCategory.DEVELOPER,

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

        #
        # Future Pipeline
        #
        # parser = ASTParser(...)
        #
        # structure = parser.parse(
        #     request.code
        # )
        #
        # documentation = LLM.generate_documentation(
        #     code=request.code,
        #     language=request.language,
        # )
        #
        # READMEGenerator(...)
        #
        # FileTool.write(...)
        #

        result = {

            "language": request.language,

            "lines_of_code": len(
                request.code.splitlines()
            ),

            "status": "documentation_generation_pending",

            "message": (

                "Documentation generation "

                "will be performed after "

                "LLM integration."

            ),

        }

        response = CodingResponse(

            success=True,

            message="Documentation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "documentation": result,

                **response.model_dump(),

            },

        )