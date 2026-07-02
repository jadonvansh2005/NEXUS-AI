"""
Parallel Logger

Responsibilities

- Log parallel execution lifecycle
- Log worker assignments
- Log task completion
- Log execution failures

Future

- LangSmith
- OpenTelemetry
- ELK
- Grafana
"""

from __future__ import annotations

import logging

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


logger = logging.getLogger(__name__)


class ParallelLogger:

    """
    Centralized logger for Parallel Execution.
    """

    # =====================================================
    # Parallel Started
    # =====================================================

    def execution_started(

        self,

        state: ParallelState,

    ) -> None:

        logger.info(

            "[Parallel] Started | "

            "Workflow=%s | "

            "Tasks=%d | "

            "Workers=%d",

            state.workflow_id,

            len(

                state.pending_tasks

            ),

            state.max_workers,

        )

    # =====================================================
    # Task Scheduled
    # =====================================================

    def task_scheduled(

        self,

        worker_id: str,

        task_id: str,

    ) -> None:

        logger.info(

            "[Parallel] Scheduled | "

            "Worker=%s | "

            "Task=%s",

            worker_id,

            task_id,

        )

    # =====================================================
    # Task Completed
    # =====================================================

    def task_completed(

        self,

        task_id: str,

    ) -> None:

        logger.info(

            "[Parallel] Completed | "

            "Task=%s",

            task_id,

        )

    # =====================================================
    # Task Failed
    # =====================================================

    def task_failed(

        self,

        task_id: str,

        error: str,

    ) -> None:

        logger.error(

            "[Parallel] Failed | "

            "Task=%s | "

            "Error=%s",

            task_id,

            error,

        )

    # =====================================================
    # Execution Completed
    # =====================================================

    def execution_completed(

        self,

        state: ParallelState,

    ) -> None:

        logger.info(

            "[Parallel] Completed | "

            "Success=%d | "

            "Failed=%d",

            len(

                state.completed_tasks

            ),

            len(

                state.failed_tasks

            ),

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(

        self,

    ) -> None:

        logger.error(

            "[Parallel] Validation Failed"

        )