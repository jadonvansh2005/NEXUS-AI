"""
Reflection Logger

Responsibilities

- Log reflection lifecycle
- Log reflection decisions
- Log recommendations
- Log failures

Future

- LangSmith
- OpenTelemetry
- ELK
- Grafana
"""

from __future__ import annotations

import logging

from agents.reflection.reflection_state import (
    ReflectionState,
)


logger = logging.getLogger(__name__)


class ReflectionLogger:

    """
    Centralized logger for Reflection Agent.
    """

    # =====================================================
    # Reflection Started
    # =====================================================

    def reflection_started(

        self,

        state: ReflectionState,

    ) -> None:

        logger.info(

            "[Reflection] Started | "

            "User=%s | "

            "Task=%s",

            state.user_id,

            state.task_id,

        )

    # =====================================================
    # Reflection Skipped
    # =====================================================

    def reflection_skipped(

        self,

    ) -> None:

        logger.info(

            "[Reflection] Skipped"

        )

    # =====================================================
    # Reflection Completed
    # =====================================================

    def reflection_completed(

        self,

        state: ReflectionState,

    ) -> None:

        logger.info(

            "[Reflection] Completed | "

            "Type=%s | "

            "Result=%s | "

            "Confidence=%s",

            state.reflection_type.value,

            state.result.value,

            state.confidence.value,

        )

    # =====================================================
    # Recommendation
    # =====================================================

    def recommendation(

        self,

        state: ReflectionState,

    ) -> None:

        if not state.recommendation:

            return

        logger.info(

            "[Reflection] Recommendation | %s",

            state.recommendation,

        )

    # =====================================================
    # Improvement
    # =====================================================

    def improvement(

        self,

        state: ReflectionState,

    ) -> None:

        if not state.improvement:

            return

        logger.info(

            "[Reflection] Improvement | %s",

            state.improvement,

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(

        self,

    ) -> None:

        logger.error(

            "[Reflection] Validation Failed"

        )

    # =====================================================
    # Reflection Failed
    # =====================================================

    def reflection_failed(

        self,

        error: str,

    ) -> None:

        logger.error(

            "[Reflection] Failed | %s",

            error,

        )