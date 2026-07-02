"""
Approval State

Responsibilities

- Runtime approval state
- Approval decision
- User action
- Approval metadata

Future

- Multi-Level Approval
- Approval Chain
- Approval History
"""

from __future__ import annotations

from typing import Any
from typing import Dict

from pydantic import BaseModel
from pydantic import Field

from agents.human_in_the_loop.approval_models import (
    ApprovalAction,
    ApprovalStatus,
    ApprovalType,
    RiskLevel,
)


class ApprovalState(BaseModel):
    """
    Runtime state for Human-in-the-Loop approval.
    """

    # =====================================================
    # User
    # =====================================================

    user_id: int

    task_id: str

    query: str

    # =====================================================
    # Approval Information
    # =====================================================

    action: ApprovalAction

    risk_level: RiskLevel

    approval_type: ApprovalType = (
        ApprovalType.USER
    )

    status: ApprovalStatus = (
        ApprovalStatus.PENDING
    )

    # =====================================================
    # Decision
    # =====================================================

    approved: bool = False

    rejected: bool = False

    reason: str = ""

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = Field(

        default_factory=dict

    )

    # =====================================================
    # Helpers
    # =====================================================

    def approve(self) -> None:

        self.approved = True

        self.rejected = False

        self.status = ApprovalStatus.APPROVED

    def reject(

        self,

        reason: str = "",

    ) -> None:

        self.approved = False

        self.rejected = True

        self.reason = reason

        self.status = ApprovalStatus.REJECTED

    def expire(self) -> None:

        self.status = ApprovalStatus.EXPIRED