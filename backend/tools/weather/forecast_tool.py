"""
UPSS Weather Forecast Tool

Returns weather forecast.

Provider-independent implementation.

Future providers:

- OpenWeatherMap
- WeatherAPI
- Tomorrow.io
- Visual Crossing
"""

from __future__ import annotations

from datetime import timedelta

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.weather.schemas import (
    ForecastRequest,
    WeatherResponse,
)


class ForecastTool(BaseTool):
    """
    Retrieve weather forecast.
    """

    metadata = ToolMetadata(

        name="weather.forecast",

        display_name="Weather Forecast",

        description="Retrieve weather forecast.",

        category=ToolCategory.WEATHER,

        tags=[
            "weather",
            "forecast",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ForecastRequest

    async def execute(
        self,
        context: ToolContext,
        request: ForecastRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # forecast = provider.forecast(
        #     request.location,
        #     request.days,
        # )
        #

        forecast = []

        for day in range(request.days):

            forecast.append(

                {

                    "day": day + 1,

                    "date_offset": str(
                        timedelta(days=day)
                    ),

                    "condition": "Sunny",

                    "temperature_min": 24,

                    "temperature_max": 33,

                    "humidity": 62,

                    "wind_speed": 11,

                    "precipitation_probability": 15,

                }

            )

        response = WeatherResponse(

            success=True,

            message="Weather forecast retrieved successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "location": request.location,

                "forecast": forecast,

                **response.model_dump(),

            },

        )