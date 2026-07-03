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

        category=ToolCategory.GITHUB,

        tags=[
            "github",
            "issue",
            "bug",
            "feature",
        ],

    )

    permission = ToolPermission.write()

    input_model = IssueRequest

    async def execute(
        self,
        context: ToolContext,
        request: IssueRequest,
    ) -> ToolResult:

        import httpx
        import os
        import uuid

        token = os.getenv("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
        success = True
        provider = "Mock"
        message = "GitHub issue created successfully (mock mode)."
        
        issue_data = {
            "id": str(uuid.uuid4()),
            "repository": request.repository,
            "title": request.title,
            "body": request.body,
            "labels": request.labels,
            "status": "open",
            "url": f"https://github.com/{request.repository}/issues/1",
            "provider": provider,
            "created_by": getattr(context, "user_id", None),
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
                "labels": request.labels
            }
            try:
                url = f"https://api.github.com/repos/{request.repository}/issues"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 201:
                        res_json = resp.json()
                        provider = "GitHub REST API"
                        message = "GitHub issue created successfully via GitHub API."
                        issue_data = {
                            "id": str(res_json.get("id")),
                            "repository": request.repository,
                            "title": res_json.get("title"),
                            "body": res_json.get("body"),
                            "labels": [label.get("name") if isinstance(label, dict) else str(label) for label in res_json.get("labels", [])],
                            "status": res_json.get("state", "open"),
                            "url": res_json.get("html_url"),
                            "provider": provider,
                            "created_by": getattr(context, "user_id", None),
                        }
                    else:
                        success = False
                        message = f"Failed to create issue: GitHub API returned {resp.status_code}: {resp.text}"
            except Exception as e:
                success = False
                message = f"Failed to create issue: {e}"
        else:
            message = "GitHub issue created in Mock mode. (Set GITHUB_TOKEN in env for live creation)."

        response = GitHubResponse(
            success=success,
            message=message,
            provider=provider,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "issue": issue_data,
                **response.model_dump(),
            },
        )