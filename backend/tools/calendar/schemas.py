"""
UPSS Calendar Schemas
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Calendar Provider
# ==========================================================

class CalendarProvider(str, Enum):

    GOOGLE = "google"

    OUTLOOK = "outlook"

    APPLE = "apple"

    LOCAL = "local"


# ==========================================================
# Create Event
# ==========================================================

class CalendarEventRequest(BaseModel):
    """
    Create calendar event.
    """

    title: str

    start_time: datetime

    end_time: datetime

    description: str = ""

    location: str = ""

    attendees: list[str] = Field(
        default_factory=list,
    )

    provider: CalendarProvider = (
        CalendarProvider.GOOGLE
    )


# ==========================================================
# Update Event
# ==========================================================

class CalendarUpdateRequest(CalendarEventRequest):
    """
    Update existing event.
    """

    event_id: str


# ==========================================================
# Delete Event
# ==========================================================

class CalendarDeleteRequest(BaseModel):
    """
    Delete calendar event.
    """

    event_id: str

    provider: CalendarProvider = (
        CalendarProvider.GOOGLE
    )


# ==========================================================
# List Events
# ==========================================================

class CalendarListRequest(BaseModel):
    """
    List calendar events.
    """

    start_time: datetime | None = None

    end_time: datetime | None = None

    provider: CalendarProvider = (
        CalendarProvider.GOOGLE
    )


# ==========================================================
# Availability
# ==========================================================

class AvailabilityRequest(BaseModel):
    """
    Check calendar availability.
    """

    start_time: datetime

    end_time: datetime

    provider: CalendarProvider = (
        CalendarProvider.GOOGLE
    )


# ==========================================================
# Reminder
# ==========================================================

class CalendarReminderRequest(BaseModel):
    """
    Create calendar reminder.
    """

    event_id: str

    reminder_minutes_before: int = Field(
        default=30,
        ge=0,
    )

    provider: CalendarProvider = (
        CalendarProvider.GOOGLE
    )


# ==========================================================
# Response
# ==========================================================

class CalendarResponse(BaseModel):
    """
    Calendar response.
    """

    success: bool

    message: str

    event_id: str | None = None