"""
UPSS Learning Roadmap Tool

Generate personalized learning roadmaps.

Future integrations:

- Concept Explainer Tool
- Research Domain
- Study Planner Tool
- Practice Question Tool
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

from tools.study.schemas import (
    LearningRoadmapRequest,
    StudyResponse,
)


class LearningRoadmapTool(BaseTool):
    """
    Generate personalized learning roadmaps.
    """

    metadata = ToolMetadata(

        name="study.learning_roadmap",

        display_name="Learning Roadmap",

        description="Generate personalized learning roadmaps.",

        category=ToolCategory.EDUCATION,

        tags=[
            "study",
            "roadmap",
            "learning",
            "education",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = LearningRoadmapRequest

    async def execute(
        self,
        context: ToolContext,
        request: LearningRoadmapRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # ConceptExplainerTool.execute(...)
        #
        # ResearchPlannerTool.execute(...)
        #
        # StudyPlannerTool.execute(...)
        #
        # PracticeQuestionTool.execute(...)
        #
        # roadmap = LLM.generate_learning_roadmap(
        #     skill=request.target_skill,
        #     level=request.current_level,
        # )
        #

        result = {

            "target_skill":

                request.target_skill,

            "current_level":

                request.current_level,

            "status":

                "learning_roadmap_pending",

            "message": (

                "Learning roadmap "

                "will be generated after "

                "workflow integration."

            ),

        }

        response = StudyResponse(

            success=True,

            message="Learning roadmap request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "learning_roadmap": result,

                **response.model_dump(),

            },

        )