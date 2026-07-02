"""
UPSS Terminal Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ShellType(str, Enum):

    CMD = "cmd"

    POWERSHELL = "powershell"

    BASH = "bash"


class TerminalRequest(BaseModel):

    command: str = Field(
        ...,
        description="Command to execute.",
    )

    working_directory: str | None = None

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
    )

    shell: ShellType = ShellType.POWERSHELL


class TerminalResponse(BaseModel):

    success: bool

    command: str

    exit_code: int

    stdout: str

    stderr: str