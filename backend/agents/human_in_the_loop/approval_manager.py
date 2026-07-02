"""
Approval Manager

Responsibilities

- Coordinate approval workflow
- Apply approval rules
- Validate approval request
- Return approval decision

Future

- Multi-Level Approval
- Approval Persistence
- Notification System
- Approval Timeout Handling
"""

from __future__ import annotations

from agents.human_in_the_loop.approval_logger import (
    ApprovalLogger,
)

from agents.human_in_the_loop.approval_rules import (
    ApprovalRules,
)

from agents.human_in_the_loop.approval_state import (
    ApprovalState,
)

from agents.human_in_the_loop.approval_validator import (
    ApprovalValidator,
)


class ApprovalManager:

    """
    Coordinates the complete approval pipeline.
    """

    def __init__(self):

        self.rules = (
            ApprovalRules()
        )

        self.validator = (
            ApprovalValidator()
        )

        self.logger = (
            ApprovalLogger()
        )

    # =====================================================
    # Process Approval
    # =====================================================

    def process(

        self,

        state: ApprovalState,

    ) -> ApprovalState:

        #
        # Validate request
        #

        if not self.validator.validate(

            state

        ):

            self.logger.validation_failed()

            return state

        #
        # Estimate risk
        #

        state.risk_level = (

            self.rules.estimate_risk(

                state.action

            )

        )

        #
        # Approval type
        #

        state.approval_type = (

            self.rules.approval_type(

                state.action

            )

        )

        #
        # Need approval?
        #

        requires = (

            self.rules.requires_approval(

                action=state.action,

                risk_level=state.risk_level,

            )

        )

        if not requires:

            state.approve()

            self.logger.execution_continued(

                state

            )

            return state

        #
        # Wait for user approval
        #

        self.logger.approval_requested(

            state

        )

        return state

    # =====================================================
    # Approve
    # =====================================================

    def approve(

        self,

        state: ApprovalState,

    ) -> ApprovalState:

        state.approve()

        self.logger.approved(

            state

        )

        return state

    # =====================================================
    # Reject
    # =====================================================

    def reject(

        self,

        state: ApprovalState,

        reason: str = "",

    ) -> ApprovalState:

        state.reject(

            reason

        )

        self.logger.rejected(

            state

        )

        return state

    # =====================================================
    # Expire
    # =====================================================

    def expire(

        self,

        state: ApprovalState,

    ) -> ApprovalState:

        state.expire()

        self.logger.expired(

            state

        )

        return state