"""
UPSS Excel Report Tool

Generate Excel reports.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.report_tools.schemas import (
    ExcelReportRequest,
    ReportResponse,
)


class ExcelReportTool(BaseTool):
    """
    Generate Excel reports.
    """

    metadata = ToolMetadata(

        name="report.excel",

        display_name="Excel Report",

        description="Generate Excel reports.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "report",
            "excel",
            "spreadsheet",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ExcelReportRequest

    async def execute(
        self,
        context: ToolContext,
        request: ExcelReportRequest,
    ) -> ToolResult:

        output_path = Path(
            request.output_path
        )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        workbook = Workbook()

        worksheet = workbook.active

        worksheet.title = request.title

        if request.data:

            worksheet.append(
                list(request.data[0].keys())
            )

            for row in request.data:

                worksheet.append(
                    list(row.values())
                )

        workbook.save(
            output_path
        )

        response = ReportResponse(

            success=True,

            message="Excel report generated successfully.",

            output_path=str(
                output_path.resolve()
            ),

        )

        return ToolResult.ok(

            message=response.message,

            data=response.model_dump(),

        )