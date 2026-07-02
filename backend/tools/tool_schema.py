"""
UPSS Tool SDK - Tool Schemas

Defines common schemas shared by every tool.

Every tool should declare:
    • Metadata
    • Input Schema
    • Output Schema
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ==========================================================
# Tool Category
# ==========================================================

class ToolCategory(str, Enum):
    """
    High-level grouping of tools.
    """

    BROWSER = "browser"
    SEARCH = "search"
    TRAVEL = "travel"
    CALENDAR = "calendar"
    COMMUNICATION = "communication"
    FILESYSTEM = "filesystem"
    TERMINAL = "terminal"
    PYTHON = "python"
    SQL = "sql"
    GITHUB = "github"
    DOCKER = "docker"
    EMAIL = "email"
    PRODUCTIVITY = "productivity"
    NOTIFICATION = "notification"
    WEATHER = "weather"
    MAPS = "maps"
    REPORT = "report"
    VISUALIZATION = "visualization"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    EXECUTION = "execution"
    SYSTEM = "system"
    OTHER = "other"


# ==========================================================
# Tool Metadata
# ==========================================================

class ToolMetadata(BaseModel):
    """
    Static information describing a tool.
    """

    name: str

    display_name: str

    description: str

    category: ToolCategory

    version: str = "1.0.0"

    author: str = "UPSS"

    tags: list[str] = Field(default_factory=list)

    enabled: bool = True

    timeout: int = 300


# ==========================================================
# Base Input Schema
# ==========================================================

class ToolInput(BaseModel):
    """
    Base input for every tool.
    """

    parameters: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Base Output Schema
# ==========================================================

class ToolOutput(BaseModel):
    """
    Base output schema.
    """

    success: bool

    message: str

    result: Any | None = None