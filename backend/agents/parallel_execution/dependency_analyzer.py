"""
Dependency Analyzer

Responsibilities

- Analyze task dependencies
- Detect parallel execution opportunities
- Build execution graph

Future

- DAG Optimization
- Critical Path Analysis
- Automatic Dependency Detection
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Set

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


class DependencyAnalyzer:

    """
    Analyze workflow dependencies for
    parallel execution.
    """

    # =====================================================
    # Analyze Dependencies
    # =====================================================

    def analyze(

        self,

        state: ParallelState,

    ) -> ParallelState:

        ready_tasks: List[str] = []

        for task in state.pending_tasks:

            dependencies = (

                state.dependencies.get(

                    task,

                    [],

                )

            )

            #
            # No dependencies
            #

            if not dependencies:

                ready_tasks.append(

                    task

                )

                continue

            #
            # All dependencies completed
            #

            if all(

                dependency

                in state.completed_tasks

                for dependency in dependencies

            ):

                ready_tasks.append(

                    task

                )

        state.ready_tasks = ready_tasks

        return state

    # =====================================================
    # Can Execute
    # =====================================================

    def can_execute(

        self,

        task_id: str,

        state: ParallelState,

    ) -> bool:

        dependencies = (

            state.dependencies.get(

                task_id,

                [],

            )

        )

        return all(

            dependency

            in state.completed_tasks

            for dependency in dependencies

        )

    # =====================================================
    # Independent Tasks
    # =====================================================

    def independent_tasks(

        self,

        state: ParallelState,

    ) -> List[str]:

        return [

            task

            for task

            in state.pending_tasks

            if not state.dependencies.get(

                task

            )

        ]

    # =====================================================
    # Dependency Graph
    # =====================================================

    def dependency_graph(

        self,

        state: ParallelState,

    ) -> Dict[str, List[str]]:

        return state.dependencies

    # =====================================================
    # Circular Dependency Check
    # =====================================================

    def has_cycle(

        self,

        state: ParallelState,

    ) -> bool:

        visited: Set[str] = set()

        recursion_stack: Set[str] = set()

        def dfs(

            task: str,

        ) -> bool:

            visited.add(

                task

            )

            recursion_stack.add(

                task

            )

            for dependency in state.dependencies.get(

                task,

                [],

            ):

                if dependency not in visited:

                    if dfs(

                        dependency

                    ):

                        return True

                elif dependency in recursion_stack:

                    return True

            recursion_stack.remove(

                task

            )

            return False

        for task in state.dependencies:

            if task not in visited:

                if dfs(

                    task

                ):

                    return True

        return False