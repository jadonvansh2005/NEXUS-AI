"""
Reflection Validator

Responsibilities

- Validate reflection request
- Validate execution state
- Validate reflection inputs

Future

- Metrics Validation
- User Feedback Validation
- Reflection Permission Validation
"""

from __future__ import annotations

from agents.reflection.reflection_state import (
    ReflectionState,
)


class ReflectionValidator:

    """
    Validate reflection requests before processing.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(

        self,

        state: ReflectionState,

    ) -> bool:

        if not self._validate_user(state):

            return False

        if not self._validate_query(state):

            return False

        if not self._validate_execution(state):

            return False

        return True

    # =====================================================
    # User Validation
    # =====================================================

    def _validate_user(

        self,

        state: ReflectionState,

    ) -> bool:

        return state.user_id is not None

    # =====================================================
    # Query Validation
    # =====================================================

    def _validate_query(

        self,

        state: ReflectionState,

    ) -> bool:

        return bool(

            state.query.strip()

        )

    # =====================================================
    # Execution Validation
    # =====================================================

    def _validate_execution(

        self,

        state: ReflectionState,

    ) -> bool:

        #
        # Reflection should have at least one
        # execution-related artifact.
        #

        return any(

            [

                bool(state.tool_name),

                bool(state.provider_name),

                bool(state.response),

                state.execution_time_ms >= 0,

            ]

        )

    # =====================================================
    # Success
    # =====================================================

    def execution_successful(

        self,

        state: ReflectionState,

    ) -> bool:

        return state.execution_success

    # =====================================================
    # Failure
    # =====================================================

    def execution_failed(

        self,

        state: ReflectionState,

    ) -> bool:

        return not state.execution_success