"""
UPSS Search Email Tool

Search emails using the configured provider.

Future providers:

- Gmail API
- Microsoft Graph
- IMAP
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
    SearchEmailRequest,
    EmailResponse,
)


class SearchEmailTool(BaseTool):
    """
    Search emails.
    """

    metadata = ToolMetadata(

        name="email.search",

        display_name="Search Email",

        description="Search emails using the configured provider.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "search",
            "communication",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = SearchEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: SearchEmailRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # results = provider.search(
        #     query=request.query,
        #     limit=request.limit,
        # )
        #

        results = [

            {

                "id": "email_001",

                "from": "careers@microsoft.com",

                "subject": "Internship Interview",

                "snippet": "Congratulations! Your interview has been scheduled.",

                "date": "2026-06-30",

            },

            {

                "id": "email_002",

                "from": "noreply@github.com",

                "subject": "Security Alert",

                "snippet": "A new sign-in to your GitHub account was detected.",

                "date": "2026-06-29",

            },

        ][: request.limit]

        response = EmailResponse(

            success=True,

            message="Email search completed successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "query": request.query,

                "count": len(results),

                "results": results,

                **response.model_dump(),

            },

        )