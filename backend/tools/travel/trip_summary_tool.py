"""
UPSS Trip Summary Tool

Create a consolidated travel summary.

This tool combines outputs from:

- Itinerary
- Flights
- Hotels
- Budget
- Nearby Places

Future:

Can directly feed into
PDFReportTool.
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
    TripSummaryRequest,
    TravelResponse,
)


class TripSummaryTool(BaseTool):
    """
    Build a travel summary.
    """

    metadata = ToolMetadata(

        name="travel.trip_summary",

        display_name="Trip Summary",

        description="Generate a complete travel summary.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "summary",
            "trip",
            "report",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = TripSummaryRequest

    async def execute(
        self,
        context: ToolContext,
        request: TripSummaryRequest,
    ) -> ToolResult:

        summary = {

            "destination": request.itinerary.get(
                "destination"
            ),

            "travel_days": request.itinerary.get(
                "total_days"
            ),

            "flight_count": len(
                request.flights
            ),

            "hotel_count": len(
                request.hotels
            ),

            "budget": request.budget,

            "itinerary": request.itinerary,

            "flights": request.flights,

            "hotels": request.hotels,

        }

        response = TravelResponse(

            success=True,

            message="Trip summary generated successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "summary": summary,

                **response.model_dump(),

            },

        )