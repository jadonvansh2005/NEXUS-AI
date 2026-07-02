"""
UPSS Desktop Notification Tool

Displays desktop notifications.
"""

from __future__ import annotations

from plyer import notification

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.notifications.schemas import (
    DesktopNotificationRequest,
    NotificationResponse,
)


class DesktopNotificationTool(BaseTool):
    """
    Send desktop notifications.
    """

    metadata = ToolMetadata(

        name="notification.desktop",

        display_name="Desktop Notification",

        description="Display a desktop notification.",

        category=ToolCategory.NOTIFICATION,

        tags=[
            "notification",
            "desktop",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DesktopNotificationRequest

    async def execute(
        self,
        context: ToolContext,
        request: DesktopNotificationRequest,
    ) -> ToolResult:

        try:

            notification.notify(

                title=request.title,

                message=request.message,

                timeout=10,

            )

            response = NotificationResponse(

                success=True,

                message="Desktop notification sent.",

            )

            return ToolResult.ok(

                message=response.message,

                data=response.model_dump(),

            )

        except Exception as exc:

            response = NotificationResponse(

                success=False,

                message=str(exc),

            )

            return ToolResult.failure(

                message=response.message,

                data=response.model_dump(),

            )