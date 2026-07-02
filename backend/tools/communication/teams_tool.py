"""
UPSS Microsoft Teams Tool

Send messages to Microsoft Teams.

Future integrations:

- Microsoft Graph API
- Teams Bot Framework
- Incoming Webhooks
- Message Composer Tool
- Translator Tool
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

from tools.communication.schemas import (
    TeamsRequest,
    CommunicationResponse,
)


class TeamsTool(BaseTool):
    """
    Send Microsoft Teams messages.
    """

    metadata = ToolMetadata(

        name="communication.teams",

        display_name="Microsoft Teams",

        description="Send messages to Microsoft Teams channels.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "communication",
            "teams",
            "microsoft",
            "delivery",
        ],

    )

    #
    # Sending messages modifies the outside world.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = TeamsRequest

    async def execute(
        self,
        context: ToolContext,
        request: TeamsRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # HITL Approval
        #
        # MessageComposerTool.execute(...)
        #
        # GrammarCheckerTool.execute(...)
        #
        # ToneConverterTool.execute(...)
        #
        # TranslatorTool.execute(...)
        #
        # Microsoft Graph API
        #
        # Teams Bot Framework
        #
        # Teams Incoming Webhook
        #

        result = {

            "channel":

                request.channel,

            "message_length":

                len(request.message),

            "status":

                "teams_delivery_pending",

            "message": (

                "Teams delivery will "

                "be performed after "

                "Microsoft Teams API "

                "integration and "

                "user approval."

            ),

        }

        response = CommunicationResponse(

            success=True,

            message="Teams request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "teams": result,

                **response.model_dump(),

            },

        )