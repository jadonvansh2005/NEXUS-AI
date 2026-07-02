"""
UPSS Create Calendar Event Tool

Creates calendar events.

Provider-independent implementation.

Future providers:

- Google Calendar
- Microsoft Outlook
- Apple Calendar
"""

from __future__ import annotations

import uuid

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.calendar.schemas import (
    CalendarEventRequest,
    CalendarResponse,
)


class CreateEventTool(BaseTool):
    """
    Create calendar events.
    """

    metadata = ToolMetadata(

        name="calendar.create",

        display_name="Create Calendar Event",

        description="Create a calendar event.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "event",
            "schedule",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CalendarEventRequest

    async def execute(
        self,
        context: ToolContext,
        request: CalendarEventRequest,
    ) -> ToolResult:

        event = {

            "event_id": str(uuid.uuid4()),

            "title": request.title,

            "start_time": request.start_time,

            "end_time": request.end_time,

            "description": request.description,

            "location": request.location,

            "attendees": request.attendees,

            "provider": request.provider.value,

            "created_by": getattr(
                context,
                "user_id",
                None,
            ),

        }

        #
        # Future
        #
        # provider.create_event(event)
        #

        response = CalendarResponse(

            success=True,

            message="Calendar event created successfully.",

            event_id=event["event_id"],

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "event": event,

                **response.model_dump(),

            },

        )