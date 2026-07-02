"""
UPSS Air Quality Tool

Returns air quality information.

Provider-independent implementation.

Future providers:

- OpenWeatherMap
- WeatherAPI
- Tomorrow.io
- IQAir
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

from tools.weather.schemas import (
    AirQualityRequest,
    WeatherResponse,
)


class AirQualityTool(BaseTool):
    """
    Retrieve air quality information.
    """

    metadata = ToolMetadata(

        name="weather.air_quality",

        display_name="Air Quality",

        description="Retrieve air quality information.",

        category=ToolCategory.WEATHER,

        tags=[
            "weather",
            "aqi",
            "air",
            "pollution",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = AirQualityRequest

    async def execute(
        self,
        context: ToolContext,
        request: AirQualityRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # air_quality = provider.air_quality(
        #     request.location
        # )
        #

        air_quality = {

            "location": request.location,

            "aqi": 72,

            "category": "Moderate",

            "pm2_5": 18.4,

            "pm10": 32.8,

            "co": 0.7,

            "no2": 21.3,

            "so2": 5.8,

            "o3": 31.4,

            "provider": request.provider.value,

        }

        response = WeatherResponse(

            success=True,

            message="Air quality retrieved successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "air_quality": air_quality,

                **response.model_dump(),

            },

        )