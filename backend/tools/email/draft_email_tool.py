"""
UPSS Draft Email Tool

Creates email drafts.

No email is sent from this tool.
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
    DraftEmailRequest,
    EmailResponse,
)


class DraftEmailTool(BaseTool):
    """
    Create an email draft.

    This tool only prepares an email.
    Actual sending is handled by
    SendEmailTool after user approval.
    """

    metadata = ToolMetadata(

        name="email.draft",

        display_name="Draft Email",

        description="Create an email draft.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "draft",
            "communication",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DraftEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: DraftEmailRequest,
    ) -> ToolResult:

        draft = {

            "draft_id": str(uuid.uuid4()),

            "to": request.to,

            "cc": request.cc,

            "bcc": request.bcc,

            "subject": request.subject,

            "body": request.body,

            "html": request.html,

            "priority": request.priority.value,

            "created_by": getattr(
                context,
                "user_id",
                None,
            ),

        }

        #
        # Future:
        #
        # DraftStorage.save(draft)
        #

        response = EmailResponse(

            success=True,

            message="Email draft created successfully.",

            email_id=draft["draft_id"],

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "draft": draft,

                **response.model_dump(),

            },

        )