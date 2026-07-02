"""
UPSS GitHub Repository Search Tool

Search GitHub repositories.

Provider-independent implementation.

Future providers:

- GitHub REST API
- GitHub GraphQL API
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
    RepositorySearchRequest,
    GitHubResponse,
)


class RepositorySearchTool(BaseTool):
    """
    Search GitHub repositories.
    """

    metadata = ToolMetadata(

        name="github.search",

        display_name="GitHub Repository Search",

        description="Search repositories on GitHub.",

        category=ToolCategory.DEVELOPER,

        tags=[
            "github",
            "repository",
            "search",
            "git",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = RepositorySearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: RepositorySearchRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # repositories = provider.search_repositories(
        #     query=request.query,
        #     limit=request.limit,
        # )
        #

        repositories = [

            {

                "name": "awesome-ai",

                "owner": "open-source",

                "description": "Collection of AI resources.",

                "language": "Python",

                "stars": 18420,

                "forks": 3210,

                "license": "MIT",

                "url": "https://github.com/open-source/awesome-ai",

            },

            {

                "name": "agent-framework",

                "owner": "community",

                "description": "Framework for AI agents.",

                "language": "Python",

                "stars": 9450,

                "forks": 1288,

                "license": "Apache-2.0",

                "url": "https://github.com/community/agent-framework",

            },

        ][: request.limit]

        response = GitHubResponse(

            success=True,

            message="Repository search completed successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "query": request.query,

                "count": len(repositories),

                "repositories": repositories,

                **response.model_dump(),

            },

        )