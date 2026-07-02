"""
UPSS Tool SDK - Tool Result

Defines the standard output returned by every tool.

All tools must return a ToolResult object.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolResult:
    """
    Standard result returned by every tool.
    """

    # Execution status
    success: bool

    # Human-readable message
    message: str = ""

    # Main output of the tool
    data: Any = None

    # Generated artifacts
    # Example:
    #   PDF
    #   CSV
    #   Image
    #   Notebook
    #   File paths
    artifacts: list[Any] = field(default_factory=list)

    # Memory updates returned to Memory Agent
    memory_updates: dict[str, Any] = field(default_factory=dict)

    # Suggested follow-up actions
    next_actions: list[str] = field(default_factory=list)

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    # Tool execution logs
    logs: list[str] = field(default_factory=list)

    # Time taken (seconds)
    execution_time: float = 0.0

    @classmethod
    def ok(
        cls,
        *,
        message: str = "",
        data: Any = None,
        artifacts: list[Any] | None = None,
        memory_updates: dict[str, Any] | None = None,
        next_actions: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        logs: list[str] | None = None,
        execution_time: float = 0.0,
    ) -> "ToolResult":

        return cls(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            memory_updates=memory_updates or {},
            next_actions=next_actions or [],
            metadata=metadata or {},
            logs=logs or [],
            execution_time=execution_time,
        )

    @classmethod
    def failure(
        cls,
        *,
        message: str,
        logs: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ToolResult":

        return cls(
            success=False,
            message=message,
            logs=logs or [],
            metadata=metadata or {},
        )