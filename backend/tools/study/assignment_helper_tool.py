"""
UPSS Assignment Helper Tool

Assist students in understanding and planning assignments.

Future integrations:

- LLM
- Concept Explainer Tool
- Research Tool
- Note Generator Tool
- Report Writer Tool
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
    AssignmentHelperRequest,
    StudyResponse,
)


class AssignmentHelperTool(BaseTool):
    """
    Help students understand and plan assignments.
    """

    metadata = ToolMetadata(

        name="study.assignment_helper",

        display_name="Assignment Helper",

        description="Assist students in understanding and planning assignments.",

        category=ToolCategory.EDUCATION,

        tags=[
            "study",
            "assignment",
            "education",
            "guidance",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = AssignmentHelperRequest

    async def execute(
        self,
        context: ToolContext,
        request: AssignmentHelperRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # concepts = ConceptExplainerTool.execute(...)
        #
        # research = WebResearchTool.execute(...)
        #
        # notes = NoteGeneratorTool.execute(...)
        #
        # guidance = LLM.assignment_guidance(
        #     assignment=request.assignment,
        #     subject=request.subject,
        # )
        #
        # ReportWriterTool.execute(...)
        #

        result = {

            "subject": request.subject,

            "assignment_length": len(
                request.assignment
            ),

            "status": "assignment_guidance_pending",

            "message": (

                "Assignment guidance will "

                "be generated after "

                "LLM integration."

            ),

        }

        response = StudyResponse(

            success=True,

            message="Assignment request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "assignment": result,

                **response.model_dump(),

            },

        )