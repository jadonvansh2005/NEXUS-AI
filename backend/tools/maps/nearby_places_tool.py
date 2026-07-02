"""
UPSS Nearby Places Tool

Find nearby places.

Provider-independent implementation.

Future providers:

- Google Places API
- Mapbox Search
- HERE Places
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
    NearbyPlacesRequest,
    MapsResponse,
)


class NearbyPlacesTool(BaseTool):
    """
    Find nearby places.
    """

    metadata = ToolMetadata(

        name="maps.nearby_places",

        display_name="Nearby Places",

        description="Find nearby places of a given type.",

        category=ToolCategory.MAPS,

        tags=[
            "maps",
            "places",
            "nearby",
            "search",
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
        # Future Provider Integration
        #
        # places = provider.nearby_places(
        #     location=request.location,
        #     place_type=request.place_type,
        #     radius=request.radius,
        # )
        #

        places = [

            {

                "id": "place_001",

                "name": "Sample Place One",

                "type": request.place_type,

                "address": "123 Main Street",

                "rating": 4.6,

                "distance_meters": 320,

                "latitude": 26.2183,

                "longitude": 78.1828,

            },

            {

                "id": "place_002",

                "name": "Sample Place Two",

                "type": request.place_type,

                "address": "456 City Road",

                "rating": 4.3,

                "distance_meters": 840,

                "latitude": 26.2201,

                "longitude": 78.1802,

            },

            {

                "id": "place_003",

                "name": "Sample Place Three",

                "type": request.place_type,

                "address": "789 Market Avenue",

                "rating": 4.1,

                "distance_meters": 1350,

                "latitude": 26.2214,

                "longitude": 78.1837,

            },

        ]

        response = MapsResponse(

            success=True,

            message="Nearby places retrieved successfully.",

            provider=request.provider.value,

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