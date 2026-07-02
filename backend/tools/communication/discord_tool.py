"""
UPSS Discord Tool

Send messages to Discord channels.

Future integrations:

- Discord Bot API
- Discord Webhooks
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
    DiscordRequest,
    CommunicationResponse,
)


class DiscordTool(BaseTool):
    """
    Send Discord messages.
    """

    metadata = ToolMetadata(

        name="communication.discord",

        display_name="Discord",

        description="Send messages to Discord channels.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "communication",
            "discord",
            "messaging",
            "delivery",
        ],

    )

    #
    # Sending messages changes the outside world.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = DiscordRequest

    async def execute(
        self,
        context: ToolContext,
        request: DiscordRequest,
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
        # Discord Bot API
        #
        # Discord Webhook
        #

        result = {

            "channel_id":

                request.channel_id,

            "message_length":

                len(request.message),

            "status":

                "discord_delivery_pending",

            "message": (

                "Discord delivery will "

                "be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = CommunicationResponse(

            success=True,

            message="Discord request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "discord": result,

                **response.model_dump(),

            },

        )