"""
Dependency Resolver

Responsibilities

- Resolve task dependencies
- Check task readiness
- Find executable tasks

Future

- Parallel dependency groups
- Conditional dependencies
- Dynamic dependency injection
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerTask,
)

from agents.workflow.workflow_models import (
    WorkflowTaskStatus,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


class DependencyResolver:

    """
    Resolve workflow task dependencies.
    """

    # =====================================================
    # Ready Tasks
    # =====================================================

    def get_ready_tasks(
        self,
        plan: ExecutionPlan,
        state: WorkflowState,
    ) -> List[PlannerTask]:

        ready_tasks: List[PlannerTask] = []

        for task in plan.tasks:

            #
            # Already Completed
            #

            runtime = state.runtime_tasks.get(
                task.id
            )

            if runtime:

                if runtime.status in [

                    WorkflowTaskStatus.RUNNING,

                    WorkflowTaskStatus.COMPLETED,

                    WorkflowTaskStatus.FAILED,

                ]:
                    continue

            #
            # Dependency Check
            #

            if self.dependencies_satisfied(
                task,
                state,
            ):

                ready_tasks.append(
                    task
                )

        return ready_tasks

    # =====================================================
    # Dependency Check
    # =====================================================

    def dependencies_satisfied(
        self,
        task: PlannerTask,
        state: WorkflowState,
    ) -> bool:

        #
        # No Dependencies
        #

        if len(task.depends_on) == 0:

            return True

        #
        # Verify Every Dependency
        #

        for dependency in task.depends_on:

            runtime = state.runtime_tasks.get(
                dependency
            )

            if runtime is None:

                return False

            if runtime.status != (
                WorkflowTaskStatus.COMPLETED
            ):

                return False

        return True

    # =====================================================
    # Dependency Graph
    # =====================================================

    def dependency_graph(
        self,
        plan: ExecutionPlan,
    ) -> dict:

        graph = {}

        for task in plan.tasks:

            graph[task.id] = task.depends_on

        return graph