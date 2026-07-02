"""
Approval Validator

Responsibilities

- Validate approval requests
- Validate approval state
- Validate approval decisions

Future

- Expiration Validation
- Permission Validation
- Multi-Level Approval Validation
"""

from __future__ import annotations

from agents.human_in_the_loop.approval_models import (
    ApprovalStatus,
)

from agents.human_in_the_loop.approval_state import (
    ApprovalState,
)


class ApprovalValidator:

    """
    Validate approval requests before execution.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(

        self,

        state: ApprovalState,

    ) -> bool:

        if not self._validate_user(state):

            return False

        if not self._validate_task(state):

            return False

        if not self._validate_query(state):

            return False

        return True

    # =====================================================
    # User Validation
    # =====================================================

    def _validate_user(

        self,

        state: ApprovalState,

    ) -> bool:

        return state.user_id is not None

    # =====================================================
    # Task Validation
    # =====================================================

    def _validate_task(

        self,

        state: ApprovalState,

    ) -> bool:

        return bool(

            state.task_id.strip()

        )

    # =====================================================
    # Query Validation
    # =====================================================

    def _validate_query(

        self,

        state: ApprovalState,

    ) -> bool:

        return bool(

            state.query.strip()

        )

    # =====================================================
    # Approval Status
    # =====================================================

    def can_execute(

        self,

        state: ApprovalState,

    ) -> bool:

        return (

            state.status

            == ApprovalStatus.APPROVED

        )

    # =====================================================
    # Rejected
    # =====================================================

    def is_rejected(

        self,

        state: ApprovalState,

    ) -> bool:

        return (

            state.status

            == ApprovalStatus.REJECTED

        )

    # =====================================================
    # Pending
    # =====================================================

    def is_pending(

        self,

        state: ApprovalState,

    ) -> bool:

        return (

            state.status

            == ApprovalStatus.PENDING

        )

    # =====================================================
    # Expired
    # =====================================================

    def is_expired(

        self,

        state: ApprovalState,

    ) -> bool:

        return (

            state.status

            == ApprovalStatus.EXPIRED

        )