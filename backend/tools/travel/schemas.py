"""
UPSS Travel Schemas
"""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class TravelProvider(str, Enum):

    GENERIC = "generic"

    GOOGLE = "google"

    SKYSCANNER = "skyscanner"

    BOOKING = "booking"

    IRCTC = "irctc"


# ==========================================================
# Itinerary
# ==========================================================

class ItineraryRequest(BaseModel):

    destination: str

    start_date: date

    end_date: date

    travelers: int = Field(
        default=1,
        ge=1,
    )

    budget: float | None = None


# ==========================================================
# Flight Search
# ==========================================================

class FlightSearchRequest(BaseModel):

    origin: str

    destination: str

    departure_date: date

    return_date: date | None = None

    passengers: int = Field(
        default=1,
        ge=1,
    )

    provider: TravelProvider = (
        TravelProvider.GENERIC
    )


# ==========================================================
# Fare Estimator
# ==========================================================

class FareEstimatorRequest(BaseModel):

    origin: str

    destination: str

    departure_date: date


# ==========================================================
# Price Compare
# ==========================================================

class PriceCompareRequest(BaseModel):

    origin: str

    destination: str

    departure_date: date

    return_date: date | None = None

    passengers: int = Field(
        default=1,
        ge=1,
    )

    providers: list[TravelProvider] = Field(
        default_factory=lambda: [
            TravelProvider.GOOGLE,
            TravelProvider.SKYSCANNER,
            TravelProvider.GENERIC,
        ]
    )


# ==========================================================
# Hotel Search
# ==========================================================

class HotelSearchRequest(BaseModel):

    destination: str

    check_in: date

    check_out: date

    guests: int = Field(
        default=1,
        ge=1,
    )

    provider: TravelProvider = (
        TravelProvider.GENERIC
    )


# ==========================================================
# Train Search
# ==========================================================

class TrainSearchRequest(BaseModel):

    origin: str

    destination: str

    journey_date: date

    provider: TravelProvider = (
        TravelProvider.IRCTC
    )


# ==========================================================
# Budget
# ==========================================================

class BudgetRequest(BaseModel):

    destination: str

    days: int = Field(
        ge=1,
    )

    travelers: int = Field(
        default=1,
        ge=1,
    )

    total_budget: float


# ==========================================================
# Nearby Places
# ==========================================================

class NearbyPlacesRequest(BaseModel):

    location: str

    place_type: str

    radius: int = Field(
        default=5000,
        ge=100,
    )


# ==========================================================
# Trip Summary
# ==========================================================

class TripSummaryRequest(BaseModel):

    itinerary: dict

    flights: list[dict] = Field(
        default_factory=list,
    )

    hotels: list[dict] = Field(
        default_factory=list,
    )

    budget: dict | None = None


# ==========================================================
# Booking
# ==========================================================

class BookingRequest(BaseModel):

    booking_type: str

    provider: TravelProvider

    details: dict


# ==========================================================
# Visa
# ==========================================================

class VisaRequest(BaseModel):

    nationality: str

    destination: str


# ==========================================================
# Currency Converter
# ==========================================================

class CurrencyConverterRequest(BaseModel):

    amount: float

    from_currency: str

    to_currency: str


# ==========================================================
# Packing List
# ==========================================================

class PackingListRequest(BaseModel):

    destination: str

    days: int

    weather: str

    activities: list[str] = Field(
        default_factory=list,
    )


# ==========================================================
# Response
# ==========================================================

class TravelResponse(BaseModel):

    success: bool

    message: str



# ==========================================================
# Flight Cancellation
# ==========================================================

class FlightCancellationRequest(BaseModel):

    booking_reference: str

    provider: TravelProvider = (
        TravelProvider.GENERIC
    )

    reason: str | None = None


# ==========================================================
# Hotel Cancellation
# ==========================================================

class HotelCancellationRequest(BaseModel):

    booking_reference: str

    provider: TravelProvider = (
        TravelProvider.BOOKING
    )

    reason: str | None = None


# ==========================================================
# Train Cancellation
# ==========================================================

class TrainCancellationRequest(BaseModel):

    booking_reference: str

    provider: TravelProvider = (
        TravelProvider.IRCTC
    )

    reason: str | None = None


# ==========================================================
# Price Compare
# ==========================================================

class PriceCompareRequest(BaseModel):

    origin: str

    destination: str

    departure_date: date

    return_date: date | None = None

    passengers: int = Field(
        default=1,
        ge=1,
    )

    providers: list[TravelProvider] = Field(
        default_factory=lambda: [
            TravelProvider.GOOGLE,
            TravelProvider.SKYSCANNER,
            TravelProvider.GENERIC,
        ]
    )