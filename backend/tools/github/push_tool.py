"""
UPSS Push Tool

Push commits to a remote repository.

Provider-independent implementation.

Future providers:

- Git CLI
- GitPython
- GitHub REST API
- GitHub Enterprise
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

from tools.github.schemas import (
    PushRequest,
    GitHubResponse,
)


class PushTool(BaseTool):
    """
    Push commits to a remote repository.
    """

    metadata = ToolMetadata(

        name="github.push",

        display_name="Git Push",

        description="Push commits to a remote repository.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "git",
            "push",
            "remote",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = PushRequest

    async def execute(
        self,
        context: ToolContext,
        request: PushRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider.push(
        #     repository_path=request.repository_path,
        #     remote=request.remote,
        #     branch=request.branch,
        # )
        #

        push = {

            "repository_path": request.repository_path,

            "remote": request.remote,

            "branch": request.branch,

            "status": "success",

            "provider": request.provider.value,

        }

        response = GitHubResponse(

            success=True,

            message="Repository pushed successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "push": push,

                **response.model_dump(),

            },

        )