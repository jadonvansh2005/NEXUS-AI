"""
UPSS SMS Notification Tool

Sends SMS notifications.

Provider-independent implementation.

Later providers:

- Twilio
- MSG91
- Vonage
- AWS SNS
- Textlocal
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
    SMSNotificationRequest,
    NotificationResponse,
)


class SMSNotificationTool(BaseTool):
    """
    Send SMS notifications.
    """

    metadata = ToolMetadata(

        name="notification.sms",

        display_name="SMS Notification",

        description="Send SMS notifications.",

        category=ToolCategory.NOTIFICATION,

        tags=[
            "notification",
            "sms",
            "mobile",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = SMSNotificationRequest

    async def execute(
        self,
        context: ToolContext,
        request: SMSNotificationRequest,
    ) -> ToolResult:

        payload = {

            "id": str(uuid.uuid4()),

            "phone_number": request.phone_number,

            "title": request.title,

            "message": request.message,

            "priority": request.priority.value,

        }

        #
        # Future Provider Integration
        #
        # sms_provider.send(
        #     payload
        # )
        #

        response = NotificationResponse(

            success=True,

            message="SMS notification request created successfully.",

            notification_id=payload["id"],

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "payload": payload,

                **response.model_dump(),

            },

        )