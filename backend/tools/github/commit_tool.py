"""
UPSS Commit Tool

Create Git commits.

Provider-independent implementation.

Future providers:

- Git CLI
- GitPython
- GitHub Desktop
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
    CommitRequest,
    GitHubResponse,
)


class CommitTool(BaseTool):
    """
    Create a Git commit.
    """

    metadata = ToolMetadata(

        name="github.commit",

        display_name="Git Commit",

        description="Create a Git commit.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "git",
            "commit",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CommitRequest

    async def execute(
        self,
        context: ToolContext,
        request: CommitRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider.commit(
        #     repository_path=request.repository_path,
        #     message=request.message,
        # )
        #

        commit = {

            "commit_hash": uuid.uuid4().hex[:12],

            "repository_path": request.repository_path,

            "message": request.message,

            "author": getattr(
                context,
                "user_id",
                "system",
            ),

            "status": "created",

            "provider": request.provider.value,

        }

        response = GitHubResponse(

            success=True,

            message="Commit created successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "commit": commit,

                **response.model_dump(),

            },

        )