"""
UPSS Literature Review Tool

Generate literature reviews.

Future integrations:

- Paper Search Tool
- Paper Summarizer Tool
- Citation Generator Tool
- Note Generator Tool
- Report Writer Tool
- LLM
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
    LiteratureReviewRequest,
    ResearchResponse,
)


class LiteratureReviewTool(BaseTool):
    """
    Generate literature reviews.
    """

    metadata = ToolMetadata(

        name="research.literature_review",

        display_name="Literature Review",

        description="Generate literature reviews from multiple research papers.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "literature",
            "review",
            "academic",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = LiteratureReviewRequest

    async def execute(
        self,
        context: ToolContext,
        request: LiteratureReviewRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # papers = PaperSearchTool.execute(...)
        #
        # summaries = PaperSummarizerTool.execute(...)
        #
        # citations = CitationGeneratorTool.execute(...)
        #
        # notes = NoteGeneratorTool.execute(...)
        #
        # review = LLM.generate_literature_review(...)
        #
        # ReportWriterTool.execute(...)
        #

        result = {

            "topic": request.topic,

            "paper_limit": request.paper_limit,

            "status": "literature_review_pending",

            "message": (

                "Literature review generation "

                "will be performed after "

                "research pipeline integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Literature review request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "literature_review": result,

                **response.model_dump(),

            },

        )