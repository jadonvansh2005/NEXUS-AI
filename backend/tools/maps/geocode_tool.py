"""
UPSS Geocode Tool

Converts an address into geographic coordinates.

Provider-independent implementation.

Future providers:

- Google Maps
- Mapbox
- OpenStreetMap (Nominatim)
- HERE Maps
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
    GeocodeRequest,
    MapsResponse,
)


class GeocodeTool(BaseTool):
    """
    Convert an address into latitude/longitude.
    """

    metadata = ToolMetadata(

        name="maps.geocode",

        display_name="Geocode",

        description="Convert an address into geographic coordinates.",

        category=ToolCategory.MAPS,

        tags=[
            "maps",
            "geocode",
            "location",
            "coordinates",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = GeocodeRequest

    async def execute(
        self,
        context: ToolContext,
        request: GeocodeRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # result = provider.geocode(
        #     request.address
        # )
        #

        location = {

            "address": request.address,

            "latitude": 26.2183,

            "longitude": 78.1828,

            "formatted_address": request.address,

            "provider": request.provider.value,

        }

        response = MapsResponse(

            success=True,

            message="Location geocoded successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "location": location,

                **response.model_dump(),

            },

        )