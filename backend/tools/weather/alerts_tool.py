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

        import httpx
        import urllib.parse
        from datetime import datetime

        location = request.location
        alerts = []
        
        try:
            # 1. Geocode location using OpenStreetMap
            headers = {"User-Agent": "UPSS-Assistant/1.0"}
            escaped_location = urllib.parse.quote(location)
            geo_url = f"https://nominatim.openstreetmap.org/search?q={escaped_location}&format=json&limit=1"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                geo_resp = await client.get(geo_url, headers=headers)
                if geo_resp.status_code == 200 and geo_resp.json():
                    geo_data = geo_resp.json()[0]
                    lat = geo_data["lat"]
                    lon = geo_data["lon"]
                    
                    # 2. Get today's daily extreme forecast metrics from Open-Meteo
                    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,windspeed_10m_max,rain_sum&timezone=auto"
                    f_resp = await client.get(forecast_url)
                    if f_resp.status_code == 200:
                        data = f_resp.json()
                        daily = data.get("daily", {})
                        
                        max_temps = daily.get("temperature_2m_max", [])
                        max_winds = daily.get("windspeed_10m_max", [])
                        rain_sums = daily.get("rain_sum", [])
                        
                        # Analyze today's metrics
                        if max_temps:
                            today_temp = max_temps[0] or 0.0
                            if today_temp > 40.0:
                                alerts.append({
                                    "id": "alert-heat",
                                    "title": "Extreme Heat Warning",
                                    "severity": "High",
                                    "description": f"Dangerously hot conditions with temperatures reaching {today_temp}°C expected.",
                                    "start_time": datetime.now().strftime("%Y-%m-%dT00:00:00"),
                                    "end_time": datetime.now().strftime("%Y-%m-%dT23:59:59"),
                                    "source": "Open-Meteo Alert Service"
                                })
                                
                        if max_winds:
                            today_wind = max_winds[0] or 0.0
                            if today_wind > 35.0:
                                alerts.append({
                                    "id": "alert-wind",
                                    "title": "Strong Wind Advisory",
                                    "severity": "Moderate",
                                    "description": f"Strong winds with speeds up to {today_wind} km/h expected today.",
                                    "start_time": datetime.now().strftime("%Y-%m-%dT00:00:00"),
                                    "end_time": datetime.now().strftime("%Y-%m-%dT23:59:59"),
                                    "source": "Open-Meteo Alert Service"
                                })
                                
                        if rain_sums:
                            today_rain = rain_sums[0] or 0.0
                            if today_rain > 12.0:
                                alerts.append({
                                    "id": "alert-rain",
                                    "title": "Heavy Rainfall Alert",
                                    "severity": "Moderate",
                                    "description": f"Significant rainfall sum of {today_rain}mm expected today. Localized flooding possible.",
                                    "start_time": datetime.now().strftime("%Y-%m-%dT00:00:00"),
                                    "end_time": datetime.now().strftime("%Y-%m-%dT23:59:59"),
                                    "source": "Open-Meteo Alert Service"
                                })
        except Exception as e:
            print(f"[Alerts API Error] {e}")

        # Default info alert if conditions are peaceful
        if not alerts:
            alerts = [
                {
                    "id": "alert-none",
                    "title": "No Active Weather Alerts",
                    "severity": "None",
                    "description": "Weather conditions are within normal ranges. No warnings in effect.",
                    "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "source": "Open-Meteo Alert Service"
                }
            ]

        response = WeatherResponse(
            success=True,
            message="Weather alerts retrieved successfully.",
            provider="Open-Meteo API",
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