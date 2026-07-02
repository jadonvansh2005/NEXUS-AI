"""
UPSS PDF Report Tool

Generate generic PDF reports.

NOTE:
This tool is different from pdf_report_generator.py,
which is dedicated to Data Science / ML reports.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
)

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.report_tools.schemas import (
    PDFReportRequest,
    ReportResponse,
)


class PDFReportTool(BaseTool):
    """
    Generate generic PDF reports.
    """

    metadata = ToolMetadata(

        name="report.pdf",

        display_name="PDF Report",

        description="Generate PDF reports.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "report",
            "pdf",
            "document",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PDFReportRequest

    async def execute(
        self,
        context: ToolContext,
        request: PDFReportRequest,
    ) -> ToolResult:

        output_path = Path(
            request.output_path
        )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        document = SimpleDocTemplate(

            str(output_path)

        )

        styles = getSampleStyleSheet()

        story = [

            Paragraph(

                f"<b>{request.title}</b>",

                styles["Heading1"],

            ),

            Paragraph(

                request.content,

                styles["BodyText"],

            ),

        ]

        document.build(

            story

        )

        response = ReportResponse(

            success=True,

            message="PDF report generated successfully.",

            output_path=str(
                output_path.resolve()
            ),

        )

        return ToolResult.ok(

            message=response.message,

            data=response.model_dump(),

        )