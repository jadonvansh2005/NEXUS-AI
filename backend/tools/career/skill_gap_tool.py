"""
UPSS Skill Gap Tool

Analyze skill gaps for a target career role.

Future integrations:

- Job Providers
- LLM
- Skill Extraction
- Resume Analyzer
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

from tools.career.schemas import (
    SkillGapRequest,
    CareerResponse,
)


class SkillGapTool(BaseTool):
    """
    Analyze missing skills for a target role.
    """

    metadata = ToolMetadata(

        name="career.skill_gap",

        display_name="Skill Gap Analysis",

        description="Analyze skill gaps for a target role.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "skills",
            "analysis",
            "learning",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = SkillGapRequest

    async def execute(
        self,
        context: ToolContext,
        request: SkillGapRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # required_skills = JobProvider.get_required_skills(
        #     role=request.target_role
        # )
        #
        # current_skills = SkillExtractor.normalize(
        #     request.current_skills
        # )
        #
        # analysis = SkillGapAnalyzer.compare(
        #     current=current_skills,
        #     required=required_skills,
        # )
        #

        result = {

            "target_role": request.target_role,

            "current_skills": request.current_skills,

            "status": "skill_gap_analysis_pending",

            "message": (

                "Skill gap analysis "

                "will be available after "

                "provider integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Skill gap request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "skill_gap": result,

                **response.model_dump(),

            },

        )