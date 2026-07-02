"""
Approval Rules

Responsibilities

- Determine whether approval is required
- Estimate risk
- Select approval type

Future

- LLM-based Risk Analysis
- Organization Policies
- User Preferences
- Dynamic Approval Rules
"""

from __future__ import annotations

from agents.human_in_the_loop.approval_models import (
    ApprovalAction,
    ApprovalType,
    RiskLevel,
)


class ApprovalRules:

    """
    Rule engine for Human-in-the-Loop.
    """

    # =====================================================
    # Approval Required
    # =====================================================

    def requires_approval(

        self,

        action: ApprovalAction,

        risk_level: RiskLevel,

    ) -> bool:

        #
        # Critical risk always requires approval
        #

        if risk_level == RiskLevel.CRITICAL:

            return True

        #
        # High-risk actions
        #

        if action in [

            ApprovalAction.PAYMENT,

            ApprovalAction.PURCHASE,

            ApprovalAction.BOOK,

            ApprovalAction.CANCEL,

            ApprovalAction.DELETE,

            ApprovalAction.SEND,

        ]:

            return True

        #
        # High risk
        #

        if risk_level == RiskLevel.HIGH:

            return True

        return False

    # =====================================================
    # Approval Type
    # =====================================================

    def approval_type(

        self,

        action: ApprovalAction,

    ) -> ApprovalType:

        #
        # Future:
        # Organization-specific rules
        #

        return ApprovalType.USER

    # =====================================================
    # Estimate Risk
    # =====================================================

    def estimate_risk(

        self,

        action: ApprovalAction,

    ) -> RiskLevel:

        if action in [

            ApprovalAction.PAYMENT,

            ApprovalAction.PURCHASE,

        ]:

            return RiskLevel.CRITICAL

        if action in [

            ApprovalAction.BOOK,

            ApprovalAction.CANCEL,

            ApprovalAction.DELETE,

            ApprovalAction.SEND,

        ]:

            return RiskLevel.HIGH

        if action in [

            ApprovalAction.UPDATE,

            ApprovalAction.EXPORT,

        ]:

            return RiskLevel.MEDIUM

        return RiskLevel.LOW