"""
UPSS Expense Tracker Tool

Track personal expenses.

Future integrations:

- Database
- Financial Planner Tool
- Budget Planner Tool
- Financial Report Tool
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
    ExpenseTrackerRequest,
    FinanceResponse,
)


class ExpenseTrackerTool(BaseTool):
    """
    Track personal expenses.
    """

    metadata = ToolMetadata(

        name="finance.expense_tracker",

        display_name="Expense Tracker",

        description="Track and organize personal expenses.",

        category=ToolCategory.FINANCE,

        tags=[
            "finance",
            "expense",
            "budget",
            "tracking",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ExpenseTrackerRequest

    async def execute(
        self,
        context: ToolContext,
        request: ExpenseTrackerRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # ExpenseRepository.add(...)
        #
        # BudgetPlannerTool.execute(...)
        #
        # FinancialReportTool.execute(...)
        #
        # AnalyticsEngine.update(...)
        #

        result = {

            "amount": request.amount,

            "category": request.category,

            "description": request.description,

            "date": request.date,

            "status": "expense_tracking_pending",

            "message": (

                "Expense tracking will "

                "be performed after "

                "database integration."

            ),

        }

        response = FinanceResponse(

            success=True,

            message="Expense tracking request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "expense": result,

                **response.model_dump(),

            },

        )