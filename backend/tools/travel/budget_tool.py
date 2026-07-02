"""
UPSS Travel Budget Tool

Estimate a travel budget.

This tool performs actual budget allocation based on
the total budget provided by the user.

Future improvements:

- Country-specific costs
- Seasonal pricing
- Dynamic hotel/flight integration
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

from tools.travel.schemas import (
    BudgetRequest,
    TravelResponse,
)


class BudgetTool(BaseTool):
    """
    Estimate a travel budget.
    """

    metadata = ToolMetadata(

        name="travel.budget",

        display_name="Budget Planner",

        description="Estimate and distribute a travel budget.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "budget",
            "finance",
            "planner",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = BudgetRequest

    async def execute(
        self,
        context: ToolContext,
        request: BudgetRequest,
    ) -> ToolResult:

        total_budget = request.total_budget

        allocation = {

            "transportation": round(
                total_budget * 0.35,
                2,
            ),

            "accommodation": round(
                total_budget * 0.30,
                2,
            ),

            "food": round(
                total_budget * 0.15,
                2,
            ),

            "activities": round(
                total_budget * 0.10,
                2,
            ),

            "local_transport": round(
                total_budget * 0.05,
                2,
            ),

            "emergency": round(
                total_budget * 0.05,
                2,
            ),

        }

        per_day = round(
            total_budget / request.days,
            2,
        )

        per_person = round(
            total_budget / request.travelers,
            2,
        )

        response = TravelResponse(

            success=True,

            message="Travel budget calculated successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "destination": request.destination,

                "days": request.days,

                "travelers": request.travelers,

                "total_budget": total_budget,

                "budget_per_day": per_day,

                "budget_per_person": per_person,

                "allocation": allocation,

                **response.model_dump(),

            },

        )