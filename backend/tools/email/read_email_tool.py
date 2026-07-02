"""
UPSS Read Email Tool

Reads an email using the configured provider.

Future providers:

- Gmail API
- IMAP
- Microsoft Graph
- Exchange
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

from tools.email.schemas import (
    ReadEmailRequest,
    EmailResponse,
)


class ReadEmailTool(BaseTool):
    """
    Read an email.
    """

    metadata = ToolMetadata(

        name="email.read",

        display_name="Read Email",

        description="Read an email.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "read",
            "communication",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ReadEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: ReadEmailRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # email = provider.read_email(
        #     request.email_id
        # )
        #

        email = {

            "id": request.email_id,

            "from": "sender@example.com",

            "to": [

                "user@example.com",

            ],

            "cc": [],

            "bcc": [],

            "subject": "Sample Email",

            "body": "This is a placeholder email. Integrate your provider here.",

            "html": False,

            "attachments": [],

        }

        response = EmailResponse(

            success=True,

            message="Email retrieved successfully.",

            email_id=request.email_id,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "email": email,

                **response.model_dump(),

            },

        )