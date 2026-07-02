"""
Reflection Rules

Responsibilities

- Decide whether reflection is required
- Determine reflection type
- Estimate confidence
- Recommend reflection result

Future

- LLM-based Reflection
- Self-Evaluation
- User Feedback Analysis
- Adaptive Reflection
"""

from __future__ import annotations

from agents.reflection.reflection_models import (
    ConfidenceLevel,
    ReflectionResult,
    ReflectionType,
)

from agents.reflection.reflection_state import (
    ReflectionState,
)


class ReflectionRules:

    """
    Rule engine for Reflection Agent.
    """

    # =====================================================
    # Reflection Required
    # =====================================================

    def requires_reflection(

        self,

        state: ReflectionState,

    ) -> bool:

        #
        # Failed execution
        #

        if not state.execution_success:

            return True

        #
        # Slow execution
        #

        if state.execution_time_ms > 5000:

            return True

        #
        # Empty response
        #

        if not state.response.strip():

            return True

        return False

    # =====================================================
    # Reflection Type
    # =====================================================

    def reflection_type(

        self,

        state: ReflectionState,

    ) -> ReflectionType:

        if not state.execution_success:

            return ReflectionType.EXECUTION

        if state.execution_time_ms > 5000:

            return ReflectionType.PROVIDER_SELECTION

        if not state.response.strip():

            return ReflectionType.RESPONSE

        return ReflectionType.NONE

    # =====================================================
    # Confidence
    # =====================================================

    def confidence(

        self,

        state: ReflectionState,

    ) -> ConfidenceLevel:

        if not state.execution_success:

            return ConfidenceLevel.LOW

        if state.execution_time_ms > 5000:

            return ConfidenceLevel.MEDIUM

        return ConfidenceLevel.HIGH

    # =====================================================
    # Expected Result
    # =====================================================

    def expected_result(

        self,

        state: ReflectionState,

    ) -> ReflectionResult:

        if not state.execution_success:

            return ReflectionResult.RETRY

        if state.execution_time_ms > 5000:

            return ReflectionResult.FALLBACK

        if not state.response.strip():

            return ReflectionResult.REPLAN

        return ReflectionResult.SUCCESS