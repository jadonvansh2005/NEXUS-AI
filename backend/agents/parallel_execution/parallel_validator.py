"""
Parallel Validator

Responsibilities

- Validate parallel execution state
- Validate task graph
- Validate worker configuration

Future

- DAG Validation
- Resource Validation
- Distributed Worker Validation
"""

from __future__ import annotations

from agents.parallel_execution.dependency_analyzer import (
    DependencyAnalyzer,
)

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


class ParallelValidator:

    """
    Validate Parallel Execution before scheduling.
    """

    def __init__(self):

        self.dependency_analyzer = (

            DependencyAnalyzer()

        )

    # =====================================================
    # Public API
    # =====================================================

    def validate(

        self,

        state: ParallelState,

    ) -> bool:

        if not self._validate_tasks(

            state

        ):

            return False

        if not self._validate_workers(

            state

        ):

            return False

        if not self._validate_dependencies(

            state

        ):

            return False

        return True

    # =====================================================
    # Tasks
    # =====================================================

    def _validate_tasks(

        self,

        state: ParallelState,

    ) -> bool:

        return len(

            state.pending_tasks

        ) > 0

    # =====================================================
    # Workers
    # =====================================================

    def _validate_workers(

        self,

        state: ParallelState,

    ) -> bool:

        return state.max_workers > 0

    # =====================================================
    # Dependencies
    # =====================================================

    def _validate_dependencies(

        self,

        state: ParallelState,

    ) -> bool:

        #
        # No circular dependency allowed
        #

        return not self.dependency_analyzer.has_cycle(

            state

        )

    # =====================================================
    # Ready Tasks
    # =====================================================

    def has_ready_tasks(

        self,

        state: ParallelState,

    ) -> bool:

        return len(

            state.ready_tasks

        ) > 0

    # =====================================================
    # Completed
    # =====================================================

    def execution_finished(

        self,

        state: ParallelState,

    ) -> bool:

        return (

            len(

                state.pending_tasks

            ) == 0

            and

            len(

                state.running_tasks

            ) == 0

        )