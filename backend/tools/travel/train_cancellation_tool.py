"""
UPSS Train Cancellation Tool

Cancel existing train reservations.

Future integrations:

- Train Booking Tool
- IRCTC
- Railway APIs
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
    TrainCancellationRequest,
    TravelResponse,
)


class TrainCancellationTool(BaseTool):
    """
    Cancel train reservations.
    """

    metadata = ToolMetadata(

        name="travel.train_cancellation",

        display_name="Train Cancellation",

        description="Cancel existing train reservations.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "train",
            "cancel",
            "refund",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = TrainCancellationRequest

    async def execute(
        self,
        context: ToolContext,
        request: TrainCancellationRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # HITL Approval
        #
        # TrainBookingProvider.get_booking(...)
        #
        # IRCTC.cancel_booking(...)
        #
        # RailwayAPI.cancel(...)
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

                "train_cancellation_pending",

            "message": (

                "Train cancellation "

                "will be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = TravelResponse(

            success=True,

            message="Train cancellation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "train_cancellation": result,

                **response.model_dump(),

            },

        )