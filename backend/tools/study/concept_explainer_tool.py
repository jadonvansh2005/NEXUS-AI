"""
UPSS Concept Explainer Tool

Explain educational concepts.

Future integrations:

- LLM
- Research Tool
- Browser Tool
- Search Tool
- Note Generator Tool
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
    ConceptExplainerRequest,
    StudyResponse,
)


class ConceptExplainerTool(BaseTool):
    """
    Explain educational concepts.
    """

    metadata = ToolMetadata(

        name="study.concept_explainer",

        display_name="Concept Explainer",

        description="Explain educational concepts at different learning levels.",

        category=ToolCategory.EDUCATION,

        tags=[
            "study",
            "education",
            "concept",
            "learning",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ConceptExplainerRequest

    async def execute(
        self,
        context: ToolContext,
        request: ConceptExplainerRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # research = WebResearchTool.execute(...)
        #
        # references = PaperSearchTool.execute(...)
        #
        # explanation = LLM.explain(
        #     topic=request.topic,
        #     level=request.level,
        # )
        #
        # NoteGeneratorTool.execute(...)
        #

        result = {

            "topic": request.topic,

            "level": request.level,

            "status": "concept_explanation_pending",

            "message": (

                "Concept explanation "

                "will be generated after "

                "LLM and Research "

                "tool integration."

            ),

        }

        response = StudyResponse(

            success=True,

            message="Concept explanation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "concept": result,

                **response.model_dump(),

            },

        )