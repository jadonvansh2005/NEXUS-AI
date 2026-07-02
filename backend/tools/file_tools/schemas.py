"""
UPSS File Tool Schemas
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class FileOperation(str, Enum):

    READ = "read"

    WRITE = "write"

    APPEND = "append"

    COPY = "copy"

    MOVE = "move"

    DELETE = "delete"

    RENAME = "rename"

    LIST = "list"

    SEARCH = "search"

    INFO = "info"

    ZIP = "zip"

    UNZIP = "unzip"


class FileRequest(BaseModel):

    path: Path = Field(
        ...,
        description="File or directory path.",
    )


class FileContentRequest(FileRequest):

    content: str


class CopyMoveRequest(FileRequest):

    destination: Path


class RenameRequest(FileRequest):

    new_name: str


class SearchRequest(FileRequest):

    pattern: str = "*"


class FileResponse(BaseModel):

    success: bool

    path: str

    message: str

    data: dict | list | str | None = None