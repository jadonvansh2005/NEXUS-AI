"""
UPSS Weather Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class WeatherProvider(str, Enum):

    OPENWEATHER = "openweather"

    WEATHER_API = "weatherapi"

    TOMORROW = "tomorrow"

    VISUAL_CROSSING = "visual_crossing"


# ==========================================================
# Current Weather
# ==========================================================

class CurrentWeatherRequest(BaseModel):

    location: str

    provider: WeatherProvider = (
        WeatherProvider.OPENWEATHER
    )


# ==========================================================
# Forecast
# ==========================================================

class ForecastRequest(BaseModel):

    location: str

    days: int = Field(
        default=5,
        ge=1,
        le=14,
    )

    provider: WeatherProvider = (
        WeatherProvider.OPENWEATHER
    )


# ==========================================================
# Air Quality
# ==========================================================

class AirQualityRequest(BaseModel):

    location: str

    provider: WeatherProvider = (
        WeatherProvider.OPENWEATHER
    )


# ==========================================================
# Alerts
# ==========================================================

class WeatherAlertsRequest(BaseModel):

    location: str

    provider: WeatherProvider = (
        WeatherProvider.OPENWEATHER
    )


# ==========================================================
# Response
# ==========================================================

class WeatherResponse(BaseModel):

    success: bool

    message: str

    provider: str