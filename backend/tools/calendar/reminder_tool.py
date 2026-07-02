"""
UPSS Calendar Reminder Tool

Creates reminders for calendar events.

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
    CalendarReminderRequest,
    CalendarResponse,
)


class ReminderTool(BaseTool):
    """
    Create a reminder for a calendar event.
    """

    metadata = ToolMetadata(

        name="calendar.reminder",

        display_name="Calendar Reminder",

        description="Create a reminder for a calendar event.",

        category=ToolCategory.PRODUCTIVITY,

        tags=[
            "calendar",
            "reminder",
            "notification",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CalendarReminderRequest

    async def execute(
        self,
        context: ToolContext,
        request: CalendarReminderRequest,
    ) -> ToolResult:

        reminder = {

            "reminder_id": str(uuid.uuid4()),

            "event_id": request.event_id,

            "minutes_before": request.reminder_minutes_before,

            "provider": request.provider.value,

            "created_by": getattr(
                context,
                "user_id",
                None,
            ),

        }

        #
        # Future Provider Integration
        #
        # provider.create_reminder(
        #     reminder
        # )
        #
        # Future Integration:
        #
        # NotificationService.schedule(
        #     reminder
        # )
        #

        response = CalendarResponse(

            success=True,

            message="Calendar reminder created successfully.",

            event_id=request.event_id,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "reminder": reminder,

                **response.model_dump(),

            },

        )