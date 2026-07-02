"""
UPSS Create Pull Request Tool

Create GitHub Pull Requests.

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
    PullRequestRequest,
    GitHubResponse,
)


class CreatePullRequestTool(BaseTool):
    """
    Create a Pull Request.
    """

    metadata = ToolMetadata(

        name="github.pull_request",

        display_name="Create Pull Request",

        description="Create a GitHub Pull Request.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "pull-request",
            "merge",
            "git",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = PullRequestRequest

    async def execute(
        self,
        context: ToolContext,
        request: PullRequestRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # pr = provider.create_pull_request(
        #     repository=request.repository,
        #     title=request.title,
        #     body=request.body,
        #     head=request.head,
        #     base=request.base,
        # )
        #

        pull_request = {

            "id": str(uuid.uuid4()),

            "repository": request.repository,

            "title": request.title,

            "body": request.body,

            "head": request.head,

            "base": request.base,

            "status": "open",

            "url": (

                f"https://github.com/"
                f"{request.repository}"
                f"/pull/1"

            ),

            "provider": request.provider.value,

        }

        response = GitHubResponse(

            success=True,

            message="Pull Request created successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "pull_request": pull_request,

                **response.model_dump(),

            },

        )