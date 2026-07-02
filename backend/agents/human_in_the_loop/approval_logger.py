"""
Approval Logger

Responsibilities

- Log approval lifecycle
- Log approval requests
- Log approvals
- Log rejections
- Log validation failures

Future

- LangSmith
- OpenTelemetry
- ELK
- Grafana
"""

from __future__ import annotations

import logging

from agents.human_in_the_loop.approval_state import (
    ApprovalState,
)


logger = logging.getLogger(__name__)


class ApprovalLogger:

    """
    Centralized logger for HITL.
    """

    # =====================================================
    # Approval Requested
    # =====================================================

    def approval_requested(

        self,

        state: ApprovalState,

    ) -> None:

        logger.info(

            "[HITL] Approval Requested | "

            "User=%s | "

            "Task=%s | "

            "Action=%s | "

            "Risk=%s",

            state.user_id,

            state.task_id,

            state.action.value,

            state.risk_level.value,

        )

    # =====================================================
    # Approved
    # =====================================================

    def approved(

        self,

        state: ApprovalState,

    ) -> None:

        logger.info(

            "[HITL] Approved | "

            "Task=%s",

            state.task_id,

        )

    # =====================================================
    # Rejected
    # =====================================================

    def rejected(

        self,

        state: ApprovalState,

    ) -> None:

        logger.warning(

            "[HITL] Rejected | "

            "Task=%s | "

            "Reason=%s",

            state.task_id,

            state.reason,

        )

    # =====================================================
    # Expired
    # =====================================================

    def expired(

        self,

        state: ApprovalState,

    ) -> None:

        logger.warning(

            "[HITL] Approval Expired | "

            "Task=%s",

            state.task_id,

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(

        self,

    ) -> None:

        logger.error(

            "[HITL] Validation Failed"

        )

    # =====================================================
    # Execution Continued
    # =====================================================

    def execution_continued(

        self,

        state: ApprovalState,

    ) -> None:

        logger.info(

            "[HITL] Execution Continued | "

            "Task=%s",

            state.task_id,

        )