"""
UPSS Research Planner Tool

Plan and orchestrate complete research workflows.

Future integrations:

- Web Research Tool
- Paper Search Tool
- Paper Summarizer Tool
- Literature Review Tool
- Fact Checker Tool
- Note Generator Tool
- Citation Generator Tool
- Bibliography Tool
- Report Writer Tool
- LLM Planner
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
    ResearchPlannerRequest,
    ResearchResponse,
)


class ResearchPlannerTool(BaseTool):
    """
    Plan complete research workflows.
    """

    metadata = ToolMetadata(

        name="research.research_planner",

        display_name="Research Planner",

        description="Plan and orchestrate complete research workflows.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "planner",
            "workflow",
            "academic",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ResearchPlannerRequest

    async def execute(
        self,
        context: ToolContext,
        request: ResearchPlannerRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # plan = LLMPlanner.create_plan(
        #     topic=request.topic,
        #     objective=request.objective,
        # )
        #
        # WebResearchTool.execute(...)
        #
        # PaperSearchTool.execute(...)
        #
        # PaperSummarizerTool.execute(...)
        #
        # LiteratureReviewTool.execute(...)
        #
        # FactCheckerTool.execute(...)
        #
        # NoteGeneratorTool.execute(...)
        #
        # CitationGeneratorTool.execute(...)
        #
        # BibliographyTool.execute(...)
        #
        # ReportWriterTool.execute(...)
        #

        result = {

            "topic": request.topic,

            "objective": request.objective,

            "duration_weeks": request.duration_weeks,

            "status": "research_planning_pending",

            "message": (

                "Research planning will "

                "be performed after "

                "workflow integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Research planning request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "research_plan": result,

                **response.model_dump(),

            },

        )