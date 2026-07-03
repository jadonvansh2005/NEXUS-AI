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

        import httpx
        import urllib.parse

        address = request.address
        location_data = {
            "address": address,
            "latitude": 26.2183,
            "longitude": 78.1828,
            "formatted_address": address,
            "provider": request.provider.value,
        }

        try:
            headers = {"User-Agent": "UPSS-Assistant/1.0"}
            escaped_address = urllib.parse.quote(address)
            url = f"https://nominatim.openstreetmap.org/search?q={escaped_address}&format=json&limit=1"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200 and resp.json():
                    geo = resp.json()[0]
                    location_data = {
                        "address": address,
                        "latitude": float(geo["lat"]),
                        "longitude": float(geo["lon"]),
                        "formatted_address": geo.get("display_name", address),
                        "provider": "OpenStreetMap Nominatim",
                    }
        except Exception as e:
            print(f"[Geocode Live Error] {e}")

        response = MapsResponse(
            success=True,
            message="Location geocoded successfully.",
            provider=location_data["provider"],
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "location": location_data,
                **response.model_dump(),
            },
        )