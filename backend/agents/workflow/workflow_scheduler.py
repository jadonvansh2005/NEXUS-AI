"""
Workflow Scheduler

Responsibilities

- Select executable tasks
- Schedule workflow execution
- Support sequential and parallel execution

Future

- Priority Scheduling
- Resource Scheduling
- Worker Scheduling
- Dynamic Scheduling
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerTask,
)

from agents.workflow.dependency_resolver import (
    DependencyResolver,
)

from agents.workflow.workflow_models import (
    WorkflowType,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


class WorkflowScheduler:

    """
    Selects tasks that are ready for execution.
    """

    def __init__(self):

        self.resolver = (
            DependencyResolver()
        )

    # =====================================================
    # Public API
    # =====================================================

    def schedule(

        self,

        plan: ExecutionPlan,

        state: WorkflowState,

        workflow_type: WorkflowType = (
            WorkflowType.SEQUENTIAL
        ),

    ) -> List[PlannerTask]:

        ready_tasks = (
            self.resolver.get_ready_tasks(
                plan,
                state,
            )
        )

        if workflow_type == WorkflowType.SEQUENTIAL:

            return self._schedule_sequential(
                ready_tasks
            )

        if workflow_type == WorkflowType.PARALLEL:

            return self._schedule_parallel(
                ready_tasks
            )

        return ready_tasks

    # =====================================================
    # Sequential Scheduler
    # =====================================================

    def _schedule_sequential(

        self,

        tasks: List[PlannerTask],

    ) -> List[PlannerTask]:

        if len(tasks) == 0:

            return []

        #
        # Execute only first ready task.
        #

        return [

            tasks[0]

        ]

    # =====================================================
    # Parallel Scheduler
    # =====================================================

    def _schedule_parallel(

        self,

        tasks: List[PlannerTask],

    ) -> List[PlannerTask]:

        #
        # Future
        #
        # Resource Allocation
        # Worker Availability
        # Parallel Groups
        #

        return tasks