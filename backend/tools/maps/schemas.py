"""
UPSS Maps Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class MapsProvider(str, Enum):

    GOOGLE = "google"

    MAPBOX = "mapbox"

    OPENSTREETMAP = "openstreetmap"

    HERE = "here"


# ==========================================================
# Geocode
# ==========================================================

class GeocodeRequest(BaseModel):

    address: str

    provider: MapsProvider = MapsProvider.GOOGLE


# ==========================================================
# Distance
# ==========================================================

class DistanceRequest(BaseModel):

    origin: str

    destination: str

    provider: MapsProvider = MapsProvider.GOOGLE


# ==========================================================
# Route
# ==========================================================

class RouteRequest(BaseModel):

    origin: str

    destination: str

    mode: str = Field(
        default="driving",
    )

    provider: MapsProvider = MapsProvider.GOOGLE


# ==========================================================
# Nearby Places
# ==========================================================

class NearbyPlacesRequest(BaseModel):

    location: str

    place_type: str

    radius: int = Field(
        default=5000,
        ge=100,
        le=50000,
    )

    provider: MapsProvider = MapsProvider.GOOGLE


# ==========================================================
# Navigation
# ==========================================================

class NavigationRequest(BaseModel):

    origin: str

    destination: str

    mode: str = Field(
        default="driving",
    )

    provider: MapsProvider = MapsProvider.GOOGLE


# ==========================================================
# Response
# ==========================================================

class MapsResponse(BaseModel):

    success: bool

    message: str

    provider: str