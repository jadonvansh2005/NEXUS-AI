"""
Approval Models

Responsibilities

- Approval status
- Approval type
- Risk levels
- Approval request models

Used by

- HITL Agent
- Approval Manager
- Execution Controller
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Approval Status
# ==========================================================

class ApprovalStatus(str, Enum):

    PENDING = "pending"

    APPROVED = "approved"

    REJECTED = "rejected"

    EXPIRED = "expired"


# ==========================================================
# Approval Type
# ==========================================================

class ApprovalType(str, Enum):

    NONE = "none"

    USER = "user"

    ADMIN = "admin"

    SYSTEM = "system"


# ==========================================================
# Risk Level
# ==========================================================

class RiskLevel(str, Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Approval Action
# ==========================================================

class ApprovalAction(str, Enum):

    EXECUTE = "execute"

    DELETE = "delete"

    UPDATE = "update"

    SEND = "send"

    PURCHASE = "purchase"

    PAYMENT = "payment"

    BOOK = "book"

    CANCEL = "cancel"

    LOGIN = "login"

    EXPORT = "export"


# ==========================================================
# Approval Request
# ==========================================================

class ApprovalRequest(BaseModel):

    user_id: int

    task_id: str

    action: ApprovalAction

    risk_level: RiskLevel

    approval_type: ApprovalType = ApprovalType.USER

    status: ApprovalStatus = ApprovalStatus.PENDING

    reason: str = ""

    expires_in_minutes: int = 10