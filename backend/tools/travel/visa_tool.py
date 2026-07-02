"""
UPSS Visa Information Tool

Retrieve visa requirements for international travel.

Current:
    Returns a normalized visa request.

Future providers:

- Government Visa Portals
- IATA Timatic
- Sherpa
- Browser Tool
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

from tools.travel.schemas import (
    VisaRequest,
    TravelResponse,
)


class VisaTool(BaseTool):
    """
    Retrieve visa information.
    """

    metadata = ToolMetadata(

        name="travel.visa",

        display_name="Visa Information",

        description="Retrieve visa requirements for a destination.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "visa",
            "passport",
            "international",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = VisaRequest

    async def execute(
        self,
        context: ToolContext,
        request: VisaRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider = ProviderFactory.get(...)
        #
        # visa = await provider.get_visa_requirements(
        #     nationality=request.nationality,
        #     destination=request.destination,
        # )
        #

        #
        # Temporary normalized response.
        # Replace with provider output.
        #

        visa = {

            "nationality": request.nationality,

            "destination": request.destination,

            "status": "information_pending",

            "provider": "future_provider",

        }

        response = TravelResponse(

            success=True,

            message="Visa information retrieved successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "visa": visa,

                **response.model_dump(),

            },

        )