"""
UPSS Note Generator Tool

Generate structured research notes.

Future integrations:

- LLM
- Web Research Tool
- Paper Summarizer Tool
- Report Generator
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

from tools.research.schemas import (
    NoteGeneratorRequest,
    ResearchResponse,
)


class NoteGeneratorTool(BaseTool):
    """
    Generate structured research notes.
    """

    metadata = ToolMetadata(

        name="research.note_generator",

        display_name="Note Generator",

        description="Generate structured notes from research content.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "notes",
            "summary",
            "study",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = NoteGeneratorRequest

    async def execute(
        self,
        context: ToolContext,
        request: NoteGeneratorRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # notes = LLM.generate_notes(
        #     text=request.text,
        #     format=request.format,
        # )
        #
        # keywords = KeywordExtractor(...)
        #
        # concepts = ConceptExtractor(...)
        #
        # ReportGenerator.execute(...)
        #

        result = {

            "format": request.format,

            "text_length": len(request.text),

            "status": "note_generation_pending",

            "message": (

                "Note generation will "

                "be performed after "

                "LLM integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Note generation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "notes": result,

                **response.model_dump(),

            },

        )