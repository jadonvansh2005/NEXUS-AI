"""
UPSS Slack Tool

Send messages to Slack channels.

Future integrations:

- Slack Web API
- Slack Bot API
- Slack Incoming Webhooks
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
    SlackRequest,
    CommunicationResponse,
)


class SlackTool(BaseTool):
    """
    Send Slack messages.
    """

    metadata = ToolMetadata(

        name="communication.slack",

        display_name="Slack",

        description="Send messages to Slack channels.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "communication",
            "slack",
            "messaging",
            "delivery",
        ],

    )

    #
    # Sending messages changes the outside world.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = SlackRequest

    async def execute(
        self,
        context: ToolContext,
        request: SlackRequest,
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
        # Slack Web API
        #
        # Slack Bot API
        #
        # Slack Incoming Webhook
        #

        result = {

            "channel":

                request.channel,

            "message_length":

                len(request.message),

            "status":

                "slack_delivery_pending",

            "message": (

                "Slack delivery will "

                "be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = CommunicationResponse(

            success=True,

            message="Slack request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "slack": result,

                **response.model_dump(),

            },

        )