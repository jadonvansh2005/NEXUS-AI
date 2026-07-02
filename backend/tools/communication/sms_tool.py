"""
UPSS SMS Tool

Send SMS messages.

Future integrations:

- Twilio
- AWS SNS
- Vonage (Nexmo)
- MessageBird
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
    SMSRequest,
    CommunicationResponse,
)


class SMSTool(BaseTool):
    """
    Send SMS messages.
    """

    metadata = ToolMetadata(

        name="communication.sms",

        display_name="SMS",

        description="Send SMS messages.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "communication",
            "sms",
            "messaging",
            "delivery",
        ],

    )

    #
    # Sending SMS modifies the outside world.
    #

    permission = ToolPermission.requires_confirmation()

    input_model = SMSRequest

    async def execute(
        self,
        context: ToolContext,
        request: SMSRequest,
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
        # Twilio API
        #
        # AWS SNS
        #
        # Vonage API
        #
        # MessageBird API
        #

        result = {

            "phone_number":

                request.phone_number,

            "message_length":

                len(request.message),

            "status":

                "sms_delivery_pending",

            "message": (

                "SMS delivery will "

                "be performed after "

                "SMS provider integration "

                "and user approval."

            ),

        }

        response = CommunicationResponse(

            success=True,

            message="SMS request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "sms": result,

                **response.model_dump(),

            },

        )