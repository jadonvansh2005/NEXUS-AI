"""
UPSS List Calendar Events Tool

Lists calendar events.

Provider-independent implementation.

Future providers:

- Google Calendar
- Microsoft Outlook
- Apple Calendar
"""

from __future__ import annotations

from datetime import timedelta

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.calendar.schemas import (
    CalendarListRequest,
    CalendarResponse,
)


class ListEventsTool(BaseTool):
    """
    List calendar events.
    """

    metadata = ToolMetadata(

        name="calendar.list",

        display_name="List Calendar Events",

        description="List calendar events.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "list",
            "events",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CalendarListRequest

    async def execute(
        self,
        context: ToolContext,
        request: CalendarListRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # events = provider.list_events(
        #     start_time=request.start_time,
        #     end_time=request.end_time,
        # )
        #

        events = []

        if request.start_time and request.end_time:

            events.append(

                {

                    "event_id": "sample-event-001",

                    "title": "Sample Meeting",

                    "start_time": request.start_time,

                    "end_time": min(

                        request.start_time + timedelta(hours=1),

                        request.end_time,

                    ),

                    "location": "Conference Room",

                    "description": "Placeholder calendar event.",

                    "attendees": [],

                    "provider": request.provider.value,

                }

            )

        response = CalendarResponse(

            success=True,

            message="Calendar events retrieved successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "count": len(events),

                "events": events,

                **response.model_dump(),

            },

        )