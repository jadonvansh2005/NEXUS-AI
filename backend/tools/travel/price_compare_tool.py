"""
UPSS Price Compare Tool

Compare prices across travel options.

Future integrations:
- Google Flights
- Skyscanner
- Booking.com
- Price Engine API
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
    PriceCompareRequest,
    TravelResponse,
)


class PriceCompareTool(BaseTool):
    """
    Compare travel options pricing.
    """

    metadata = ToolMetadata(

        name="travel.price_compare",

        display_name="Price Compare",

        description="Compare prices across travel options.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "flight",
            "hotel",
            "compare",
            "price",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PriceCompareRequest

    async def execute(
        self,
        context: ToolContext,
        request: PriceCompareRequest,
    ) -> ToolResult:

        result = {

            "origin": request.origin,

            "destination": request.destination,

            "departure_date": request.departure_date,

            "status": "price_compare_pending",

            "message": (

                "Price comparison will "

                "be performed after "

                "travel provider integration."

            ),

        }

        response = TravelResponse(

            success=True,

            message="Price comparison request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "price_compare": result,

                **response.model_dump(),

            },

        )