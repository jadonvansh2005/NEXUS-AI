"""
UPSS Reminder Tool

Creates reminder requests.

Scheduling is delegated to the notification
scheduler service.
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

from tools.notifications.schemas import (
    ReminderRequest,
    NotificationResponse,
)


class ReminderTool(BaseTool):
    """
    Create reminder requests.

    Actual scheduling is handled by the
    reminder service.
    """

    metadata = ToolMetadata(

        name="notification.reminder",

        display_name="Reminder",

        description="Create reminder.",

        category=ToolCategory.NOTIFICATION,

        tags=[
            "notification",
            "reminder",
            "scheduler",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = ReminderRequest

    async def execute(
        self,
        context: ToolContext,
        request: ReminderRequest,
    ) -> ToolResult:

        reminder = {

            "id": str(uuid.uuid4()),

            "title": request.title,

            "message": request.message,

            "priority": request.priority.value,

            "reminder_time": request.reminder_time,

            "user_id": context.user_id,

        }

        #
        # Future
        #
        # reminder_service.schedule(
        #     reminder
        # )
        #

        response = NotificationResponse(

            success=True,

            message="Reminder created successfully.",

            notification_id=reminder["id"],

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "reminder": reminder,

                **response.model_dump(),

            },

        )