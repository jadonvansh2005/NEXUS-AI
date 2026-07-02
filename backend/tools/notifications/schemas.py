"""
UPSS Notification Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class NotificationPriority(str, Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    URGENT = "urgent"


class NotificationRequest(BaseModel):
    """
    Base notification request.
    """

    title: str = Field(
        ...,
        description="Notification title.",
    )

    message: str = Field(
        ...,
        description="Notification body.",
    )

    priority: NotificationPriority = (
        NotificationPriority.NORMAL
    )


class DesktopNotificationRequest(
    NotificationRequest
):
    pass


class PushNotificationRequest(
    NotificationRequest
):

    device_token: str | None = None


class SMSNotificationRequest(
    NotificationRequest
):

    phone_number: str


class ReminderRequest(NotificationRequest):

    reminder_time: str


class NotificationResponse(BaseModel):

    success: bool

    message: str

    notification_id: str | None = None