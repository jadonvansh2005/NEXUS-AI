"""
UPSS Job Search Tool

Search jobs from supported providers.

Future integrations:

- LinkedIn Jobs
- Naukri
- Indeed
- Glassdoor
- Browser Tool
- Search Tool
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

from tools.career.schemas import (
    JobSearchRequest,
    CareerResponse,
)


class JobSearchTool(BaseTool):
    """
    Search jobs.
    """

    metadata = ToolMetadata(

        name="career.job_search",

        display_name="Job Search",

        description="Search jobs from supported providers.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "jobs",
            "employment",
            "search",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = JobSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: JobSearchRequest,
    ) -> ToolResult:

        #
        # Future Provider Flow
        #
        # provider = ProviderFactory.get(
        #     request.provider
        # )
        #
        # jobs = await provider.search_jobs(
        #     keywords=request.keywords,
        #     location=request.location,
        #     experience_level=request.experience_level,
        #     limit=request.limit,
        # )
        #

        result = {

            "keywords": request.keywords,

            "location": request.location,

            "experience_level": request.experience_level,

            "limit": request.limit,

            "provider": request.provider.value,

            "status": "job_search_pending",

            "message": (

                "Job search will be "

                "performed after "

                "provider integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Job search request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "job_search": result,

                **response.model_dump(),

            },

        )