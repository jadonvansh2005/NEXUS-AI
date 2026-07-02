"""
UPSS Resume Builder Tool

Build professional resumes.

Future integrations:

- Jinja2 Templates
- PDF Report Tool
- DOCX Generator
- AI Resume Optimizer
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
    ResumeBuilderRequest,
    CareerResponse,
)


class ResumeBuilderTool(BaseTool):
    """
    Build professional resumes.
    """

    metadata = ToolMetadata(

        name="career.resume_builder",

        display_name="Resume Builder",

        description="Generate professional resumes.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "resume",
            "builder",
            "cv",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ResumeBuilderRequest

    async def execute(
        self,
        context: ToolContext,
        request: ResumeBuilderRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # ResumeTemplate.render(...)
        #
        # PDFReportTool.execute(...)
        #
        # DOCXGenerator.generate(...)
        #

        resume = {

            "personal_information":

                request.personal_information,

            "education":

                request.education,

            "experience":

                request.experience,

            "skills":

                request.skills,

            "projects":

                request.projects,

            "status":

                "resume_generation_pending",

            "message": (

                "Resume generation will be "

                "performed during "

                "integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Resume data prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "resume": resume,

                **response.model_dump(),

            },

        )