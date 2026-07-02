"""
UPSS ATS Score Tool

Analyze a resume for Applicant Tracking System (ATS)
compatibility.

Future integrations:

- Resume Parser
- LLM
- ATS Scoring Engine
- Keyword Extractor
"""

from __future__ import annotations

from pathlib import Path

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.career.schemas import (
    ATSScoreRequest,
    CareerResponse,
)


class ATSScoreTool(BaseTool):
    """
    Analyze resume ATS compatibility.
    """

    metadata = ToolMetadata(

        name="career.ats_score",

        display_name="ATS Score",

        description="Analyze ATS compatibility of a resume.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "resume",
            "ats",
            "analysis",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ATSScoreRequest

    async def execute(
        self,
        context: ToolContext,
        request: ATSScoreRequest,
    ) -> ToolResult:

        resume = Path(
            request.resume_path
        )

        if not resume.exists():

            return ToolResult.failure(

                message="Resume file not found."

            )

        #
        # Future Pipeline
        #
        # text = ResumeParser.parse(resume)
        #
        # ats = ATSScorer.score(
        #     resume=text,
        #     job_description=request.job_description,
        # )
        #

        result = {

            "resume": str(
                resume.resolve()
            ),

            "job_description_supplied":

                request.job_description
                is not None,

            "status": "ats_scoring_pending",

            "message": (

                "ATS scoring will be "

                "performed after "

                "provider integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Resume accepted for ATS analysis.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "ats": result,

                **response.model_dump(),

            },

        )