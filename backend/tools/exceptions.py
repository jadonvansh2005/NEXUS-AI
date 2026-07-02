"""
UPSS Tool SDK - Exceptions

This module defines the standard exception hierarchy for all tools.

Every tool in the platform should raise only exceptions defined here.
This allows the ToolExecutor to handle failures consistently.
"""

from __future__ import annotations

from typing import Any, Optional


class ToolError(Exception):
    """
    Base exception for every Tool SDK error.
    """

    def __init__(
        self,
        message: str,
        *,
        tool_name: Optional[str] = None,
        details: Any = None,
    ):
        self.message = message
        self.tool_name = tool_name
        self.details = details

        super().__init__(message)

    def __str__(self) -> str:
        if self.tool_name:
            return f"[{self.tool_name}] {self.message}"
        return self.message


class ToolNotFoundError(ToolError):
    """
    Raised when a requested tool is not registered.
    """
    pass


class ToolAlreadyRegisteredError(ToolError):
    """
    Raised when attempting to register a tool
    with an existing name.
    """
    pass


class ToolValidationError(ToolError):
    """
    Raised when tool input validation fails.
    """
    pass


class ToolExecutionError(ToolError):
    """
    Raised when execution of a tool fails.
    """
    pass


class ToolPermissionError(ToolError):
    """
    Raised when the tool requires user approval
    before execution.
    """
    pass


class ToolTimeoutError(ToolError):
    """
    Raised when a tool exceeds its timeout.
    """
    pass


class ToolDependencyError(ToolError):
    """
    Raised when an external dependency
    is unavailable.
    """
    pass


class ToolConfigurationError(ToolError):
    """
    Raised when a tool is improperly configured.
    """
    pass


class ToolDiscoveryError(ToolError):
    """
    Raised during automatic tool discovery.
    """
    pass


class ToolRegistryError(ToolError):
    """
    Raised for registry-related failures.
    """
    pass


class ToolExecutorError(ToolError):
    """
    Raised by ToolExecutor when execution
    cannot continue.
    """
    pass


class ToolCancelledError(ToolError):
    """
    Raised when execution is cancelled
    by the user or system.
    """
    pass