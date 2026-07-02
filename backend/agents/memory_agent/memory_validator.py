"""
Memory Validator

Responsibilities

- Validate memory requests
- Validate memory state
- Validate retrieval routes

Future

- Permission Validation
- Memory Expiration
- Access Policies
- Confidence Validation
"""

from __future__ import annotations

from agents.memory_agent.memory_state import (
    MemoryState,
)


class MemoryValidator:

    """
    Validate memory operations before retrieval.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(
        self,
        state: MemoryState,
    ) -> bool:

        if not self._validate_user(state):
            return False

        if not self._validate_query(state):
            return False

        if not self._validate_routes(state):
            return False

        return True

    # =====================================================
    # User Validation
    # =====================================================

    def _validate_user(
        self,
        state: MemoryState,
    ) -> bool:

        return state.user_id is not None

    # =====================================================
    # Query Validation
    # =====================================================

    def _validate_query(
        self,
        state: MemoryState,
    ) -> bool:

        return bool(
            state.query.strip()
        )

    # =====================================================
    # Route Validation
    # =====================================================

    def _validate_routes(
        self,
        state: MemoryState,
    ) -> bool:

        return len(
            state.requested_memory_types
        ) > 0