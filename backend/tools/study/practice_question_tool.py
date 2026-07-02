"""
UPSS Practice Question Tool

Generate practice questions for educational topics.

Future integrations:

- LLM
- Concept Explainer Tool
- Quiz Generator Tool
- Research Tool
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
    PracticeQuestionRequest,
    StudyResponse,
)


class PracticeQuestionTool(BaseTool):
    """
    Generate practice questions.
    """

    metadata = ToolMetadata(

        name="study.practice_questions",

        display_name="Practice Questions",

        description="Generate practice questions for learning reinforcement.",

        category=ToolCategory.EDUCATION,

        tags=[
            "study",
            "practice",
            "questions",
            "education",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PracticeQuestionRequest

    async def execute(
        self,
        context: ToolContext,
        request: PracticeQuestionRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # concepts = ConceptExplainerTool.execute(...)
        #
        # quiz = QuizGeneratorTool.execute(...)
        #
        # research = WebResearchTool.execute(...)
        #
        # questions = LLM.generate_practice_questions(
        #     topic=request.topic,
        #     difficulty=request.difficulty,
        #     count=request.count,
        # )
        #

        result = {

            "topic": request.topic,

            "difficulty": request.difficulty,

            "count": request.count,

            "status": "practice_question_generation_pending",

            "message": (

                "Practice question generation "

                "will be performed after "

                "LLM integration."

            ),

        }

        response = StudyResponse(

            success=True,

            message="Practice question request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "practice_questions": result,

                **response.model_dump(),

            },

        )