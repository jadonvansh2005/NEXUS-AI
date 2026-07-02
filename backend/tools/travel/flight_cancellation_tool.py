"""
UPSS Flight Cancellation Tool

Cancel existing flight bookings.

Future integrations:

- Flight Booking Tool
- Amadeus
- Skyscanner
- Kiwi
- Airline APIs
- Refund Engine
- HITL Approval
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
    FlightCancellationRequest,
    TravelResponse,
)


class FlightCancellationTool(BaseTool):
    """
    Cancel flight bookings.
    """

    metadata = ToolMetadata(

        name="travel.flight_cancellation",

        display_name="Flight Cancellation",

        description="Cancel existing flight reservations.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "flight",
            "cancel",
            "refund",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = FlightCancellationRequest

    async def execute(
        self,
        context: ToolContext,
        request: FlightCancellationRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # HITL Approval
        #
        # BookingProvider.get_booking(...)
        #
        # AirlineAPI.cancel_booking(...)
        #
        # RefundEngine.calculate(...)
        #
        # NotificationTool.send(...)
        #

        result = {

            "booking_reference":

                request.booking_reference,

            "provider":

                request.provider,

            "status":

                "flight_cancellation_pending",

            "message": (

                "Flight cancellation "

                "will be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = TravelResponse(

            success=True,

            message="Flight cancellation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "flight_cancellation": result,

                **response.model_dump(),

            },

        )