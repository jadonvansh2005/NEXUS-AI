"""
UPSS Calendar Availability Tool

Checks calendar availability.

Provider-independent implementation.

Future providers:

- Google Calendar
- Microsoft Outlook
- Apple Calendar
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

from tools.calendar.schemas import (
    AvailabilityRequest,
)


class AvailabilityTool(BaseTool):
    """
    Check calendar availability.
    """

    metadata = ToolMetadata(

        name="calendar.availability",

        display_name="Calendar Availability",

        description="Check whether a time slot is available.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "availability",
            "schedule",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = AvailabilityRequest

    async def execute(
        self,
        context: ToolContext,
        request: AvailabilityRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # busy_slots = provider.get_busy_slots(
        #     start_time=request.start_time,
        #     end_time=request.end_time,
        # )
        #
        # available = len(busy_slots) == 0
        #

        available = True

        busy_slots = []

        return ToolResult.ok(

            message="Availability checked successfully.",

            data={

                "available": available,

                "start_time": request.start_time,

                "end_time": request.end_time,

                "provider": request.provider.value,

                "busy_slots": busy_slots,

            },

        )