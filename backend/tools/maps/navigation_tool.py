"""
UPSS Navigation Tool

Provides navigation guidance.

Provider-independent implementation.

Future providers:

- Google Maps Navigation
- Mapbox Navigation
- HERE Navigation
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
    NavigationRequest,
    MapsResponse,
)


class NavigationTool(BaseTool):
    """
    Provide navigation guidance between two locations.
    """

    metadata = ToolMetadata(

        name="maps.navigation",

        display_name="Navigation",

        description="Provide navigation guidance between two locations.",

        category=ToolCategory.MAPS,

        tags=[
            "maps",
            "navigation",
            "route",
            "directions",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = NavigationRequest

    async def execute(
        self,
        context: ToolContext,
        request: NavigationRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # navigation = provider.navigation(
        #     origin=request.origin,
        #     destination=request.destination,
        #     mode=request.mode,
        # )
        #

        navigation = {

            "origin": request.origin,

            "destination": request.destination,

            "mode": request.mode,

            "provider": request.provider.value,

            "summary": {

                "distance_km": 12.8,

                "estimated_duration": "22 mins",

                "traffic": "Moderate",

            },

            "steps": [

                {

                    "step": 1,

                    "instruction": "Head north on Main Road",

                    "distance": "500 m",

                },

                {

                    "step": 2,

                    "instruction": "Turn right onto Highway 12",

                    "distance": "3.2 km",

                },

                {

                    "step": 3,

                    "instruction": "Continue straight",

                    "distance": "7.8 km",

                },

                {

                    "step": 4,

                    "instruction": "Turn left toward destination",

                    "distance": "1.0 km",

                },

                {

                    "step": 5,

                    "instruction": "You have arrived at your destination",

                    "distance": "0 m",

                },

            ],

        }

        response = MapsResponse(

            success=True,

            message="Navigation generated successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "navigation": navigation,

                **response.model_dump(),

            },

        )