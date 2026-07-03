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

        category=ToolCategory.GITHUB,

        tags=[
            "github",
            "pull-request",
            "merge",
            "git",
        ],

    )

    permission = ToolPermission.write()

    input_model = PullRequestRequest

    async def execute(
        self,
        context: ToolContext,
        request: PullRequestRequest,
    ) -> ToolResult:

        import httpx
        import os
        import uuid

        token = os.getenv("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
        success = True
        provider = "Mock"
        message = "Pull Request created successfully (mock mode)."
        
        pr_data = {
            "id": str(uuid.uuid4()),
            "repository": request.repository,
            "title": request.title,
            "body": request.body,
            "head": request.head,
            "base": request.base,
            "status": "open",
            "url": f"https://github.com/{request.repository}/pull/1",
            "provider": provider,
        }

        if token:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "UPSS-Assistant/1.0"
            }
            payload = {
                "title": request.title,
                "body": request.body,
                "head": request.head,
                "base": request.base
            }
            try:
                url = f"https://api.github.com/repos/{request.repository}/pulls"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 201:
                        res_json = resp.json()
                        provider = "GitHub REST API"
                        message = "Pull Request created successfully via GitHub API."
                        pr_data = {
                            "id": str(res_json.get("id")),
                            "repository": request.repository,
                            "title": res_json.get("title"),
                            "body": res_json.get("body"),
                            "head": request.head,
                            "base": request.base,
                            "status": res_json.get("state", "open"),
                            "url": res_json.get("html_url"),
                            "provider": provider,
                        }
                    else:
                        success = False
                        message = f"Failed to create Pull Request: GitHub API returned {resp.status_code}: {resp.text}"
            except Exception as e:
                success = False
                message = f"Failed to create Pull Request: {e}"
        else:
            message = "Pull Request created in Mock mode. (Set GITHUB_TOKEN in env for live creation)."

        response = GitHubResponse(
            success=success,
            message=message,
            provider=provider,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "pull_request": pr_data,
                **response.model_dump(),
            },
        )