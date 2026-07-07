"""
UPSS Tool SDK - Permission Models

Defines permission levels and approval policies
used by ToolExecutor before executing tools.
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PermissionLevel(str, Enum):
    """
    Permission required by a tool.
    """

    NONE = "none"

    READ = "read"

    WRITE = "write"

    TRANSACTION = "transaction"

    ADMIN = "admin"


class ApprovalStatus(str, Enum):
    """
    Current approval state.
    """

    PENDING = "pending"

    APPROVED = "approved"

    REJECTED = "rejected"

    NOT_REQUIRED = "not_required"


@dataclass(slots=True)
class ToolPermission:

    """
    Permission metadata attached to every tool.
    """

    level: PermissionLevel = PermissionLevel.NONE

    requires_approval: bool = False

    approval_message: Optional[str] = None

    allow_retry: bool = True

    timeout_seconds: int = 300

    def needs_approval(self) -> bool:
        """
        Returns True if the tool requires
        explicit user approval.
        """
        return self.requires_approval

    @classmethod
    def read_only(cls) -> "ToolPermission":
        return cls(
            level=PermissionLevel.READ,
            requires_approval=False
        )

    @classmethod
    def requires_confirmation(cls) -> "ToolPermission":
        return cls(
            level=PermissionLevel.WRITE,
            requires_approval=True
        )

    @classmethod
    def write(cls) -> "ToolPermission":
        return cls(
            level=PermissionLevel.WRITE,
            requires_approval=True
        )

    @classmethod
    def transaction(cls) -> "ToolPermission":
        return cls(
            level=PermissionLevel.TRANSACTION,
            requires_approval=True
        )

    @classmethod
    def admin(cls) -> "ToolPermission":
        return cls(
            level=PermissionLevel.ADMIN,
            requires_approval=True
        )