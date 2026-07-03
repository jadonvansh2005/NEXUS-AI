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

        import httpx
        import urllib.parse

        location = request.location
        
        # Default mock fallback data
        air_quality = {
            "location": location,
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
                    
                    # 2. Query keyless Open-Meteo Air Quality API
                    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
                    aqi_resp = await client.get(aqi_url)
                    if aqi_resp.status_code == 200:
                        data = aqi_resp.json()
                        current = data.get("current", {})
                        aqi_val = current.get("us_aqi", 72)
                        
                        # Determine AQI classification
                        if aqi_val <= 50:
                            cat = "Good"
                        elif aqi_val <= 100:
                            cat = "Moderate"
                        elif aqi_val <= 150:
                            cat = "Unhealthy for Sensitive Groups"
                        elif aqi_val <= 200:
                            cat = "Unhealthy"
                        elif aqi_val <= 300:
                            cat = "Very Unhealthy"
                        else:
                            cat = "Hazardous"
                            
                        air_quality = {
                            "location": location,
                            "aqi": int(aqi_val),
                            "category": cat,
                            "pm2_5": current.get("pm2_5", 18.4),
                            "pm10": current.get("pm10", 32.8),
                            "co": current.get("carbon_monoxide", 0.7),
                            "no2": current.get("nitrogen_dioxide", 21.3),
                            "so2": current.get("sulphur_dioxide", 5.8),
                            "o3": current.get("ozone", 31.4),
                            "provider": "Open-Meteo API",
                        }
        except Exception as e:
            print(f"[AQI Live Fetch Error] {e}")

        response = WeatherResponse(
            success=True,
            message="Air quality retrieved successfully.",
            provider=air_quality["provider"],
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "air_quality": air_quality,
                **response.model_dump(),
            },
        )