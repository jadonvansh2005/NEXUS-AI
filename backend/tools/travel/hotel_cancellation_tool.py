"""
UPSS Hotel Cancellation Tool

Cancel existing hotel reservations.

Future integrations:

- Hotel Booking Tool
- Booking.com
- Agoda
- Expedia
- Hotels.com
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
    HotelCancellationRequest,
    TravelResponse,
)


class HotelCancellationTool(BaseTool):
    """
    Cancel hotel reservations.
    """

    metadata = ToolMetadata(

        name="travel.hotel_cancellation",

        display_name="Hotel Cancellation",

        description="Cancel existing hotel reservations.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "hotel",
            "cancel",
            "refund",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = HotelCancellationRequest

    async def execute(
        self,
        context: ToolContext,
        request: HotelCancellationRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # HITL Approval
        #
        # BookingProvider.get_booking(...)
        #
        # HotelProvider.cancel_booking(...)
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

                "hotel_cancellation_pending",

            "message": (

                "Hotel cancellation "

                "will be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = TravelResponse(

            success=True,

            message="Hotel cancellation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "hotel_cancellation": result,

                **response.model_dump(),

            },

        )