"""
UPSS Email Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class EmailPriority(str, Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"


class EmailRequest(BaseModel):
    """
    Base email request.
    """

    to: list[EmailStr]

    cc: list[EmailStr] = Field(
        default_factory=list,
    )

    bcc: list[EmailStr] = Field(
        default_factory=list,
    )

    subject: str

    body: str

    html: bool = False

    priority: EmailPriority = (
        EmailPriority.NORMAL
    )


class DraftEmailRequest(EmailRequest):
    pass


class SendEmailRequest(EmailRequest):

    attachments: list[str] = Field(
        default_factory=list,
    )


class ReadEmailRequest(BaseModel):

    email_id: str


class SearchEmailRequest(BaseModel):

    query: str

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )


class AttachmentRequest(BaseModel):

    email_id: str

    download_directory: str = "downloads"


class EmailResponse(BaseModel):

    success: bool

    message: str

    email_id: str | None = None