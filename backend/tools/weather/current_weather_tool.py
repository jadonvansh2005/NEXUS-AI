"""
UPSS Current Weather Tool

Returns current weather information.

Provider-independent implementation.

Future providers:

- OpenWeatherMap
- WeatherAPI
- Tomorrow.io
- Visual Crossing
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
    CurrentWeatherRequest,
    WeatherResponse,
)


class CurrentWeatherTool(BaseTool):
    """
    Get current weather.
    """

    metadata = ToolMetadata(

        name="weather.current",

        display_name="Current Weather",

        description="Retrieve current weather conditions.",

        category=ToolCategory.WEATHER,

        tags=[
            "weather",
            "current",
            "forecast",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CurrentWeatherRequest

    async def execute(
        self,
        context: ToolContext,
        request: CurrentWeatherRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # weather = provider.current_weather(
        #     request.location
        # )
        #

        weather = {

            "location": request.location,

            "temperature": 28,

            "feels_like": 31,

            "humidity": 68,

            "pressure": 1012,

            "wind_speed": 14,

            "wind_direction": "NW",

            "visibility": 10000,

            "condition": "Partly Cloudy",

            "icon": "partly_cloudy",

            "provider": request.provider.value,

        }

        response = WeatherResponse(

            success=True,

            message="Current weather retrieved successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "weather": weather,

                **response.model_dump(),

            },

        )