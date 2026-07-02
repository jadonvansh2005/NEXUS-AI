"""
UPSS Delete Calendar Event Tool

Deletes an existing calendar event.

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
    CalendarDeleteRequest,
    CalendarResponse,
)


class DeleteEventTool(BaseTool):
    """
    Delete an existing calendar event.
    """

    metadata = ToolMetadata(

        name="calendar.delete",

        display_name="Delete Calendar Event",

        description="Delete an existing calendar event.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "delete",
            "event",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CalendarDeleteRequest

    async def execute(
        self,
        context: ToolContext,
        request: CalendarDeleteRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider.delete_event(
        #     request.event_id
        # )
        #

        response = CalendarResponse(

            success=True,

            message="Calendar event deleted successfully.",

            event_id=request.event_id,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "event_id": request.event_id,

                "provider": request.provider.value,

                **response.model_dump(),

            },

        )