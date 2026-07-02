"""
UPSS Booking Tool

Prepare booking requests.

Current:
    Creates a booking plan.

Future:
    Browser Automation
    Official Booking APIs
    Human-in-the-Loop Approval
"""

from __future__ import annotations

import uuid
from datetime import datetime

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.travel.schemas import (
    BookingRequest,
    TravelResponse,
)


class BookingTool(BaseTool):
    """
    Prepare booking requests.

    NOTE:
    No booking is performed yet.
    """

    metadata = ToolMetadata(

        name="travel.booking",

        display_name="Booking",

        description="Prepare travel booking requests.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "booking",
            "reservation",
        ],

    )

    #
    # Booking changes the external world.
    # Keep confirmation enabled.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = BookingRequest

    async def execute(
        self,
        context: ToolContext,
        request: BookingRequest,
    ) -> ToolResult:

        booking = {

            "booking_id": str(
                uuid.uuid4()
            ),

            "booking_type": request.booking_type,

            "provider": request.provider.value,

            "status": "pending",

            "created_at": datetime.utcnow().isoformat(),

            "details": request.details,

            "requires_confirmation": True,

        }

        response = TravelResponse(

            success=True,

            message="Booking request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "booking": booking,

                **response.model_dump(),

            },

        )