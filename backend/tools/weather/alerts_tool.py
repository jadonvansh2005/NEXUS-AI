"""
UPSS Weather Alerts Tool

Returns active weather alerts.

Provider-independent implementation.

Future providers:

- OpenWeatherMap
- WeatherAPI
- Tomorrow.io
- National Weather Service
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
    WeatherAlertsRequest,
    WeatherResponse,
)


class AlertsTool(BaseTool):
    """
    Retrieve weather alerts.
    """

    metadata = ToolMetadata(

        name="weather.alerts",

        display_name="Weather Alerts",

        description="Retrieve active weather alerts.",

        category=ToolCategory.WEATHER,

        tags=[
            "weather",
            "alerts",
            "warning",
            "emergency",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = WeatherAlertsRequest

    async def execute(
        self,
        context: ToolContext,
        request: WeatherAlertsRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # alerts = provider.get_alerts(
        #     request.location
        # )
        #

        alerts = [

            {

                "id": "alert-001",

                "title": "Heavy Rain Warning",

                "severity": "Moderate",

                "description": (
                    "Heavy rainfall expected within the next "
                    "24 hours."
                ),

                "start_time": "2026-07-01T08:00:00",

                "end_time": "2026-07-01T18:00:00",

                "source": "Weather Service",

            },

            {

                "id": "alert-002",

                "title": "Strong Wind Advisory",

                "severity": "Low",

                "description": (
                    "Wind speeds may exceed 45 km/h."
                ),

                "start_time": "2026-07-01T12:00:00",

                "end_time": "2026-07-01T20:00:00",

                "source": "Weather Service",

            },

        ]

        response = WeatherResponse(

            success=True,

            message="Weather alerts retrieved successfully.",

            provider=request.provider.value,

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "location": request.location,

                "count": len(alerts),

                "alerts": alerts,

                **response.model_dump(),

            },

        )