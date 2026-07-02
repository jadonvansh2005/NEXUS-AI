"""
UPSS Push Notification Tool

Sends push notifications to mobile/web devices.
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

from tools.notifications.schemas import (
    PushNotificationRequest,
    NotificationResponse,
)


class PushNotificationTool(BaseTool):
    """
    Send push notifications.

    NOTE:
    This is a provider-independent implementation.
    Later this tool can integrate with:

    - Firebase Cloud Messaging (FCM)
    - OneSignal
    - AWS SNS
    - APNs
    """

    metadata = ToolMetadata(

        name="notification.push",

        display_name="Push Notification",

        description="Send push notifications.",

        category=ToolCategory.NOTIFICATION,

        tags=[
            "notification",
            "push",
            "mobile",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = PushNotificationRequest

    async def execute(
        self,
        context: ToolContext,
        request: PushNotificationRequest,
    ) -> ToolResult:

        # --------------------------------------------------
        # Placeholder for provider integration
        # --------------------------------------------------

        payload = {

            "title": request.title,

            "message": request.message,

            "priority": request.priority.value,

            "device_token": request.device_token,

        }

        # TODO:
        #
        # provider.send(payload)
        #

        response = NotificationResponse(

            success=True,

            message="Push notification request prepared successfully.",

            notification_id=None,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "payload": payload,

                **response.model_dump(),

            },

        )