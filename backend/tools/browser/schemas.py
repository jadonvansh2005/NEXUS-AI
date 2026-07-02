"""
UPSS Browser Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class BrowserAction(str, Enum):

    READ = "read"

    SEARCH = "search"

    SCREENSHOT = "screenshot"

    DOWNLOAD = "download"


class BrowserRequest(BaseModel):

    url: str = Field(
        ...,
        description="Target webpage URL.",
    )

    timeout: int = Field(
        default=30,
        ge=5,
        le=120,
    )

    wait_until: str = Field(
        default="networkidle",
    )


class BrowserPage(BaseModel):

    url: str

    title: str

    html: str

    text: str

    markdown: str = ""


class BrowserResponse(BaseModel):

    success: bool

    page: BrowserPage | None = None

    message: str = ""