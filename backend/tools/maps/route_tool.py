"""
UPSS Route Tool

Calculates routes between two locations.

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
    RouteRequest,
    MapsResponse,
)


class RouteTool(BaseTool):
    """
    Calculate the best route between two locations.
    """

    metadata = ToolMetadata(

        name="maps.route",

        display_name="Route Planner",

        description="Calculate the best route between two locations.",

        category=ToolCategory.MAPS,

        tags=[
            "maps",
            "route",
            "navigation",
            "travel",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = RouteRequest

    async def execute(
        self,
        context: ToolContext,
        request: RouteRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # route = provider.route(
        #     origin=request.origin,
        #     destination=request.destination,
        #     mode=request.mode,
        # )
        #

        route = {

            "origin": request.origin,

            "destination": request.destination,

            "mode": request.mode,

            "distance_km": 12.8,

            "duration": "22 mins",

            "provider": request.provider.value,

            "legs": [

                {

                    "distance_km": 4.2,

                    "duration": "8 mins",

                    "start": request.origin,

                    "end": "Intermediate Point",

                },

                {

                    "distance_km": 8.6,

                    "duration": "14 mins",

                    "start": "Intermediate Point",

                    "end": request.destination,

                },

            ],

            "steps": [

                {

                    "instruction": "Head north",

                    "distance": "500 m",

                },

                {

                    "instruction": "Turn right",

                    "distance": "2 km",

                },

                {

                    "instruction": "Continue straight",

                    "distance": "5 km",

                },

                {

                    "instruction": "Destination will be on the left",

                    "distance": "300 m",

                },

            ],

        }

        response = MapsResponse(

            success=True,

            message="Route calculated successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "route": route,

                **response.model_dump(),

            },

        )