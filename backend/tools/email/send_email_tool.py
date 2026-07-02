"""
UPSS Send Email Tool

Provider-independent email sender.

Later providers can include:

- SMTP
- Gmail API
- Microsoft Graph
- Exchange
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

from tools.email.schemas import (
    SendEmailRequest,
    EmailResponse,
)


class SendEmailTool(BaseTool):
    """
    Send emails.

    Actual delivery is delegated to the configured
    email provider.
    """

    metadata = ToolMetadata(

        name="email.send",

        display_name="Send Email",

        description="Send email using configured provider.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "send",
            "communication",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = SendEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: SendEmailRequest,
    ) -> ToolResult:

        payload = {

            "id": str(uuid.uuid4()),

            "to": request.to,

            "cc": request.cc,

            "bcc": request.bcc,

            "subject": request.subject,

            "body": request.body,

            "html": request.html,

            "priority": request.priority.value,

            "attachments": request.attachments,

        }

        #
        # Future Provider Integration
        #
        # provider.send(payload)
        #
        # SMTPProvider
        # GmailProvider
        # OutlookProvider
        #

        response = EmailResponse(

            success=True,

            message="Email request created successfully.",

            email_id=payload["id"],

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "payload": payload,

                **response.model_dump(),

            },

        )