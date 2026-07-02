"""
UPSS Interview Questions Tool

Generate interview questions.

Future integrations:

- LLM
- Company Research
- Role Analyzer
- Coding Interview Generator
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
    InterviewQuestionsRequest,
    CareerResponse,
)


class InterviewQuestionsTool(BaseTool):
    """
    Generate interview questions.
    """

    metadata = ToolMetadata(

        name="career.interview_questions",

        display_name="Interview Questions",

        description="Generate interview questions for a target role.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "interview",
            "questions",
            "preparation",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = InterviewQuestionsRequest

    async def execute(
        self,
        context: ToolContext,
        request: InterviewQuestionsRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # company = CompanyResearch(...)
        #
        # role = RoleAnalyzer(...)
        #
        # questions = LLM.generate_questions(
        #     role=request.role,
        #     experience=request.experience_level,
        #     limit=request.number_of_questions,
        # )
        #

        result = {

            "role": request.role,

            "experience_level": request.experience_level,

            "number_of_questions": request.number_of_questions,

            "status": "question_generation_pending",

            "message": (

                "Interview questions will "

                "be generated after "

                "LLM integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Interview question request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "interview": result,

                **response.model_dump(),

            },

        )