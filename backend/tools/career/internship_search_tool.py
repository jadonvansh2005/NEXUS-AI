"""
UPSS Internship Search Tool

Search internships from supported providers.

Future integrations:

- Internshala
- LinkedIn
- Indeed
- Wellfound
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
    InternshipSearchRequest,
    CareerResponse,
)


class InternshipSearchTool(BaseTool):
    """
    Search internships.
    """

    metadata = ToolMetadata(

        name="career.internship_search",

        display_name="Internship Search",

        description="Search internships from supported providers.",

        category=ToolCategory.CAREER,

        tags=[
            "career",
            "internship",
            "jobs",
            "students",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = InternshipSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: InternshipSearchRequest,
    ) -> ToolResult:

        #
        # Future Provider Flow
        #
        # provider = ProviderFactory.get(
        #     request.provider
        # )
        #
        # internships = await provider.search_internships(
        #     keywords=request.keywords,
        #     location=request.location,
        #     stipend_required=request.stipend_required,
        #     limit=request.limit,
        # )
        #

        result = {

            "keywords": request.keywords,

            "location": request.location,

            "stipend_required": request.stipend_required,

            "limit": request.limit,

            "provider": request.provider.value,

            "status": "internship_search_pending",

            "message": (

                "Internship search will be "

                "performed after "

                "provider integration."

            ),

        }

        response = CareerResponse(

            success=True,

            message="Internship search request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "internship_search": result,

                **response.model_dump(),

            },

        )