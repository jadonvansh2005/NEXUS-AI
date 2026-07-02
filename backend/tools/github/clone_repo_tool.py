"""
UPSS Clone Repository Tool

Clone GitHub repositories.

Provider-independent implementation.

Future providers:

- Git CLI
- GitPython
- GitHub REST API
- GitHub Enterprise
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

from tools.github.schemas import (
    CloneRepositoryRequest,
    GitHubResponse,
)


class CloneRepositoryTool(BaseTool):
    """
    Clone a GitHub repository.
    """

    metadata = ToolMetadata(

        name="github.clone",

        display_name="Clone Repository",

        description="Clone a GitHub repository.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "git",
            "clone",
            "repository",
        ],

    )

    permission = ToolPermission.requires_confirmation()

    input_model = CloneRepositoryRequest

    async def execute(
        self,
        context: ToolContext,
        request: CloneRepositoryRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider.clone_repository(
        #     repository=request.repository,
        #     destination=request.destination,
        # )
        #

        destination = Path(
            request.destination
        )

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        repository_name = (
            request.repository.rstrip("/")
            .split("/")[-1]
            .replace(".git", "")
        )

        local_repository = (
            destination / repository_name
        )

        #
        # Placeholder
        #

        local_repository.mkdir(
            exist_ok=True,
        )

        response = GitHubResponse(

            success=True,

            message="Repository cloned successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "repository": request.repository,

                "local_path": str(
                    local_repository.resolve()
                ),

                **response.model_dump(),

            },

        )