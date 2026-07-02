"""
Workflow Builder

Responsibilities

- Build workflow runtime
- Initialize workflow state
- Register planner tasks
- Prepare workflow execution

Future

- DAG generation
- Parallel groups
- Conditional branches
- Dynamic workflows
"""

from __future__ import annotations

from agents.planner.schemas import (
    ExecutionPlan,
)

from agents.workflow.workflow_models import (
    WorkflowStatus,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


class WorkflowBuilder:

    """
    Builds a runtime workflow from an ExecutionPlan.
    """

    def build(
        self,
        plan: ExecutionPlan,
    ) -> WorkflowState:

        state = WorkflowState()

        #
        # Workflow Created
        #

        state.workflow_status = (
            WorkflowStatus.CREATED
        )

        #
        # Register Tasks
        #

        for task in plan.tasks:

            state.add_task(
                task.id
            )

        #
        # Ready For Scheduling
        #

        state.workflow_status = (
            WorkflowStatus.READY
        )

        return state