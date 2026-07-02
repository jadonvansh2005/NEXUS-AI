"""
UPSS GitHub Issue Tool

Create GitHub Issues.

Provider-independent implementation.

Future providers:

- GitHub REST API
- GitHub GraphQL API
- GitHub Enterprise
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

from tools.github.schemas import (
    IssueRequest,
    GitHubResponse,
)


class IssueTool(BaseTool):
    """
    Create GitHub Issues.
    """

    metadata = ToolMetadata(

        name="github.issue",

        display_name="Create GitHub Issue",

        description="Create a GitHub issue.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "issue",
            "bug",
            "feature",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = IssueRequest

    async def execute(
        self,
        context: ToolContext,
        request: IssueRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # issue = provider.create_issue(
        #     repository=request.repository,
        #     title=request.title,
        #     body=request.body,
        #     labels=request.labels,
        # )
        #

        issue = {

            "id": str(uuid.uuid4()),

            "repository": request.repository,

            "title": request.title,

            "body": request.body,

            "labels": request.labels,

            "status": "open",

            "url": (

                f"https://github.com/"
                f"{request.repository}"
                f"/issues/1"

            ),

            "provider": request.provider.value,

            "created_by": getattr(
                context,
                "user_id",
                None,
            ),

        }

        response = GitHubResponse(

            success=True,

            message="GitHub issue created successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "issue": issue,

                **response.model_dump(),

            },

        )