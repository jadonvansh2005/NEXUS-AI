"""
UPSS Travel Nearby Places Tool

Find nearby places for travelers.

Provider-independent implementation.

Future providers:

- Google Places API
- Mapbox Search
- OpenStreetMap
- HERE Places
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
    NearbyPlacesRequest,
    TravelResponse,
)


class NearbyPlacesTool(BaseTool):
    """
    Search nearby places for travelers.
    """

    metadata = ToolMetadata(

        name="travel.nearby_places",

        display_name="Nearby Places",

        description="Find nearby places for a destination.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "nearby",
            "places",
            "tourism",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = NearbyPlacesRequest

    async def execute(
        self,
        context: ToolContext,
        request: NearbyPlacesRequest,
    ) -> ToolResult:

        #
        # Future Implementation
        #
        # This tool should internally call:
        #
        # MapsNearbyPlacesTool
        #
        # or
        #
        # Google Places Provider
        #

        places = [

            {

                "name": "Central Museum",

                "type": request.place_type,

                "rating": 4.7,

                "distance_meters": 450,

                "address": "Museum Road",

            },

            {

                "name": "City Restaurant",

                "type": request.place_type,

                "rating": 4.5,

                "distance_meters": 820,

                "address": "Downtown",

            },

            {

                "name": "Shopping Plaza",

                "type": request.place_type,

                "rating": 4.3,

                "distance_meters": 1300,

                "address": "Market Street",

            },

        ]

        response = TravelResponse(

            success=True,

            message="Nearby places retrieved successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "location": request.location,

                "place_type": request.place_type,

                "radius": request.radius,

                "count": len(places),

                "places": places,

                **response.model_dump(),

            },

        )