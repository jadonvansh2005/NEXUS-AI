"""
UPSS Tax Estimator Tool

Estimate income tax.

Future integrations:

- Country Tax Engine
- Government Tax APIs
- Financial Planner Tool
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
    TaxEstimatorRequest,
    FinanceResponse,
)


class TaxEstimatorTool(BaseTool):
    """
    Estimate income tax.
    """

    metadata = ToolMetadata(

        name="finance.tax_estimator",

        display_name="Tax Estimator",

        description="Estimate income tax based on user financial information.",

        category=ToolCategory.FINANCE,

        tags=[
            "finance",
            "tax",
            "income-tax",
            "planning",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = TaxEstimatorRequest

    async def execute(
        self,
        context: ToolContext,
        request: TaxEstimatorRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # tax_engine = TaxEngineFactory.get(
        #     request.country
        # )
        #
        # estimate = tax_engine.calculate(
        #     annual_income=request.annual_income,
        # )
        #
        # FinancialPlannerTool.execute(...)
        #
        # FinancialReportTool.execute(...)
        #

        result = {

            "annual_income":

                request.annual_income,

            "country":

                request.country,

            "status":

                "tax_estimation_pending",

            "message": (

                "Tax estimation will "

                "be performed after "

                "country-specific tax "

                "engine integration."

            ),

        }

        response = FinanceResponse(

            success=True,

            message="Tax estimation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "tax_estimation": result,

                **response.model_dump(),

            },

        )