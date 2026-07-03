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

        category=ToolCategory.GITHUB,

        tags=[
            "github",
            "git",
            "clone",
            "repository",
        ],

    )

    permission = ToolPermission.write()

    input_model = CloneRepositoryRequest

    async def execute(
        self,
        context: ToolContext,
        request: CloneRepositoryRequest,
    ) -> ToolResult:

        import subprocess
        from pathlib import Path

        destination = Path(request.destination)
        destination.mkdir(parents=True, exist_ok=True)

        repository_name = (
            request.repository.rstrip("/")
            .split("/")[-1]
            .replace(".git", "")
        )

        local_repository = destination / repository_name

        # If folder exists and is not empty, skip cloning to prevent errors
        if local_repository.exists() and any(local_repository.iterdir()):
            msg = f"Repository already exists at {local_repository}."
            return ToolResult.ok(
                message=msg,
                data={
                    "repository": request.repository,
                    "local_path": str(local_repository.resolve()),
                    "success": True,
                    "message": msg,
                    "provider": "Git CLI",
                },
            )

        success = True
        err_output = ""
        try:
            # Execute subprocess git clone
            cmd = ["git", "clone", request.repository, str(local_repository)]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            message = "Repository cloned successfully via Git CLI."
        except Exception as e:
            # Fallback if git fails (e.g. auth required or network error)
            message = f"Failed to clone repository: {e}"
            success = False
            err_output = str(e)
            local_repository.mkdir(exist_ok=True)  # Create local dir as fallback placeholder

        response = GitHubResponse(
            success=success,
            message=message,
            provider="Git CLI",
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "repository": request.repository,
                "local_path": str(local_repository.resolve()),
                "error": err_output,
                **response.model_dump(),
            },
        )