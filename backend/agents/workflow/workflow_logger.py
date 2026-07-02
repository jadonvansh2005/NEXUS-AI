"""
Workflow Logger

Responsibilities

- Log workflow lifecycle
- Log task lifecycle
- Log failures
- Log execution metrics

Future

- LangSmith
- OpenTelemetry
- ELK Stack
- Prometheus
"""

from __future__ import annotations

import logging

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerTask,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


logger = logging.getLogger(__name__)


class WorkflowLogger:

    """
    Centralized workflow logger.
    """

    # =====================================================
    # Workflow
    # =====================================================

    def workflow_started(
        self,
        plan: ExecutionPlan,
    ) -> None:

        logger.info(
            "[Workflow] Started | Goal=%s | Domain=%s | Tasks=%d",
            plan.goal,
            plan.domain,
            len(plan.tasks),
        )

    def workflow_completed(
        self,
        state: WorkflowState,
    ) -> None:

        logger.info(
            "[Workflow] Completed | Completed=%d | Failed=%d",
            state.completed_tasks,
            state.failed_tasks,
        )

    def workflow_failed(
        self,
        error: str,
    ) -> None:

        logger.error(
            "[Workflow] Failed | %s",
            error,
        )

    # =====================================================
    # Task
    # =====================================================

    def task_started(
        self,
        task: PlannerTask,
    ) -> None:

        logger.info(
            "[Task] Started | %s (%s)",
            task.name,
            task.id,
        )

    def task_completed(
        self,
        task: PlannerTask,
    ) -> None:

        logger.info(
            "[Task] Completed | %s (%s)",
            task.name,
            task.id,
        )

    def task_failed(
        self,
        task: PlannerTask,
        error: str,
    ) -> None:

        logger.error(
            "[Task] Failed | %s | %s",
            task.name,
            error,
        )

    # =====================================================
    # Scheduler
    # =====================================================

    def scheduling(
        self,
        count: int,
    ) -> None:

        logger.info(
            "[Scheduler] Ready Tasks=%d",
            count,
        )

    # =====================================================
    # Dependency
    # =====================================================

    def dependency_wait(
        self,
        task: PlannerTask,
    ) -> None:

        logger.info(
            "[Dependency] Waiting | %s",
            task.name,
        )