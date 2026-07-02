"""
UPSS Paper Summarizer Tool

Summarize academic research papers.

Future integrations:

- PDF Tool
- Browser Tool
- LLM
- Report Generator
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

from tools.research.schemas import (
    PaperSummarizerRequest,
    ResearchResponse,
)


class PaperSummarizerTool(BaseTool):
    """
    Summarize research papers.
    """

    metadata = ToolMetadata(

        name="research.paper_summarizer",

        display_name="Paper Summarizer",

        description="Summarize academic research papers.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "paper",
            "summary",
            "pdf",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PaperSummarizerRequest

    async def execute(
        self,
        context: ToolContext,
        request: PaperSummarizerRequest,
    ) -> ToolResult:

        paper = Path(
            request.paper_path
        )

        if not paper.exists():

            return ToolResult.failure(

                message="Paper file not found."

            )

        #
        # Future Pipeline
        #
        # text = PDFTool.extract_text(
        #     paper
        # )
        #
        # summary = LLM.summarize(
        #     text
        # )
        #
        # key_points = KeyPointExtractor(...)
        #
        # ReportGenerator.generate(...)
        #

        result = {

            "paper_name": paper.name,

            "paper_path": str(
                paper.resolve()
            ),

            "file_type": paper.suffix,

            "file_size": paper.stat().st_size,

            "status": "paper_summary_pending",

            "message": (

                "Paper summarization "

                "will be performed after "

                "PDF and LLM integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Paper summarization request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "paper_summary": result,

                **response.model_dump(),

            },

        )