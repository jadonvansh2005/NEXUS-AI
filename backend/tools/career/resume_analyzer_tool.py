"""
UPSS Resume Analyzer Tool

Analyze resumes and extract useful information.

Future integrations:

- PDF Parser
- DOCX Parser
- OCR
- LLM
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
    ResumeAnalyzerRequest,
    CareerResponse,
)


class ResumeAnalyzerTool(BaseTool):
    """
    Analyze resumes.
    """

    metadata = ToolMetadata(

        name="career.resume_analyzer",

        display_name="Resume Analyzer",

        description="Analyze resumes and extract useful information.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "resume",
            "analysis",
            "ats",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ResumeAnalyzerRequest

    async def execute(
        self,
        context: ToolContext,
        request: ResumeAnalyzerRequest,
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
        # analysis = LLM.analyze(text)
        #
        # skills = SkillExtractor.extract(text)
        #
        # education = EducationExtractor.extract(text)
        #
        # experience = ExperienceExtractor.extract(text)
        #

        analysis = {

            "file_name": resume.name,

            "file_type": resume.suffix,

            "file_size": resume.stat().st_size,

            "status": "analysis_pending",

            "message": (

                "Resume parsing will be "

                "performed during provider "

                "integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Resume received successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "analysis": analysis,

                **response.model_dump(),

            },

        )