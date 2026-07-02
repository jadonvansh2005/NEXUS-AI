"""
UPSS Update Calendar Event Tool

Updates an existing calendar event.

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
    CalendarUpdateRequest,
    CalendarResponse,
)


class UpdateEventTool(BaseTool):
    """
    Update an existing calendar event.
    """

    metadata = ToolMetadata(

        name="calendar.update",

        display_name="Update Calendar Event",

        description="Update an existing calendar event.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "update",
            "event",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CalendarUpdateRequest

    async def execute(
        self,
        context: ToolContext,
        request: CalendarUpdateRequest,
    ) -> ToolResult:

        updated_event = {

            "event_id": request.event_id,

            "title": request.title,

            "start_time": request.start_time,

            "end_time": request.end_time,

            "description": request.description,

            "location": request.location,

            "attendees": request.attendees,

            "provider": request.provider.value,

            "updated_by": getattr(
                context,
                "user_id",
                None,
            ),

        }

        #
        # Future Provider Integration
        #
        # provider.update_event(updated_event)
        #

        response = CalendarResponse(

            success=True,

            message="Calendar event updated successfully.",

            event_id=request.event_id,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "event": updated_event,

                **response.model_dump(),

            },

        )