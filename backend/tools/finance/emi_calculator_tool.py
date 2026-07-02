"""
UPSS EMI Calculator Tool

Calculate Equated Monthly Installments (EMI).

Future integrations:

- Financial Planner Tool
- Financial Report Tool
- Loan Comparison Engine
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
    EMICalculatorRequest,
    FinanceResponse,
)


class EMICalculatorTool(BaseTool):
    """
    Calculate loan EMI.
    """

    metadata = ToolMetadata(

        name="finance.emi_calculator",

        display_name="EMI Calculator",

        description="Calculate Equated Monthly Installments (EMI).",

        category=ToolCategory.FINANCE,

        tags=[
            "finance",
            "emi",
            "loan",
            "calculator",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = EMICalculatorRequest

    async def execute(
        self,
        context: ToolContext,
        request: EMICalculatorRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # calculator = EMIEngine.calculate(
        #     principal=request.principal,
        #     annual_interest_rate=request.annual_interest_rate,
        #     tenure_months=request.tenure_months,
        # )
        #
        # FinancialPlannerTool.execute(...)
        #
        # FinancialReportTool.execute(...)
        #

        result = {

            "principal":

                request.principal,

            "annual_interest_rate":

                request.annual_interest_rate,

            "tenure_months":

                request.tenure_months,

            "status":

                "emi_calculation_pending",

            "message": (

                "EMI calculation will "

                "be performed after "

                "calculation engine "

                "integration."

            ),

        }

        response = FinanceResponse(

            success=True,

            message="EMI calculation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "emi": result,

                **response.model_dump(),

            },

        )