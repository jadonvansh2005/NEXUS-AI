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

        category=ToolCategory.GITHUB,

        tags=[
            "github",
            "git",
            "commit",
        ],

    )

    permission = ToolPermission.write()

    input_model = CommitRequest

    async def execute(
        self,
        context: ToolContext,
        request: CommitRequest,
    ) -> ToolResult:

        import subprocess
        import re
        import uuid
        from pathlib import Path

        repo_path = Path(request.repository_path)
        if not repo_path.exists():
            return ToolResult.error(f"Repository path does not exist: {repo_path}")

        success = True
        err_output = ""
        commit_hash = ""
        try:
            # Stage all changes
            subprocess.run(["git", "add", "-A"], cwd=str(repo_path), capture_output=True, text=True, check=True)
            # Commit changes
            res = subprocess.run(["git", "commit", "-m", request.message], cwd=str(repo_path), capture_output=True, text=True, check=True)
            
            # Parse commit hash
            match = re.search(r'\[\w+\s+([0-9a-fA-F]+)\]', res.stdout)
            commit_hash = match.group(1) if match else "local-commit"
            message = "Commit created successfully via Git CLI."
        except Exception as e:
            # Return failure if nothing to commit or git error
            message = f"Failed to create commit (possibly no changes to commit): {e}"
            success = False
            err_output = str(e)
            commit_hash = uuid.uuid4().hex[:12]

        commit = {
            "commit_hash": commit_hash,
            "repository_path": request.repository_path,
            "message": request.message,
            "author": getattr(context, "user_id", "system"),
            "status": "created" if success else "failed",
            "provider": "Git CLI",
        }

        response = GitHubResponse(
            success=success,
            message=message,
            provider="Git CLI",
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "commit": commit,
                "error": err_output,
                **response.model_dump(),
            },
        )