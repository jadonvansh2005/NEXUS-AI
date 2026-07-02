"""
UPSS Financial Report Tool

Generate financial reports.

Future integrations:

- Report Module
- Expense Tracker Tool
- Budget Planner Tool
- Portfolio Tracker Tool
- Financial Planner Tool
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

from tools.finance.schemas import (
    FinancialReportRequest,
    FinanceResponse,
)


class FinancialReportTool(BaseTool):
    """
    Generate financial reports.
    """

    metadata = ToolMetadata(

        name="finance.financial_report",

        display_name="Financial Report",

        description="Generate comprehensive financial reports.",

        category=ToolCategory.FINANCE,

        tags=[
            "finance",
            "report",
            "analytics",
            "summary",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = FinancialReportRequest

    async def execute(
        self,
        context: ToolContext,
        request: FinancialReportRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # expenses = ExpenseTrackerTool.execute(...)
        #
        # budget = BudgetPlannerTool.execute(...)
        #
        # portfolio = PortfolioTrackerTool.execute(...)
        #
        # planner = FinancialPlannerTool.execute(...)
        #
        # ReportModule.generate(
        #     title=request.title,
        #     period=request.period,
        # )
        #

        result = {

            "title":

                request.title,

            "period":

                request.period,

            "status":

                "financial_report_pending",

            "message": (

                "Financial report generation "

                "will be performed after "

                "Report module integration."

            ),

        }

        response = FinanceResponse(

            success=True,

            message="Financial report request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "financial_report": result,

                **response.model_dump(),

            },

        )