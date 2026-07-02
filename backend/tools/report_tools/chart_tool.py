"""
UPSS Chart Tool

Generate charts for reports.

Supports:

- Bar
- Line
- Scatter
- Pie
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.report_tools.schemas import (
    ChartRequest,
    ReportResponse,
)


class ChartTool(BaseTool):
    """
    Generate charts.
    """

    metadata = ToolMetadata(

        name="report.chart",

        display_name="Chart Generator",

        description="Generate charts for reports.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "chart",
            "plot",
            "graph",
            "visualization",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ChartRequest

    async def execute(
        self,
        context: ToolContext,
        request: ChartRequest,
    ) -> ToolResult:

        output_path = Path(
            request.output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not request.data:

            return ToolResult.failure(
                message="No chart data provided."
            )

        x = [
            row.get("x")
            for row in request.data
        ]

        y = [
            row.get("y")
            for row in request.data
        ]

        plt.figure(figsize=(8, 5))

        chart = request.chart_type.lower()

        if chart == "bar":

            plt.bar(
                x,
                y,
            )

        elif chart == "line":

            plt.plot(
                x,
                y,
            )

        elif chart == "scatter":

            plt.scatter(
                x,
                y,
            )

        elif chart == "pie":

            plt.pie(
                y,
                labels=x,
                autopct="%1.1f%%",
            )

        else:

            return ToolResult.failure(

                message=f"Unsupported chart type: {chart}"

            )

        plt.title(
            request.title
        )

        if chart != "pie":

            plt.xlabel("X")

            plt.ylabel("Y")

            plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_path
        )

        plt.close()

        response = ReportResponse(

            success=True,

            message="Chart generated successfully.",

            output_path=str(
                output_path.resolve()
            ),

        )

        return ToolResult.ok(

            message=response.message,

            data=response.model_dump(),

        )