"""
Collaboration Logger

Responsibilities

- Log collaboration lifecycle
- Log agent assignments
- Log communication events
- Log merge operations

Future

- LangSmith
- OpenTelemetry
- ELK
- Grafana
"""

from __future__ import annotations

import logging

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


logger = logging.getLogger(__name__)


class CollaborationLogger:

    """
    Centralized logger for
    Multi-Agent Collaboration.
    """

    # =====================================================
    # Collaboration Started
    # =====================================================

    def collaboration_started(

        self,

        state: CollaborationState,

    ) -> None:

        logger.info(

            "[Collaboration] Started | "

            "Workflow=%s | "

            "Agents=%d | "

            "Tasks=%d",

            state.workflow_id,

            len(

                state.participating_agents

            ),

            len(

                state.tasks

            ),

        )

    # =====================================================
    # Agent Assigned
    # =====================================================

    def agent_assigned(

        self,

        agent_name: str,

        task_id: str,

    ) -> None:

        logger.info(

            "[Collaboration] Assigned | "

            "Agent=%s | "

            "Task=%s",

            agent_name,

            task_id,

        )

    # =====================================================
    # Message Published
    # =====================================================

    def message_published(

        self,

        event: str,

    ) -> None:

        logger.info(

            "[Collaboration] Event | "

            "%s",

            event,

        )

    # =====================================================
    # Agent Completed
    # =====================================================

    def agent_completed(

        self,

        agent_name: str,

    ) -> None:

        logger.info(

            "[Collaboration] Completed | "

            "Agent=%s",

            agent_name,

        )

    # =====================================================
    # Agent Failed
    # =====================================================

    def agent_failed(

        self,

        agent_name: str,

        error: str,

    ) -> None:

        logger.error(

            "[Collaboration] Failed | "

            "Agent=%s | "

            "Reason=%s",

            agent_name,

            error,

        )

    # =====================================================
    # Merge Started
    # =====================================================

    def merge_started(

        self,

    ) -> None:

        logger.info(

            "[Collaboration] Merging Responses"

        )

    # =====================================================
    # Merge Completed
    # =====================================================

    def merge_completed(

        self,

    ) -> None:

        logger.info(

            "[Collaboration] Merge Completed"

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(

        self,

    ) -> None:

        logger.error(

            "[Collaboration] Validation Failed"

        )

    # =====================================================
    # Collaboration Completed
    # =====================================================

    def collaboration_completed(

        self,

        state: CollaborationState,

    ) -> None:

        logger.info(

            "[Collaboration] Completed | "

            "Completed=%d | "

            "Failed=%d",

            len(

                state.completed_agents

            ),

            len(

                state.failed_agents

            ),

        )