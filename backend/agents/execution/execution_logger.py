"""
Execution Logger

Responsibilities

- Log execution lifecycle
- Log execution failures
- Log retries
- Log execution timing

Future

- LangSmith
- OpenTelemetry
- ELK
- Prometheus
- Grafana
"""

from __future__ import annotations

import logging

from agents.execution.execution_result import (
    ExecutionResult,
)

from agents.execution.execution_state import (
    ExecutionState,
)


logger = logging.getLogger(__name__)


class ExecutionLogger:

    """
    Centralized logger for Execution Controller.
    """

    # =====================================================
    # Execution Started
    # =====================================================

    def execution_started(
        self,
        state: ExecutionState,
    ) -> None:

        logger.info(

            "[Execution] Started | "

            "Task=%s | Tool=%s | Provider=%s",

            state.task_id,

            state.tool_name,

            state.provider_name,

        )

    # =====================================================
    # Execution Completed
    # =====================================================

    def execution_completed(
        self,
        result: ExecutionResult,
    ) -> None:

        logger.info(

            "[Execution] Completed | "

            "Tool=%s | Provider=%s | "

            "Time=%.2f ms",

            result.tool_name,

            result.provider_name,

            result.execution_time_ms,

        )

    # =====================================================
    # Execution Failed
    # =====================================================

    def execution_failed(
        self,
        error: str,
    ) -> None:

        logger.error(

            "[Execution] Failed | %s",

            error,

        )

    # =====================================================
    # Retry
    # =====================================================

    def retrying(
        self,
        retry_count: int,
        delay: float,
    ) -> None:

        logger.warning(

            "[Execution] Retry %d | "

            "Waiting %.2f sec",

            retry_count,

            delay,

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(
        self,
    ) -> None:

        logger.error(

            "[Execution] Validation Failed"

        )

    # =====================================================
    # Dispatcher Failed
    # =====================================================

    def dispatcher_failed(
        self,
        error: str,
    ) -> None:

        logger.error(

            "[Dispatcher] %s",

            error,

        )

    # =====================================================
    # Metrics
    # =====================================================

    def metrics(
        self,
        execution_time: float,
    ) -> None:

        logger.info(

            "[Execution] Duration = %.2f ms",

            execution_time,

        )