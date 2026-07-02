"""
UPSS WhatsApp Tool

Send WhatsApp messages.

Future integrations:

- WhatsApp Business API
- Twilio WhatsApp
- Meta Graph API
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
    WhatsAppRequest,
    CommunicationResponse,
)


class WhatsAppTool(BaseTool):
    """
    Send WhatsApp messages.
    """

    metadata = ToolMetadata(

        name="communication.whatsapp",

        display_name="WhatsApp",

        description="Send WhatsApp messages.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "communication",
            "whatsapp",
            "messaging",
            "delivery",
        ],

    )

    #
    # Sending messages changes the outside world.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = WhatsAppRequest

    async def execute(
        self,
        context: ToolContext,
        request: WhatsAppRequest,
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
        # WhatsApp Business API
        #
        # Twilio WhatsApp
        #
        # Meta Graph API
        #

        result = {

            "recipient":

                request.recipient,

            "message_length":

                len(request.message),

            "status":

                "whatsapp_delivery_pending",

            "message": (

                "WhatsApp delivery will "

                "be performed after "

                "provider integration "

                "and user approval."

            ),

        }

        response = CommunicationResponse(

            success=True,

            message="WhatsApp request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "whatsapp": result,

                **response.model_dump(),

            },

        )