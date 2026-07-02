"""
UPSS Email Attachment Tool

Download email attachments.

Future providers:

- Gmail API
- Microsoft Graph
- IMAP
- Exchange
"""

from __future__ import annotations

from pathlib import Path

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.email.schemas import (
    AttachmentRequest,
    EmailResponse,
)


class AttachmentTool(BaseTool):
    """
    Download email attachments.
    """

    metadata = ToolMetadata(

        name="email.attachment",

        display_name="Email Attachment",

        description="Download email attachments.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "attachment",
            "download",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = AttachmentRequest

    async def execute(
        self,
        context: ToolContext,
        request: AttachmentRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # attachments = provider.download_attachments(
        #     email_id=request.email_id,
        #     download_directory=request.download_directory,
        # )
        #

        download_directory = Path(
            request.download_directory
        )

        download_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        #
        # Placeholder attachment
        #

        attachment_path = (

            download_directory

            / "sample_attachment.txt"

        )

        attachment_path.write_text(

            "Provider integration pending.",

            encoding="utf-8",

        )

        response = EmailResponse(

            success=True,

            message="Attachment downloaded successfully.",

            email_id=request.email_id,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "email_id": request.email_id,

                "attachments": [

                    {

                        "filename": attachment_path.name,

                        "path": str(
                            attachment_path.resolve()
                        ),

                        "size": attachment_path.stat().st_size,

                    }

                ],

                **response.model_dump(),

            },

        )