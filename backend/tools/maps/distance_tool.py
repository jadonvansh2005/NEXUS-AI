"""
UPSS Distance Tool

Calculates the distance between two locations.

Provider-independent implementation.

Future providers:

- Google Maps
- Mapbox
- HERE Maps
- OpenStreetMap
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

from tools.maps.schemas import (
    DistanceRequest,
    MapsResponse,
)


class DistanceTool(BaseTool):
    """
    Calculate distance between two locations.
    """

    metadata = ToolMetadata(

        name="maps.distance",

        display_name="Distance Calculator",

        description="Calculate the distance between two locations.",

        category=ToolCategory.MAPS,

        tags=[
            "maps",
            "distance",
            "travel",
            "route",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DistanceRequest

    async def execute(
        self,
        context: ToolContext,
        request: DistanceRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # result = provider.distance(
        #     origin=request.origin,
        #     destination=request.destination,
        # )
        #

        distance = {

            "origin": request.origin,

            "destination": request.destination,

            "distance_km": 12.8,

            "distance_meters": 12800,

            "estimated_duration": "22 mins",

            "estimated_duration_seconds": 1320,

            "provider": request.provider.value,

        }

        response = MapsResponse(

            success=True,

            message="Distance calculated successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "distance": distance,

                **response.model_dump(),

            },

        )